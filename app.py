"""Flask feedback application."""

from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, Feedback, User
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost:5433/feedbacks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
with app.app_context():
    connect_db(app)
    db.create_all()



@app.route('/')
def home_page():
    return redirect("/register")


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Display form to register new user and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        """Return the user registration in the order {username, password, first_name, last_name, email}"""

        user = User.register(username, password, first_name, last_name, email)

        db.session.add(user.username)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)

            session['username'] = user.username
            flash('Welcome! Successfully Created Your Account!', "success")
            return redirect(f"/users/{user.username}")

    return render_template("register.html", form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Display login form."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("login.html", form=form)


@app.route('/logout')
def logout_user():
    """Logout route."""

    session.pop("username")
    flash("Goodbye!", "info")
    return redirect("/login")


@app.route('/users/<username>')
def show_user(username):
    """Display page for logged-in-users."""

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect("/login")

        user = User.query.get(username)
        form = DeleteForm()
        db.session.add(new_username)
        db.session.commit()
        flash('Accepted!', 'success')

    return render_template("show.html", user=user, form=form)



@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete user and redirect to login page."""

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect("/login")

        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

    return redirect("/login")



@app.route('/users/<username>/feedback/new', methods=['GET', 'POST'])
def add_new_feedback(username):
    """Display new-feedback form and handle process."""

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect("/login")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("new.html", form=form)



@app.route('/feedback/<int:feedback_id>/edit', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """Display edit-feedback form and handle process."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("Please login first!", "danger")
        return redirect("/login")

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("edit.html", form=form, feedback=feedback)



@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash("Please login first!", "danger")
        return redirect("/login")

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")












