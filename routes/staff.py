from flask import render_template, redirect, url_for,Blueprint,request,flash
from flask_login import login_required, current_user

from models import db,Trek,StaffProfile

# Blueprint
staff_bp=Blueprint("staff",__name__)

@staff_bp.route("/staff/dashboard")
@login_required
def staff_dashboard():
    if current_user.role != "Staff":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    return render_template("staff/dashboard.html")

    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id ).all()

    total_assigned = len(assigned_treks)

    total_registered = sum(len(trek.bookings) for trek in assigned_treks )

    open_treks = sum(1 for trek in assigned_treks if trek.status == "Open" )

    completed_treks = sum(1 for trek in assigned_treks if trek.status == "Completed")

    return render_template("staff/dashboard.html",
                           total_assigned=total_assigned,
                           total_registered=total_registered,
                           open_treks=open_treks,
                           completed_treks=completed_treks )

@staff_bp.route("/staff/profile", methods=["GET", "POST"])
@login_required
def staff_profile():

    if current_user.role != "Staff":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    profile = StaffProfile.query.get(current_user.id)

    if request.method == "POST":

        profile.phone = request.form["phone"]
        profile.experience = request.form["experience"]

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("staff.staff_profile"))

    return render_template("staff/profile.html",profile=profile)