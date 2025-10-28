
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.utils import secure_filename
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "farmtohome.db")

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.executescript(open("schema.sql").read())
        conn.commit()

app = Flask(__name__)
app.secret_key = "dev-secret-key-for-demo"  # Replace for production

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB limit

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.cli.command("init")
def db_init():
    init_db()
    print("Initialized the database.")

@app.route("/")
def index():
    listings = query_db("SELECT l.*, f.name AS farmer_name FROM listings l JOIN farmers f ON l.farmer_id = f.id ORDER BY l.created_at DESC")
    return render_template("index.html", listings=listings)

# Farmer registration (very simple)
@app.route("/farmer/register", methods=["GET", "POST"])
def farmer_register():
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        db = get_db()
        db.execute("INSERT INTO farmers (name, phone, email, password) VALUES (?,?,?,?)", (name, phone, email, password))
        db.commit()
        flash("Farmer registered. Please log in.", "success")
        return redirect(url_for("farmer_login"))
    return render_template("farmer_register.html")

@app.route("/farmer/login", methods=["GET", "POST"])
def farmer_login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        farmer = query_db("SELECT * FROM farmers WHERE email = ? AND password = ?", (email, password), one=True)
        if farmer:
            session["farmer_id"] = farmer["id"]
            session["farmer_name"] = farmer["name"]
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("farmer_login.html")

@app.route("/farmer/logout")
def farmer_logout():
    session.pop("farmer_id", None)
    session.pop("farmer_name", None)
    flash("Logged out.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "farmer_id" not in session:
        return redirect(url_for("farmer_login"))
    farmer_id = session["farmer_id"]
    listings = query_db("SELECT * FROM listings WHERE farmer_id = ? ORDER BY created_at DESC", (farmer_id,))
    return render_template("dashboard.html", listings=listings)

@app.route("/listing/new", methods=["GET", "POST"])
def listing_new():
    if "farmer_id" not in session:
        return redirect(url_for("farmer_login"))
    if request.method == "POST":
        title = request.form["title"].strip()
        qty = request.form["quantity"].strip()
        price = request.form["price"].strip()
        desc = request.form["description"].strip()
        image = request.files.get("image")
        filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(save_path)
        db = get_db()
        db.execute("INSERT INTO listings (farmer_id, title, quantity, price, description, image) VALUES (?,?,?,?,?,?)",
                   (session["farmer_id"], title, qty, price, desc, filename))
        db.commit()
        flash("Listing created.", "success")
        return redirect(url_for("dashboard"))
    return render_template("listing_new.html")

@app.route("/listing/<int:lid>")
def listing_detail(lid):
    listing = query_db("SELECT l.*, f.name AS farmer_name, f.phone AS farmer_phone FROM listings l JOIN farmers f ON l.farmer_id = f.id WHERE l.id = ?", (lid,), one=True)
    if not listing:
        return "Not found", 404
    return render_template("listing_detail.html", listing=listing)

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        message = request.form["message"].strip()
        listing_id = request.form.get("listing_id")
        db = get_db()
        db.execute("INSERT INTO contacts (name, phone, message, listing_id) VALUES (?,?,?,?)", (name, phone, message, listing_id))
        db.commit()
        flash("Your message has been sent. Farmer will contact you.", "success")
        return redirect(url_for("index"))
    return render_template("contact.html")

# Admin-like pages (no auth) to view contacts (for demo)
@app.route("/admin/contacts")
def admin_contacts():
    contacts = query_db("SELECT c.*, l.title AS listing_title FROM contacts c LEFT JOIN listings l ON c.listing_id = l.id ORDER BY c.created_at DESC")
    return render_template("admin_contacts.html", contacts=contacts)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
