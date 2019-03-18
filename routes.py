from __future__ import unicode_literals
import os
from flask import render_template, flash, redirect, url_for, request, make_response, jsonify
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required
from siamsite import app, mail, db, bcrypt
from siamsite.forms import NewItem, Contact, Image, Login, NewAdmin, NewCaterItem, NewEvent, CaterOrder, AboutForm
from utils import Twitter, save_picture
from siamsite.models import MenuItem, User, CaterItem, EventItem, About
from datetime import datetime


@app.route("/", methods=['GET', 'POST'])
def index():

    # Year for copyright
    year = str(datetime.now().year)

    # Handling Twitter
    twitter_user_name = "sianstreetfood"
    tweet = Twitter(twitter_user_name)
    handle = tweet.user
    text = tweet.text
    time = tweet.time_convert()

    # Handling image file names
    menu_image_list = []
    for root, dirs, files in os.walk('siamsite/static/img/menu/'):
        for filename in files:
            x = os.path.join('siamsite/static/img/menu/', filename)
            menu_image_list.append(x)

    # Menu Items
    items = MenuItem.query.order_by(MenuItem.rank.asc())

    # Cater Menu Items
    cater_items = CaterItem.query.order_by(CaterItem.rank.asc())

    # Event Items
    event_items = EventItem.query.order_by(EventItem.date.asc())

    # About Us
    about = About.query.first()

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

    return render_template('index.html', title='Sian Street Food', form=form, year=year, items=items, about=about,
                           tweet_handle=handle, tweet_text=text, tweet_time=time, tweet_user=twitter_user_name,
                           image1=menu_image_list[0], image2=menu_image_list[1],
                           image3=menu_image_list[2], image4=menu_image_list[3],
                           event_items=event_items, cater_items=cater_items
                           )

@app.route("/booking", methods=['GET', 'POST'])
def booking():

    event_items = EventItem.query.order_by(EventItem.date.asc())

    form = CaterOrder()
    if request.method == 'POST':
        if form.validate_on_submit() is False:
            flash('Try Again. Make sure all fields are filled.')
        if form.validate_on_submit() is True:
            subject = "New catering order from " + form.customer_first.data + "!"
            msg = Message(subject=subject, sender='booking@sianstreetfood.com', recipients=['customer@sianstreetfood.com'])
            msg.body = '''
            From: %s %s
            Contact Info: <%s> %s
            Event Date: %s
            Time: %s - %s
            Guest Count: %s
            Location: %s
            
            Additional Info: %s
            
            ''' % (form.customer_first.data, form.customer_last.data, form.email.data, form.phone.data, form.date.data,
                   form.start_time.data, form.end_time.data, form.guest_count.data, form.location.data, form.info.data)

            mail.send(msg)
            flash('Email sent successfully, expect a reply shortly.')
            return redirect(url_for('index'))

    return render_template('booking.html', title='Catering Booking - Sian Street Food', form=form, event_items=event_items)


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

    menu_form = NewItem()
    if menu_form.validate_on_submit():
        new_item = MenuItem(name=menu_form.name.data,
                            description=menu_form.description.data,
                            head=menu_form.head.data,
                            spice=menu_form.spice.data,
                            vegetarian=menu_form.veg.data
                            )
        db.session.add(new_item)
        db.session.commit()
        flash('You successfully added a new menu item!', 'success')
        return redirect(url_for('admin'))

    items = MenuItem.query.order_by(MenuItem.rank.asc())

    return render_template('admin.html', title='Manage Menu - SSF Admin',
                           menu_form=menu_form, items=items)


@app.route("/admin/about", methods=['GET', 'POST'])
@login_required
def about():
    form = AboutForm()
    if form.validate_on_submit():

        old = About.query.first()
        if old:
            db.session.delete(old)

        new_item = About(text=form.about.data)
        db.session.add(new_item)
        db.session.commit()
        flash('About Us section successfully updated', 'success')
        return redirect(url_for('about'))

    about = About.query.all()

    return render_template('about.html', title='Manage About Us - SSF Admin', form=form, about=about)

@app.route("/admin/catering", methods=['GET', 'POST'])
@login_required
def cater_menu():

    cater_form = NewCaterItem()
    if cater_form.validate_on_submit():
        cater_item = CaterItem(name=cater_form.name.data,
                               description=cater_form.description.data,
                               whole=cater_form.whole.data,
                               half=cater_form.half.data,
                               head=cater_form.head.data,
                               spice=cater_form.spice.data,
                               vegetarian=cater_form.veg.data)
        db.session.add(cater_item)
        db.session.commit()
        flash('You successfully added a new catering menu item!', 'success')
        return redirect(url_for('cater_menu'))

    cater_items = CaterItem.query.order_by(CaterItem.rank.asc())

    return render_template('cater.html', title='Manage Catering Menu - SSF Admin',
                           cater_form=cater_form, cater_items=cater_items)


@app.route("/admin/event", methods=['GET', 'POST'])
@login_required
def new_event():

    event_form = NewEvent()
    if event_form.validate_on_submit():
        event_item = EventItem(name=event_form.name.data,
                               location=event_form.location.data,
                               description=event_form.description.data,
                               date=event_form.date.data,
                               start_time=event_form.start_time.data,
                               end_time=event_form.end_time.data)
        db.session.add(event_item)
        db.session.commit()
        flash('You successfully added a new event!', 'success')
        return redirect(url_for('new_event'))

    event_items = EventItem.query.order_by(EventItem.date.asc())

    return render_template('event.html', title='Manage Events - SSF Admin',
                           event_form=event_form, event_items=event_items)


@app.route("/admin/image_uploader", methods=['GET', 'POST'])
@login_required
def image_uploader():

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

    return render_template('image_uploader.html', title='Manage Images - SSF Admin',
                           img_form=img_form)


@app.route("/admin/new_admin", methods=['GET', 'POST'])
@login_required
def new_admin():

    new_form = NewAdmin()
    if new_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(new_form.password.data).decode('utf-8')
        email = new_form.email.data
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('New administrative account created', 'success')
        return redirect(url_for('new_admin'))

    return render_template('new_admin.html', title='Manage Admins - SSF Admin',
                           new_form=new_form)


@app.route("/item/<int:item_id>/<table>/<location>/delete", methods=['GET', 'POST'])
def delete_item(item_id, table, location):

    if table == 'MenuItem':
        item = MenuItem.query.get_or_404(item_id)
    elif table == 'CaterItem':
        item = CaterItem.query.get_or_404(item_id)
    elif table == 'EventItem':
        item = EventItem.query.get_or_404(item_id)
    else:
        flash('Delete failed, try again', 'danger')
        return redirect(url_for(location))

    db.session.delete(item)
    db.session.commit()
    flash('Your menu item has been deleted!', 'success')
    return redirect(url_for(location))


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

    return res

@app.route("/cater_post", methods=['POST'])
def cater_post():

    id_array = request.get_json()
    print(id_array)
    res = make_response(jsonify({"so glad": "It worked"}), 200)

    list_rank = 1
    for id in id_array:

        item = CaterItem.query.get(id)
        item.rank = list_rank
        db.session.commit()
        print(item.name + " " + str(item.rank))
        list_rank += 1

    flash('You have succesfully re-ordered and posted the menu to the website!')

    return res








