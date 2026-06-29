from flask import render_template, redirect, url_for,Blueprint
from flask_login import login_required, current_user

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