from decimal import Decimal
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


def get_db():
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"]
    )


def fetch_all(sql, params=()):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


def cart_details():
    cart = session.get("cart", {})
    if not cart:
        return [], Decimal("0.00")
    ids = []
    for key in cart:
        try:
            ids.append(int(key))
        except (ValueError, TypeError):
            continue
    if not ids:
        return [], Decimal("0.00")
    placeholders = ",".join(["%s"] * len(ids))
    items = fetch_all(
        f"SELECT id, name, price, image_url FROM menu_items WHERE is_available=1 AND id IN ({placeholders})",
        tuple(ids)
    )
    rows, total = [], Decimal("0.00")
    for item in items:
        quantity = max(1, min(99, int(cart.get(str(item["id"]), 1))))
        subtotal = Decimal(str(item["price"])) * quantity
        item["quantity"] = quantity
        item["subtotal"] = subtotal
        rows.append(item)
        total += subtotal
    return rows, total


@app.context_processor
def inject_cart_count():
    cart = session.get("cart", {})
    return {"cart_count": sum(int(q) for q in cart.values()) if cart else 0}


@app.route("/")
def home():
    featured = fetch_all("SELECT * FROM menu_items WHERE is_available=1 ORDER BY id LIMIT 4")
    return render_template("index.html", featured=featured)


@app.route("/menu")
def menu():
    category = request.args.get("category", "").strip()
    categories = fetch_all("SELECT DISTINCT category FROM menu_items WHERE is_available=1 ORDER BY category")
    if category and category.lower() != "all":
        items = fetch_all(
            "SELECT * FROM menu_items WHERE is_available=1 AND category=%s ORDER BY name",
            (category,)
        )
    else:
        items = fetch_all("SELECT * FROM menu_items WHERE is_available=1 ORDER BY id")
    return render_template("menu.html", items=items, categories=categories, selected_category=category)


@app.post("/cart/add/<int:item_id>")
def add_to_cart(item_id):
    item = fetch_one("SELECT id FROM menu_items WHERE id=%s AND is_available=1", (item_id,))
    if not item:
        flash("This item is not available right now.", "error")
        return redirect(url_for("menu"))
    cart = session.get("cart", {})
    key = str(item_id)
    cart[key] = min(99, int(cart.get(key, 0)) + 1)
    session["cart"] = cart
    flash("Item added to your cart.", "success")
    return redirect(request.referrer or url_for("menu"))


@app.route("/cart")
def cart():
    items, total = cart_details()
    return render_template("cart.html", items=items, total=total)


@app.post("/cart/update")
def update_cart():
    cart_data = session.get("cart", {})
    for key in list(cart_data.keys()):
        try:
            qty = int(request.form.get(f"quantity_{key}", cart_data[key]))
            if qty <= 0:
                cart_data.pop(key, None)
            else:
                cart_data[key] = min(qty, 99)
        except (ValueError, TypeError):
            pass
    session["cart"] = cart_data
    flash("Cart updated.", "success")
    return redirect(url_for("cart"))


@app.post("/cart/remove/<int:item_id>")
def remove_from_cart(item_id):
    cart_data = session.get("cart", {})
    cart_data.pop(str(item_id), None)
    session["cart"] = cart_data
    flash("Item removed from your cart.", "success")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_details()
    if not items:
        flash("Your cart is empty. Add a dish before checkout.", "error")
        return redirect(url_for("menu"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        notes = request.form.get("notes", "").strip()
        if not all([name, email, phone, address]):
            flash("Please fill in all required fields.", "error")
            return render_template("checkout.html", items=items, total=total)
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO orders (customer_name,email,phone,address,notes,total) VALUES (%s,%s,%s,%s,%s,%s)",
                (name, email, phone, address, notes, str(total))
            )
            order_id = cur.lastrowid
            for item in items:
                cur.execute(
                    "INSERT INTO order_items (order_id,menu_item_id,item_name,quantity,unit_price) VALUES (%s,%s,%s,%s,%s)",
                    (order_id, item["id"], item["name"], item["quantity"], str(item["price"]))
                )
            conn.commit()
            session["cart"] = {}
            return render_template("success.html", order_id=order_id, customer_name=name, total=total)
        except Error:
            conn.rollback()
            flash("We could not save your order. Check the database connection and try again.", "error")
        finally:
            cur.close()
            conn.close()
    return render_template("checkout.html", items=items, total=total)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not all([name, email, message]):
            flash("Please complete all contact fields.", "error")
        else:
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO contact_messages (name,email,message) VALUES (%s,%s,%s)",
                    (name, email, message)
                )
                conn.commit()
                flash("Thanks! Your message has been received.", "success")
                return redirect(url_for("contact"))
            except Error:
                conn.rollback()
                flash("Message could not be saved. Please try again.", "error")
            finally:
                cur.close()
                conn.close()
    return render_template("contact.html")


@app.errorhandler(500)
def server_error(_error):
    return render_template("base.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
