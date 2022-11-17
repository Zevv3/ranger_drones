from flask import Blueprint, render_template, request, redirect, url_for, flash
from drone_inventory.models import User, db
from drone_inventory.forms import UserLoginForm
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST']) #always going to be a list and will always be methods
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data

            #Take info and put it into our database
            user = User(email, first_name = first_name, last_name = last_name, password = password)

            db.session.add(user)
            db.session.commit()

            # this is a flash message. First is the message, second is the category
            flash(f"You have succesfully created a user account {email}!", "user-created")

            #setting this to the homepage instead of sign in for testing purposes since signin 
            # is not set up yet
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            #sets the user to the user corresponding to that email in the database
            logged_user = User.query.filter(User.email == email).first()
            print(logged_user)
            if logged_user and check_password_hash(logged_user.password, password):
                print('hello')
                login_user(logged_user)
                flash('You were succesfully logged in via Email/Password!', 'auth-success')
                return redirect(url_for('site.profile'))

            else:
                flash("Your email or password is invalid.", 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid form data: Please try again, dawg")

    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))