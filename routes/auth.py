from flask import render_template, request, redirect, url_for, flash,Blueprint
from flask_login import login_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

# Blueprint
auth_bp = Blueprint("auth", __name__)

# Home Route
@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@auth_bp.route("/login",methods=["GET","POST"])
def login():
      if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Search user
        user = User.query.filter_by(username=username).first()

        # Username exists?
        if user is None:

            flash("Invalid Username")

            return redirect(url_for("auth.login"))

        # Password correct?
        if not check_password_hash(user.password, password):

            flash("Invalid Password")

            return redirect(url_for("auth.login"))

       
        login_user(user)

        # Redirect based on role

        if user.role == "Admin":

            return redirect(url_for("admin.admin_dashboard"))

        elif user.role == "Staff":

            return redirect(url_for("staff.staff_dashboard"))

        else:

            return redirect(url_for("user.user_dashboard"))

      return render_template("login.html")

@auth_bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]
        

        # Passwords must match
        if password != confirm_password:
            
            flash("Passwords do not match.")
            return redirect(url_for("auth.register"))

        # Username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("auth.register"))
        
        print("Creating new user...")

        # Create new user
        new_user = User(

            username=username,

            password=generate_password_hash(password)

        )

        db.session.add(new_user)

        db.session.commit()
        
        

        flash("Registration Successful! Please Login.")

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("auth.login"))
