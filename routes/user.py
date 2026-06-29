from flask import render_template, redirect, url_for,Blueprint
from flask_login import login_required, current_user

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
