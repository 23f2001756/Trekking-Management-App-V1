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

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(
        role="Trekker"
    ).count()

    total_staff = User.query.filter_by(
        role="Staff",
        approval_status="Approved"
    ).count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )

@admin_bp.route("/admin/treks")
@login_required

def list_treks():
     
     if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))
     
     search = request.args.get("search", "").strip()

     if search:

        treks = Trek.query.filter(
            (Trek.trek_name.ilike(f"%{search}%")) |
            (Trek.destination.ilike(f"%{search}%"))
        ).order_by(Trek.id).all()

     else:
        treks = Trek.query.order_by(Trek.id).all()
     return render_template("admin/treks/list.html",treks=treks)


@admin_bp.route("/admin/treks/create", methods=["GET", "POST"])
@login_required
def create_trek():

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    if request.method == "POST":

        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()

        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()

        duration = int(request.form["duration"])

        if end_date < start_date:

            flash("End date cannot be earlier than start date.")

            return redirect(url_for("admin.create_trek"))

        expected_duration = (end_date - start_date).days + 1

        if duration != expected_duration:

            flash(f"Duration should be {expected_duration} day(s) based on the selected dates.")

            return redirect(url_for("admin.create_trek"))

        trek = Trek(
            trek_name=request.form["trek_name"],
            destination=request.form["destination"],
            difficulty=request.form["difficulty"],
            duration=int(request.form["duration"]),
            price=request.form["price"],
            available_slots=int(request.form["available_slots"]),
            start_date=datetime.strptime(request.form["start_date"],"%Y-%m-%d").date(),
            end_date=datetime.strptime(request.form["end_date"],"%Y-%m-%d").date(),
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

        start_date = datetime.strptime(request.form["start_date"],"%Y-%m-%d").date()

        end_date = datetime.strptime(request.form["end_date"],"%Y-%m-%d").date()

        duration = int(request.form["duration"])

        if end_date < start_date:

            flash("End date cannot be earlier than start date.")

            return redirect(url_for("admin.edit_trek", id=id))

        expected_duration = (end_date - start_date).days + 1

        if duration != expected_duration:

            flash(f"Duration should be {expected_duration} day(s) based on the selected dates.")

            return redirect(url_for("admin.edit_trek", id=id))

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

        if trek.status == "Completed" and trek.assigned_staff_id:

            staff = StaffProfile.query.get(trek.assigned_staff_id)

            if staff:
                staff.status = "not assigned"

            trek.assigned_staff_id = None

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

    if trek.bookings:

        flash("Cannot delete trek because bookings already exist.")

        return redirect(url_for("admin.list_treks"))

    if trek.assigned_staff_id:
        staff = StaffProfile.query.get(trek.assigned_staff_id)

        if staff:
            staff.status = "not assigned"

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
    
    search = request.args.get("search", "").strip()

    if search:

        staff_members = User.query.join(StaffProfile).filter(
            User.role == "Staff",
            User.approval_status == "Approved",
            (
                User.username.ilike(f"%{search}%") |
                StaffProfile.phone.ilike(f"%{search}%")
            )
        ).order_by(User.id).all()

    else:

        staff_members = User.query.filter_by(
            role="Staff",
            approval_status="Approved"
        ).order_by(User.id).all()

    return render_template("admin/staff/list.html",staff_members=staff_members)

@admin_bp.route("/admin/staff/pending")
@login_required
def pending_staff():

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    pending_staff = User.query.filter_by(
        role="Staff",
        approval_status="Pending"
    ).order_by(User.id).all()

    return render_template("admin/staff/pending.html",pending_staff=pending_staff)

@admin_bp.route("/admin/staff/approve/<int:id>")
@login_required
def approve_staff(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    user = User.query.get_or_404(id)

    if user.role != "Staff":

        flash("Invalid staff account.")

        return redirect(url_for("admin.pending_staff"))

    user.approval_status = "Approved"

    db.session.commit()

    flash("Staff approved successfully!")

    return redirect(url_for("admin.pending_staff"))

@admin_bp.route("/admin/staff/reject/<int:id>")
@login_required
def reject_staff(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    user = User.query.get_or_404(id)

    if user.role != "Staff":

        flash("Invalid staff account.")

        return redirect(url_for("admin.pending_staff"))

    staff_profile = StaffProfile.query.get(id)

    if staff_profile:

        db.session.delete(staff_profile)

    db.session.delete(user)

    db.session.commit()

    flash("Staff registration rejected.")

    return redirect(url_for("admin.pending_staff"))





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
         
        user.full_name = request.form["full_name"]

        user.email = request.form["email"]

        user.phone = request.form["phone"]

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

    assigned_trek = Trek.query.filter_by(
        assigned_staff_id=staff_profile.id
    ).first()

    if assigned_trek:

        flash("Cannot delete staff because they are assigned to a trek.")

        return redirect(url_for("admin.list_staff"))

    db.session.delete(staff_profile)
    db.session.delete(user)

    db.session.commit()

    flash("Staff deleted successfully!")

    return redirect(url_for("admin.list_staff"))


@admin_bp.route("/admin/treks/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign_staff(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    trek = Trek.query.get_or_404(id)

    staff_members = StaffProfile.query.join(User).filter(
    User.approval_status == "Approved",
    StaffProfile.status == "not assigned"
    ).all()

    if request.method == "POST":

        new_staff = StaffProfile.query.get(request.form["staff_id"])

        if trek.assigned_staff_id:

            old_staff = StaffProfile.query.get(trek.assigned_staff_id)

            if old_staff:
                old_staff.status = "not assigned"

        trek.assigned_staff_id = new_staff.id

        new_staff.status = "assigned"

        db.session.commit()

        flash("Staff assigned successfully!")

        return redirect(url_for("admin.list_treks"))

    return render_template("admin/treks/assign_staff.html",trek=trek,staff_members=staff_members)


@admin_bp.route("/admin/users")
@login_required
def list_users():

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))
    
    search = request.args.get("search", "").strip()

    if search:

        users = User.query.filter(
            User.role == "Trekker",
            User.username.ilike(f"%{search}%")
        ).order_by(User.id).all()

    else:

        users = User.query.filter_by(
            role="Trekker"
        ).order_by(User.id).all()

    return render_template("admin/users/list.html",users=users)


@admin_bp.route("/admin/users/toggle/<int:id>")
@login_required
def toggle_user_status(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    user = User.query.get_or_404(id)

    user.is_active = not user.is_active

    db.session.commit()

    if user.is_active:
        flash("User activated successfully!")
    else:
        flash("User deactivated successfully!")

    return redirect(url_for("admin.list_users"))


@admin_bp.route("/admin/staff/toggle/<int:id>")
@login_required
def toggle_staff_status(id):

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    user = User.query.get_or_404(id)

    if user.role != "Staff":

        flash("Invalid staff account.")

        return redirect(url_for("admin.list_staff"))

    user.is_active = not user.is_active

    db.session.commit()

    if user.is_active:

        flash("Staff activated successfully!")

    else:

        flash("Staff deactivated successfully!")

    return redirect(url_for("admin.list_staff"))


@admin_bp.route("/admin/bookings")
@login_required
def list_bookings():

    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff.staff_dashboard"))

        return redirect(url_for("user.user_dashboard"))

    bookings = Booking.query.order_by(Booking.id.desc()).all()

    return render_template("admin/bookings/list.html",bookings=bookings)


