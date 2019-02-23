from __future__ import unicode_literals
import os
from flask import render_template, flash, redirect, url_for, request, make_response, jsonify
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
from siamsite import app, mail, db, bcrypt
from siamsite.forms import NewItem, Contact, Image, Login, NewAdmin
from siamsite.utils import Twitter, save_picture
from siamsite.models import MenuItem, User
from datetime import datetime
import json


@app.route("/", methods=['GET', 'POST'])
def index():

    # Year for copyright
    year = str(datetime.now().year)

    # Handling Twitter
    twitter_user_name = "o_succ"
    tweet = Twitter(twitter_user_name)
    handle = tweet.user
    text = tweet.text
    time = tweet.time_convert()

    # Handling image file names
    menu_image_list = []
    for root, dirs, files in os.walk('siamsite/static/img/menu/'):
        for filename in files:
            x = os.path.join('static/img/menu/', filename)
            menu_image_list.append(x)

    # Menu Items
    items = MenuItem.query.order_by(MenuItem.rank.asc())

    # Handling email contact form
    form = Contact()
    if request.method == 'POST':
        if form.validate_on_submit() is False:
            flash('Try Again. Make sure all fields are filled.')
        elif form.validate_on_submit() is True:
            msg = Message(form.subject.data, sender='customer@sianstreetfood.com', recipients=['customer@sianstreetfood.com'])
            msg.body = '''
            From: %s <%s>
            %s
            ''' % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            flash('Message sent successfully!')

    return render_template('index.html', title='Sian Street Food', form=form, year=year, items=items,
                           tweet_handle=handle, tweet_text=text, tweet_time=time, tweet_user=twitter_user_name,
                           image1=menu_image_list[0], image2=menu_image_list[1],
                           image3=menu_image_list[2], image4=menu_image_list[3])


@app.route("/login", methods=['GET', 'POST'])
def login():

    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    elif form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form, title='Admin Login')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():

    img_form = Image()
    if img_form.validate_on_submit():

        if img_form.img1.data:
            save_picture(img_form.img1.data, '1')

        if img_form.img2.data:
            save_picture(img_form.img2.data, '2')

        if img_form.img3.data:
            save_picture(img_form.img3.data, '3')

        if img_form.img4.data:
            save_picture(img_form.img4.data, '4')

        flash('You successfully uploaded and posted your image(s)!', 'success')

    new_form = NewAdmin()
    if new_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(new_form.password.data).decode('utf-8')
        email = new_form.email.data
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('New administrative account created', 'success')
        return redirect(url_for('admin'))

    return render_template('admin.html', title='Sian Street Food - Admin Page',
                           img_form=img_form, new_form=new_form)


@app.route("/working", methods=['GET', 'POST'])
def working():

    form = NewItem()
    if form.validate_on_submit():
        new_item = MenuItem(name=form.name.data,
                            description=form.description.data,
                            head=form.head.data,
                            spice=form.spice.data,
                            vegetarian=form.veg.data
                            )
        db.session.add(new_item)
        db.session.commit()
        flash('You successfully added a new menu item!', 'success')
        return redirect(url_for('working'))
    items = MenuItem.query.order_by(MenuItem.rank.asc())
    return render_template('working.html', form=form, items=items, title='Sian Street Food')


@app.route("/item/<int:item_id>/delete", methods=['GET', 'POST'])
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Your menu item has been deleted!', 'success')
    return redirect(url_for('working'))


@app.route("/post", methods=['POST'])
def post():

    id_array = request.get_json()
    print(id_array)
    res = make_response(jsonify({"so glad": "It worked"}), 200)

    list_rank = 1
    for id in id_array:

        item = MenuItem.query.get(id)
        item.rank = list_rank
        db.session.commit()
        print(item.name + " " + str(item.rank))
        list_rank += 1

    flash('You have succesfully re-ordered and posted the menu to the website!')

    full_menu = MenuItem.query.order_by(MenuItem.rank.desc())

    return res, render_template("post.html", x=full_menu)









