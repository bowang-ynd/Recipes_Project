from flask import render_template, request, redirect, flash, session
from flask_app import app, bcrypt

from flask_app.models.user_model import User


#?  landing page, redirect to register and login
@app.route('/')
def landing_page():
    # checks if uid exists in session
    if 'uid' in session:
        return redirect('/recipes')
    return redirect('/register_and_login')

#? ==================== REGISTER and LOGIN ====================
#* render the login and register html page 
@app.route('/register_and_login')
def register_and_login():
    return render_template('/login_and_register.html')

#* takes user's input of register info, checks if register info is valid
@app.route('/register', methods=['POST'])
def register():
    # checks if the user has inputed valid registration info
    if not User.validate_register(request.form):
        return redirect('/register_and_login')

    # if user has valid registration info, register the user in the database
    data = {
        **request.form,
        'password' : bcrypt.generate_password_hash(request.form['password']),
    }

    User.register(data)
    session['uid'] = User.get_by_email(data).id
    return redirect('/recipes')

#* takes user's input of login info, checks if login info is valid
@app.route('/login', methods=['POST'])
def login():
    # checks if the user has inputed valid login info
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }

    logged_in_user = User.validate_login(data)

    if not logged_in_user:
        return redirect('/register_and_login')
    
    # if the user has valid login info, login the user and redirect the dashboard
    session['uid'] = logged_in_user.id

    return redirect('/recipes')


#? ========== LOGOUT ==========
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


