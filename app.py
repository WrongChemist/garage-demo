from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
import os
from models import db, User, Car, Ticket
from auth import admin_required
from logger import setup_logger
from upload import save_car_image
from admin_create import create_admin



port = int(os.environment.get("PORT", 5000))

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
setup_logger(app)

@app.route("/")
def index():
    return render_template("index.html", Car=Car.query.all())



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        session["user"] = {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }

        flash("Logged in successfully")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out")
    return redirect(url_for("login"))



# ---------------- USERS CRUD ----------------

@app.route("/users")
@admin_required
def users_list():
    users = User.query.all()
    return render_template("users/list.html", users=users)

# ---------------- CARS CRUD ----------------

@app.route("/cars/create", methods=["GET", "POST"])
@admin_required
def create_car():
    if request.method == "POST":
        model = request.form["model"]
        plate = request.form["license_plate"]
        user_id = request.form["user_id"]
        image = save_car_image(request.files.get("image"))

        car = Car(model=model, license_plate=plate, user_id=user_id, image_path=image)
        db.session.add(car)
        db.session.commit()
        return redirect(url_for("index"))

    users = User.query.all()
    return render_template("cars/create.html", users=users)

# ---------------- TICKETS CRUD ----------------

@app.route("/tickets/create/<int:car_id>", methods=["GET", "POST"])
@admin_required
def create_ticket(car_id):
    if request.method == "POST":
        desc = request.form["description"]
        ticket = Ticket(description=desc, car_id=car_id)
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("tickets/create.html", car_id=car_id)

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        create_admin(app)
    app.run(host='0.0.0.0', port=port, debug=True)
