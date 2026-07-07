from flask import Flask,render_template,request,redirect,url_for,flash,abort
from flask_login import LoginManager,login_user,logout_user,login_required,current_user

from models import db,User,StaffProfile
from werkzeug.security import generate_password_hash,check_password_hash

# Register blueprint
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.user import user_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"

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
            full_name="System Administrator",
            email="admin@trek.com",
            phone="9999999999",
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
        full_name="Sai Neeraj",
        email="staff1@trek.com",
        phone="9876543210",
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

'''@app.route("/")
def home():
    return redirect(url_for("login"))'''

if __name__ == "__main__":
    app.run(debug=True)
