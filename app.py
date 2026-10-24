from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from config import Config
import data


class ContactForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(2, 80)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    phone = StringField("Phone (optional)", validators=[Length(0, 20)])
    interest = SelectField("Interested In", choices=[
        ("admissions", "Admissions"),
        ("programs",   "Programs & Curriculum"),
        ("placements", "Placements"),
        ("facilities", "Facilities"),
        ("other",      "Other"),
    ])
    message = TextAreaField("Message", validators=[DataRequired(), Length(10, 1000)])
    submit = SubmitField("Send Message")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.context_processor(lambda: {
        "INSTITUTE_NAME":    Config.INSTITUTE_NAME,
        "INSTITUTE_SHORT":   Config.INSTITUTE_SHORT,
        "INSTITUTE_YEARS":   2026 - Config.FOUNDED_YEAR,
        "ADDRESS":           Config.ADDRESS,
        "PHONE":             Config.PHONE,
        "EMAIL":             Config.EMAIL,
    })

    @app.route("/")
    def index():
        return render_template("index.html",
                               stats=data.STATS,
                               highlights=data.HIGHLIGHTS,
                               programs=data.PROGRAMS[:3],
                               facilities=data.FACILITIES[:6],
                               recruiters=data.RECRUITERS[:8])

    @app.route("/about")
    def about():
        return render_template("about.html", timeline=data.TIMELINE)

    @app.route("/courses")
    def courses():
        return render_template("courses.html", programs=data.PROGRAMS)

    @app.route("/facilities")
    def facilities():
        return render_template("facilities.html", facilities=data.FACILITIES)

    @app.route("/faculty")
    def faculty():
        return render_template("faculty.html", faculty=data.FACULTY)

    @app.route("/placements")
    def placements():
        return render_template("placements.html",
                               stats=data.PLACEMENT_STATS,
                               recruiters=data.RECRUITERS)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            # Production: persist to DB or dispatch email
            flash(f"Thank you, {form.name.data}! Our team will reach out within 24 hours.", "success")
            return redirect(url_for("contact"))
        return render_template("contact.html", form=form)

    @app.errorhandler(404)
    def not_found(_):
        return render_template("base.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)