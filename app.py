from flask import Flask,render_template,request,redirect,url_for,flash,abort
from flask_login import LoginManager,login_user,logout_user,login_required,current_user

from models import db,User,StaffProfile
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"
# Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key"

db.init_app(app)
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    admin=User.query.filter_by(username="admin").first()
    if admin is None:
        admin=User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='Admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created succesfully')
    
    else:
        print('Admin user already exists')
    staff = User.query.filter_by(username="staff1").first()

    if staff is None:
        staff = User(
        username="staff1",
        password=generate_password_hash("staff123"),
        role="Staff"
    )

        db.session.add(staff)
        db.session.commit()

    # Create Staff Profile
        staff_profile = StaffProfile(
        id=staff.id,
        phone="9876543210",
        experience=2,
        status="not assigned"
    )

        db.session.add(staff_profile)
        db.session.commit()

        print("Staff user created successfully")

    else:

        print("Staff user already exists")

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login",methods=["GET","POST"])
def login():
      if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Search user
        user = User.query.filter_by(username=username).first()

        # Username exists?
        if user is None:

            flash("Invalid Username")

            return redirect(url_for("login"))

        # Password correct?
        if not check_password_hash(user.password, password):

            flash("Invalid Password")

            return redirect(url_for("login"))

       
        login_user(user)

        # Redirect based on role

        if user.role == "Admin":

            return redirect(url_for("admin_dashboard"))

        elif user.role == "Staff":

            return redirect(url_for("staff_dashboard"))

        else:

            return redirect(url_for("user_dashboard"))

      return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]
        

        # Passwords must match
        if password != confirm_password:
            
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        # Username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("register"))
        
        print("Creating new user...")

        # Create new user
        new_user = User(

            username=username,

            password=generate_password_hash(password)

        )

        db.session.add(new_user)

        db.session.commit()
        
        

        flash("Registration Successful! Please Login.")

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "Admin":

        if current_user.role == "Staff":
            return redirect(url_for("staff_dashboard"))

        return redirect(url_for("user_dashboard"))

    return render_template("admin/dashboard.html")


@app.route("/staff/dashboard")
@login_required
def staff_dashboard():
    if current_user.role != "Staff":

        if current_user.role == "Admin":
            return redirect(url_for("admin_dashboard"))

        return redirect(url_for("user_dashboard"))

    return render_template("staff/dashboard.html")


@app.route("/user/dashboard")
@login_required
def user_dashboard():
     if current_user.role != "Trekker":

        if current_user.role == "Admin":
            return redirect(url_for("admin_dashboard"))

        return redirect(url_for("staff_dashboard"))

     return render_template("user/dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("login"))
    
if __name__ == "__main__":
    app.run(debug=True)
