from flask import render_template, redirect, url_for,Blueprint,request,flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from models import db,Trek,User,StaffProfile,Booking
from datetime import datetime

# Blueprint
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/dashboard")
@login_required

def admin_dashboard():
    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    return render_template("admin/dashboard.html")



@admin_bp.route("/admin/treks")
@login_required

def list_treks():
     
     if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))
     
     treks=Trek.query.order_by(Trek.id).all()

     return render_template("admin/treks/list.html",treks=treks)


@admin_bp.route("/admin/treks/create", methods=["GET", "POST"])
@login_required
def create_trek():

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    if request.method == "POST":

        trek = Trek(
            trek_name=request.form["trek_name"],
            destination=request.form["destination"],
            difficulty=request.form["difficulty"],
            duration=int(request.form["duration"]),
            price=request.form["price"],
            available_slots=int(request.form["available_slots"]),
            start_date=datetime.strptime(
                request.form["start_date"],
                "%Y-%m-%d"
            ).date(),
            end_date=datetime.strptime(
                request.form["end_date"],
                "%Y-%m-%d"
            ).date(),
            description=request.form["description"]
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek created successfully!")

        return redirect(url_for("admin.list_treks"))

    return render_template("admin/treks/create.html")

@admin_bp.route("/admin/treks/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_trek(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    trek = Trek.query.get_or_404(id)

    if request.method == "POST":

        trek.trek_name = request.form["trek_name"]
        trek.destination = request.form["destination"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.price = request.form["price"]
        trek.available_slots = int(request.form["available_slots"])
        trek.start_date = datetime.strptime(
            request.form["start_date"],
            "%Y-%m-%d"
        ).date()
        trek.end_date = datetime.strptime(
            request.form["end_date"],
            "%Y-%m-%d"
        ).date()
        trek.description = request.form["description"]

        db.session.commit()

        flash("Trek updated successfully!")

        return redirect(url_for("admin.list_treks"))

    return render_template(
        "admin/treks/edit.html",
        trek=trek
    )


@admin_bp.route("/admin/treks/delete/<int:id>")
@login_required
def delete_trek(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    trek = Trek.query.get_or_404(id)

    db.session.delete(trek)

    db.session.commit()

    flash("Trek deleted successfully!")

    return redirect(url_for("admin.list_treks"))


@admin_bp.route("/admin/staff")
@login_required
def list_staff():

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    staff_members = (User.query.filter_by(role="Staff").order_by(User.id).all())

    return render_template("admin/staff/list.html",staff_members=staff_members)


@admin_bp.route("/admin/staff/create", methods=["GET", "POST"])
@login_required
def create_staff():

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    if request.method == "POST":

        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"]),
            role="Staff"
        )

        db.session.add(user)
        db.session.commit()

        staff_profile = StaffProfile(
            id=user.id,
            phone=request.form["phone"],
            experience=int(request.form["experience"]),
            status="not assigned"
        )

        db.session.add(staff_profile)
        db.session.commit()

        flash("Staff added successfully!")

        return redirect(url_for("admin.list_staff"))

    return render_template("admin/staff/create.html")


@admin_bp.route("/admin/staff/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_staff(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    user = User.query.get_or_404(id)
    staff_profile = StaffProfile.query.get_or_404(id)

    if request.method == "POST":

        user.username = request.form["username"]

        new_password=request.form["password"]

        if new_password:
            user.password = generate_password_hash(new_password)

        staff_profile.phone = request.form["phone"]

        staff_profile.experience = int(request.form["experience"])

        db.session.commit()

        flash("Staff updated successfully!")

        return redirect(url_for("admin.list_staff"))

    return render_template("admin/staff/edit.html",user=user,staff_profile=staff_profile)


@admin_bp.route("/admin/staff/delete/<int:id>")
@login_required
def delete_staff(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    user = User.query.get_or_404(id)
    staff_profile = StaffProfile.query.get_or_404(id)

    db.session.delete(staff_profile)
    db.session.delete(user)

    db.session.commit()

    flash("Staff deleted successfully!")

    return redirect(url_for("admin.list_staff"))


