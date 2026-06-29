from flask import render_template, redirect, url_for,Blueprint
from flask_login import login_required, current_user

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