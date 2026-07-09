from flask import render_template, redirect, url_for,Blueprint,request,flash
from flask_login import login_required, current_user

from models import db,User,Booking,Trek
from datetime import date

# Blueprint
user_bp=Blueprint("user",__name__)

@user_bp.route("/user/dashboard")
@login_required
def user_dashboard():
        if current_user.role != "Trekker":

            if current_user.role == "Admin":
                return redirect(url_for("admin.admin_dashboard"))

            return redirect(url_for("staff.staff_dashboard"))
        
        return render_template("user/dashboard.html")

        total_bookings=Booking.query.filter_by(user_id=current_user.id).count()

        upcoming_treks=Booking.query.join(Booking.trek).filter(
            Booking.user_id == current_user.id,
            Booking.trek.has(status="Completed") 
        ).count()

        completed_treks = Booking.query.join(Booking.trek).filter(
             Booking.user_id == current_user.id,
             Booking.trek.has(status="Completed")
        ).count()

        return render_template(
             "user/dashboard.html",
             total_bookings=total_bookings,
             upcoming_treks=upcoming_treks,
             completed_treks=completed_treks
            )


@user_bp.route("/user/profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if current_user.role != "Trekker":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("staff.staff_dashboard"))

    if request.method == "POST":

        email=request.form["email"]

        existing_email = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if existing_email:

            flash("Email already exists.")

            return redirect(url_for("user.edit_profile"))

        current_user.full_name=request.form["full_name"]

        current_user.email=email

        current_user.phone=request.form["phone"]

        db.session.commit()

        flash("Profile updated successfully!")

        return redirect(url_for("user.edit_profile"))

    return render_template("user/edit_profile.html")


@user_bp.route("/user/treks")
@login_required
def available_treks():

    if current_user.role != "Trekker":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("staff.staff_dashboard"))

    search=request.args.get("search", "").strip()

    difficulty=request.args.get("difficulty", "").strip()

    destination=request.args.get("destination", "").strip()

    treks=Trek.query.filter(Trek.status == "Open", Trek.available_slots > 0)

    if search:

        treks=treks.filter(Trek.trek_name.ilike(f"%{search}%"))

    if difficulty:

        treks=treks.filter(Trek.difficulty == difficulty)

    if destination:

        treks=treks.filter(Trek.destination.ilike(f"%{destination}%"))

    treks=treks.order_by(Trek.start_date).all()

    return render_template(
        "user/available_treks.html",
        treks=treks,
        search=search,
        difficulty=difficulty,
        destination=destination
    )


@user_bp.route("/user/trek/<int:id>")
@login_required
def trek_details(id):

    if current_user.role != "Trekker":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("staff.staff_dashboard"))

    trek=Trek.query.get_or_404(id)

    return render_template("user/trek_details.html",trek=trek)


@user_bp.route("/user/book/<int:id>")
@login_required
def book_trek(id):

    if current_user.role != "Trekker":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("staff.staff_dashboard"))

    trek=Trek.query.get_or_404(id)

    # Trek must be open
    if trek.status != "Open": 

        flash("This trek is not open for booking.")

        return redirect(url_for("user.trek_details", id=id))

    # Slots available
    if trek.available_slots <= 0:

        flash("No slots available for this trek.")

        return redirect(url_for("user.trek_details", id=id))

    # Duplicate booking check
    existing_booking=Booking.query.filter_by(user_id=current_user.id,trek_id=id).first()

    if existing_booking:

        flash("You have already booked this trek.")

        return redirect(url_for("user.trek_details", id=id))

    booking=Booking(user_id=current_user.id,trek_id=id)

    db.session.add(booking)

    trek.available_slots -= 1

    db.session.commit()

    flash("Trek booked successfully!")

    return redirect(url_for("user.my_bookings"))


@user_bp.route("/user/bookings")
@login_required
def my_bookings():

    if current_user.role != "Trekker":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("staff.staff_dashboard"))

    bookings=Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template("user/my_bookings.html",bookings=bookings)


@user_bp.route("/user/history")
@login_required
def trekking_history():

    if current_user.role != "Trekker":

        if current_user.role == "Admin":
            return redirect(url_for("admin.admin_dashboard"))

        return redirect(url_for("staff.staff_dashboard"))

    history = Booking.query.join(Trek).filter(
        Booking.user_id == current_user.id,
        Trek.status == "Completed"
    ).order_by(
        Trek.end_date.desc()
    ).all()

    return render_template(
        "user/history.html",
        history=history
    )



    
  
