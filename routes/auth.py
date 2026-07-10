from flask import render_template, request, redirect, url_for, flash,Blueprint
from flask_login import login_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from models import db,User,StaffProfile

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
        
        # Check if account is active
        if not user.is_active:

            flash("Your account has been deactivated. Please contact the administrator.")

            return redirect(url_for("auth.login"))
        
        if user.role == "Staff" and user.approval_status != "Approved":

            flash("Your staff account is waiting for admin approval.")

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

        full_name = request.form.get("full_name")

        email = request.form.get("email")

        phone = request.form.get("phone")
        

        # Passwords must match
        if password != confirm_password:
            
            flash("Passwords do not match.")
            return redirect(url_for("auth.register"))

        # Username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("auth.register"))
        
        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))
        
        print("Creating new user...")

        # Create new user
        new_user = User(

            username=username,
            password=generate_password_hash(password),
            full_name=full_name,
            email=email,
            phone=phone,
            role="Trekker"
        )

        db.session.add(new_user)

        db.session.commit()
        
        

        flash("Registration Successful! Please Login.")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/staff/register", methods=["GET", "POST"])
def staff_register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        experience = request.form.get("experience")

        # Passwords must match
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("auth.staff_register"))

        # Username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("auth.staff_register"))

        # Email already exists
        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash("Email already registered.")
            return redirect(url_for("auth.staff_register"))

        # Create Staff User
        new_staff = User(
            username=username,
            password=generate_password_hash(password),
            full_name=full_name,
            email=email,
            phone=phone,
            role="Staff",
            approval_status="Pending"
        )

        db.session.add(new_staff)
        db.session.commit()

        # Create Staff Profile
        staff_profile = StaffProfile(
            id=new_staff.id,
            phone=phone,
            experience=int(experience) if experience else None,
            status="not assigned"
        )

        db.session.add(staff_profile)
        db.session.commit()

        flash("Registration successful! Please wait for admin approval before logging in")

        return redirect(url_for("auth.login"))

    return render_template("staff_register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("auth.login"))
