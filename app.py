from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from config import Config
import data

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

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Context Processor (Makes variables available in all templates automatically)
    app.context_processor(lambda: {
        "INSTITUTE_NAME": "NICT COMPUTER",
        "TAGLINE": "TRAINING CENTER • JAMSHEDPUR",
        "MAIN_BRANCH": data.BRANCHES[0],
        "NEW_BRANCH": data.BRANCHES[1],
        "CONTACT_NUMBER": data.BRANCHES[0]['phone']
    })

    @app.route("/")
    def index():
        return render_template("index.html", 
                               stats=data.HERO_STATS, 
                               toppers=data.TOPPERS[:3],
                               courses=data.PROFESSIONAL_COURSES)

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

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            flash(f"Thank you {form.name.data}! Our team will call you shortly to confirm your discount.", "success")
            return redirect(url_for("contact"))
        return render_template("contact.html", form=form)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)