import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from forms import RegistrationForm, LoginForm
import os
import pyotp
import qrcode
import io
from base64 import b64encode

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match.')
            return render_template('register.html', title='Register', form=form)

        if not is_password_complex(form.password.data):
            flash('Password must be at least 8 characters long and include a lowercase, an uppercase, a number, and a special character.', category='error')
            return render_template('register.html', title='Register', form=form)

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already in use! Redirecting to the login screen.', category='error')
            return redirect(url_for('auth.login'))

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)

        if User.query.count() == 0:
            user.is_admin = True

        try:
            db.session.add(user)
            db.session.commit()
            session['pre_2fa_user_id'] = user.id
            flash('Registration successful. Please set up your OTP.', category='success')
            return redirect(url_for('auth.two_factor_setup'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred. Please try again. Error details: {e}', category='error')
            return render_template('register.html', title='Register', form=form)

    return render_template('register.html', title='Register', form=form)



def is_password_complex(password):
    """Check if the password is complex enough."""
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*()_+]", password):
        return False
    return True

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    form = LoginForm()
    otp_required = False
    if form.validate_on_submit():
        if not request.form.get('ipConsentCheckbox', False):
            flash('You must consent to IP logging to proceed.', category='error')
            return render_template('login.html', form=form, otp_required=otp_required)
        
        user = User.query.filter_by(email=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            if user.otp_verified:
                session['pre_2fa_user_id'] = user.id
                otp_required = True
            else:
                session['user_id'] = user.id
                session['username'] = user.username
                session['is_admin'] = user.is_admin
                return redirect(url_for('auth.profile'))
        else:
            flash('Invalid username or password', category='error')

    return render_template('login.html', form=form, otp_required=otp_required)



@auth.route('/two_factor_login', methods=['POST'])
def two_factor_login():
    user = User.query.get(session['pre_2fa_user_id'])
    data = request.get_json()
    otp = data.get('otp')
    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(otp) or totp.verify(otp, valid_window=1):
        session['user_id'] = user.id
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        session.pop('pre_2fa_user_id', None)
        return jsonify(success=True)
    return jsonify(success=False)


@auth.route('/two_factor_setup', methods=['GET', 'POST'])
def two_factor_setup():
    user = User.query.get(session['pre_2fa_user_id'])
    if user.otp_verified:
        flash('OTP already verified. Please log in.', category='success')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        otp = request.form['otp']
        totp = pyotp.TOTP(user.otp_secret)
        if totp.verify(otp) or totp.verify(otp, valid_window=1):
            user.otp_verified = True
            db.session.commit()
            session.pop('pre_2fa_user_id', None)
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('auth.profile'))
        flash('Invalid OTP', category='error')

    totp_uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(user.email, issuer_name="YourApp")
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf)
    img_b64 = b64encode(buf.getvalue()).decode('utf-8')
    return render_template('two_factor_setup.html', img_b64=img_b64, user=user)





@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    return render_template('index.html')


@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user is None:
        return "User not found", 404

    if request.method == 'POST':
        if 'current_password' in request.form and 'new_password' in request.form:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')

            if user and check_password_hash(user.password_hash, current_password):
                user.password_hash = generate_password_hash(new_password)
                db.session.commit()
                flash('Password successfully updated.', 'success')
            else:
                flash('Current password is incorrect.', 'error')

        if 'otp_action' in request.form:
            otp_action = request.form.get('otp_action')
            if otp_action == 'enable':
                user.otp_secret = pyotp.random_base32()
                user.otp_verified = False
                db.session.commit()
                session['pre_2fa_user_id'] = user.id
                return redirect(url_for('auth.two_factor_setup'))
            elif otp_action == 'disable':
                user.otp_secret = pyotp.random_base32()  # Reset the secret to a new random value
                user.otp_verified = False
                db.session.commit()
                flash('OTP has been disabled.', 'success')

    return render_template('profile.html', user=user)



@auth.route('/delete_profile', methods=['POST'])
def delete_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not found.', 'error')
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.login'))

    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('Your profile has been successfully deleted.', 'success')
    return redirect(url_for('index'))
