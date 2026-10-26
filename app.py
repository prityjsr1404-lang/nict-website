import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import data
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/google1234567890abcdef.html')
def google_verification():
    return send_from_directory(
        app.root_path,
        'google1234567890abcdef.html'
    )
# Models Import karein
from models import db, User, Enquiry

class ContactForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(2, 80)])
    phone = StringField("Phone Number", validators=[DataRequired(), Length(10, 15)])
    course = SelectField("Interested Course", choices=[
        ("school", "School Syllabus (ICSE/ISC/CBSE)"),
        ("doa", "D.O.A (Office Automation)"),
        ("excel", "Advance Excel"),
        ("tally", "Tally Prime"),
        ("dtp", "D.T.P"),
        ("other", "Other")
    ])
    message = TextAreaField("Message", validators=[DataRequired(), Length(5, 500)])
    submit = SubmitField("Claim Discount & Register Now")

# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Database Config (SQLite use kar rahe hain)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nict_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Login Manager Setup
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # App ke start hote hi database table bana dega
    with app.app_context():
        db.create_all()
        # Ek default Admin User banana (Username: admin, Password: admin123)
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin123')
            new_admin = User(username='admin', password=hashed_pw)
            db.session.add(new_admin)
            db.session.commit()

    # Context Processor
    app.context_processor(lambda: {
        "INSTITUTE_NAME": "NICT COMPUTER",
        "TAGLINE": "TRAINING CENTER • JAMSHEDPUR",
        "MAIN_BRANCH": data.BRANCHES[0],
        "NEW_BRANCH": data.BRANCHES[1],
        "CONTACT_NUMBER": data.BRANCHES[0]['phone']
    })

    # ================= ROUTES =================
    
    @app.route("/")
    def index():
        return render_template("index.html", stats=data.HERO_STATS, toppers=data.TOPPERS[:3], courses=data.PROFESSIONAL_COURSES)

    @app.route("/about")
    def about():
        return render_template("about.html", about=data.ABOUT_TEXT)

    @app.route("/faculty")
    def faculty():
        return render_template("faculty.html", faculty=data.FACULTY)

    @app.route("/toppers")
    def toppers():
        return render_template("toppers.html", toppers=data.TOPPERS)

    @app.route("/school-syllabus")
    def school_syllabus():
        return render_template("school_syllabus.html", syllabus=data.SCHOOL_SYLLABUS)

    @app.route("/courses")
    def courses():
        return render_template("courses.html", courses=data.PROFESSIONAL_COURSES)

    @app.route("/branches")
    def branches():
        return render_template("branches.html", branches=data.BRANCHES)

    # Contact Route (Yahan data database mein save hoga)
    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            # Naya Enquiry Database mein save karein
            new_enquiry = Enquiry(
                name=form.name.data,
                phone=form.phone.data,
                course=dict(form.course.choices).get(form.course.data),
                message=form.message.data
            )
            db.session.add(new_enquiry)
            db.session.commit()
            
            flash(f"Thank you {form.name.data}! Our team will call you shortly.", "success")
            return redirect(url_for("contact"))
        return render_template("contact.html", form=form)

    # ================= ADMIN / STAFF ROUTES =================

    @app.route("/admin/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        return render_template("admin_login.html", form=form)

    @app.route("/admin/dashboard")
    @login_required
    def admin_dashboard():
        # Saari enquiries nikal rahe hain (latest sabse upar)
        enquiries = Enquiry.query.order_by(Enquiry.date_submitted.desc()).all()
        return render_template("admin_dashboard.html", enquiries=enquiries)

    @app.route("/admin/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)