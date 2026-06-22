from flask import Flask
from models import db,User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key"

db.init_app(app)

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

@app.route("/")
def home():
    return "<h1>Trekking Management Application</h1>"

if __name__ == "__main__":
    app.run(debug=True)
