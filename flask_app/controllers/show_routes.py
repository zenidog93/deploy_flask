from flask_app import app   
from flask import render_template, request, redirect, session, flash

from flask_app.models import show_model
from flask_app.models import user_model
from flask_app.models import likes_model

@app.route('/shows/new')
def display_create_page():
    if 'user_id'  not in session:
        return redirect ('/')
    return render_template('display_create_new.html')

@app.route('/shows/create', methods = ['POST'])
def create_show():
    if 'user_id'  not in session:
        return redirect ('/')
    
    if not show_model.Show.validate_show(request.form):
        return redirect('/shows/new')
    
    shows_data = {
        **request.form,
        'user_id' :session['user_id']
    }
    show_model.Show.create_show(shows_data)
    
    return redirect('/shows')

@app.route('/shows/edit/<int:id>')
def display_shows_edit_page(id):
    if 'user_id'  not in session:
        return redirect ('/')
    temp_id = id
    show_data = {
        'id': temp_id
    }
    likes_data = {
        'show_id' : temp_id
    }
    
    data = {
        'id': session['user_id']
    }
    logged_user =user_model.User.get_one(data)
    
    this_shows_likes = likes_model.Like.get_num_of_likes_for_each_show(likes_data)
    
    
    this_show = show_model.Show.get_one_show_for_edit(show_data)
    return render_template('display_show_edit_page.html', this_show= this_show, this_shows_likes = this_shows_likes, logged_user = logged_user)

@app.route('/shows/<int:id>/edit', methods = ['POST'])
def update_show(id):
    if 'user_id'  not in session:
        return redirect ('/')
    if not show_model.Show.validate_show(request.form):
        return redirect(f'/shows/edit/{id}')
    show_data = {
        **request.form,
        'id' : id
    }
    show_model.Show.update_show(show_data)
    return redirect('/shows')

@app.route('/shows/<int:id>')
def display_one_show_page(id):
    if 'user_id'  not in session:
        return redirect ('/')
    temp_id = id
    show_data = {
        'id': temp_id
    }
    likes_data = {
        'show_id' : temp_id
    }
    data = {
        'id': session['user_id']
    }
    logged_user =user_model.User.get_one(data)
    
    this_shows_likes = likes_model.Like.get_num_of_likes_for_each_show(likes_data)
    
    this_show = show_model.Show.get_one_show_for_edit(show_data)
    return render_template('display_one_show_page.html', this_show= this_show, this_shows_likes = this_shows_likes, logged_user = logged_user)


@app.route('/create/like/<int:id>')
def create_like(id):
    if 'user_id'  not in session:
        return redirect ('/')
    liked_data = {
        'show_id' : id,
        'user_id': session['user_id']  
    }
    print(liked_data)
    likes_model.Like.create_a_like(liked_data)
    
    return  redirect('/shows')



@app.route('/delete/<int:id>')
def delete_show(id):
    if 'user_id'  not in session:
        return redirect ('/')
    show_model.Show.delete_show({'id': id })
    return redirect('/shows')