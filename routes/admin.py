from flask import render_template, redirect, url_for,Blueprint,request,flash
from flask_login import login_required, current_user

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


