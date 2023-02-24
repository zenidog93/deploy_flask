from flask_app import app   
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user_model import User
from flask_app.models.show_model import Show
from flask_app.models import likes_model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user/create', methods =['POST'])
def register_user():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    #1 has the passwords
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # get the data dictionary ready with the new hashed password to create a User
    data = {
        **request.form,
        'password' :pw_hash
    }
    #3 pass it to the user model
    user_id = User.create_user(data)
    
    #4 we store the user_id in session to keep track of the which user is currently logged in. 
    session['user_id'] = user_id
    return redirect ('/shows')


#log in method- The action where we will be redirected
@app.route ("/user/login", methods=['POST'])
def user_login():
    data = {
        'email' : request.form['email']
    }
    
    user_in_db = User.get_one_by_email(data) ## returns false or a user
    
    # if email not found
    if not user_in_db:
        flash("Email or password are invalid")
        return redirect('/')
    
    #check to make sure the password matches with its email
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    
    return redirect('/shows')


# renders dashboard after logging in
@app.route('/shows')
def display_dash():
    if 'user_id'  not in session:
        return redirect ('/')
    
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_one(data)
    
    likes_data = {
        'user_id' :session['user_id']
    }
    
    user_likes = likes_model.Like.get_all_likes(likes_data)
    print('\n\n\n====??', user_likes)
    all_shows = Show.get_all_shows()
    
    return render_template("shows.html", logged_user = logged_user, all_shows = all_shows, user_likes = user_likes)


#log out - action route
@app.route('/logout')
def logout():
    if 'user_id'  not in session:
        return redirect ('/')
    session.clear()
    return redirect('/')