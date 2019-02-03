from . import db, mail
from app import app
from flask import render_template, url_for, flash, redirect, request, session, abort
from forms import RegistrationForm, LoginForm, SearchForm, BookForm, RequestForgetPasswordForm, ResetPasswordForm, UpdateProductForm
from forms import AdminLogin
from models import User, Product, Order, Admin
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from sqlalchemy.sql.functions import func
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import  Message
import os
from threading import Thread
from sqlalchemy import or_

def async_email(app, message):
    with app.app_context():
        mail.send(message)

def send_email(app,message):
    thread = Thread(target=async_email, args=[app, message])
    thread.start()
    return thread

def get_num_items():
    try:
        items = len(session['items'])
    except KeyError:
        items = 0
    return items

#__________________________________________ MAIN SITE ___________________________________________________________________    


@app.route('/store')
def index():
    form1 = LoginForm()
    products = Product.query.all()
    return render_template('index.html', title='PyraSpace', products=products,form1=form1, items_in_cart=get_num_items())

@app.route('/books')
def books():
    products = Product.query.filter_by(category='Books').all()
    return render_template('index.html', title='PyraSpace', products=products, items_in_cart=get_num_items())

@app.route('/electronics')
def electronics():
    products = Product.query.filter_by(category='Electronics').all()
    return render_template('index.html', title='PyraSpace', products=products, items_in_cart=get_num_items())
@app.route('/other')
def other():
    products = Product.query.filter_by(category='Other').all()
    return render_template('index.html', title='PyraSpace', products=products, items_in_cart=get_num_items())

@app.route('/search', methods=['GET', 'POST'])
def search(search_input=None):
    if request.args.get('search_input'):
        search_input = request.args.get('search_input')
    search_query = search_input
    products = Product.query.filter(or_(Product.title.like("%{}%".format(search_query)), Product.code.like("%{}%".format(search_query)))).all()
    try:
        items = len(session['items'])
    except KeyError:
        items = 0
    if products:
        show_number = True
        return render_template('index.html', title='PyraSpace', products=products, show_number=show_number,
                               items_in_cart=items)

    products = Product.query.filter(Product.code.like("%{}%".format(search_query))).all()
    if products:
        show_number = True
        return render_template('index.html', title='PyraSpace', products=products,
                               show_number=show_number,
                               items_in_cart=items)
    products = Product.query.all()
    for product in products:
        temp_code = product.code.replace(" ","")
        temp_product  = Product.query.filter(Product.code.like("%{}%".format(temp_code))).all()
        if temp_product:
            show_number = True
            return render_template('index.html', title='PyraSpace', products=products,
                                   show_number=show_number,
                                   items_in_cart=items)

    flash('No item found.')
    return render_template('index.html', title='PyraSpace', products=products,items_in_cart=items)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    form1 = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None:
            flash('Email already registered.')
            return redirect(url_for('register'))
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data.lower(), phone_number=form.phone_number.data, rating=0)
        user.password_hash = user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully Registered!')
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).decode_netloc() != '':
            next_page = url_for('index')
        return redirect(next_page)

    if form1.validate_on_submit():
        user = User.query.filter_by(email=form1.email.data.lower()).first()
        if user is None or not user.check_password(form1.password.data):
            flash('Invalid Email or Password')
            return redirect(url_for('register'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Sign Up | Sign In', form=form, form1=form1)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('register'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', items_in_cart=get_num_items())

def correct_file_type(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ['png', 'jpg', 'jpeg']

@app.route('/profile/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = BookForm()
    if form.validate_on_submit():
        file = form.image.data
        if file and correct_file_type(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join('app/static/images', filename)
            file.save(path)
            product = Product(title=form.title.data, description=form.description.data, price=form.price.data, code=form.module_code.data,
                              category=form.category.data, status='available', image_link=path,
                              user_id=current_user.id, ad_fee_paid='No', location=form.location.data)
            db.session.add(product)
            db.session.commit()
            flash('Item Successfully Added!')
            return redirect(url_for('index'))
        else:
            flash('Incorrect File Type. Only .png, .jpg and .jpeg allowed.')
            return render_template('profile.html', title='Profile', form=form, page='add_item')
    return render_template('profile.html', title='Profile', form=form, page='add_item', items_in_cart=get_num_items())


@app.route('/profile/manage_items', methods=['GET', 'POST'])
@login_required
def manage_items():
    products = Product.query.filter_by(user_id=current_user.id).all()
    update_form = UpdateProductForm()
    data = {'merchant_id' : '13457516', 'merchant_key':'hvy51mk1svng8',
            'return_url' : 'https://www.pyraspace.com/return', 'cancel_url': 'https://www.pyraspace.com/cancel',
            'notify_url' : 'https://www.pyraspace.com/notify/', 'm_payment_id': 'O1AB', 'amount':'10.00',
            'item_name': 'PyraSpace Ad Fee', 'item_descriptiom': 'Ad Fee'}
    try:
        product = Product.query.filter_by(id=session['id']).first()
        if update_form.is_submitted():
            product = Product.query.filter_by(id=session['id']).first()
            temp_title = product.title
            temp_descr = product.description
            temp_price = product.price
            if len(update_form.title.data) is not 0 and update_form.title.data != temp_title:
                product.title = update_form.title.data
            else:
                product.title = temp_title
            if len(update_form.description.data) is not 0:
                product.description = update_form.description.data
            else:
                product.description = temp_descr
            if update_form.price.data  is not None:
                product.price = update_form.price.data
            else:
                product.price = temp_price
            db.session.commit()
            return redirect(url_for('manage_items'))
        return render_template('profile.html', title='Profile', page='manage_items', products=products,
                               update_form=update_form,items_in_cart=get_num_items())

    except KeyError:
        return render_template('profile.html', title='Profile', page='manage_items', products=products, update_form=update_form, items_in_cart=get_num_items())

@app.route('/profile/purchases', methods=['GET', 'POST'])
@login_required
def purchases():
    products = Order.query.filter_by(buyer_id=current_user.id).all()
    return render_template('profile.html', title='My Purchases', page='purchases', products=products,items_in_cart=get_num_items())

@app.route('/profile/incoming_orders')
@login_required
def incoming_orders():
    products = Order.query.filter_by(seller_id=current_user.id).all()
    return render_template('profile.html', title='My Purchases', page='incoming_orders', products=products, items_in_cart=get_num_items())

@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    session['id'] = request.args.get('id')
    return str(request.args.get('id'))

@app.route('/mark_sold', methods=['GET', 'POST'])
@login_required
def mark_sold():
    id = session.get('sold_id')
    item = Product.query.filter_by(id=id).first()
    if item is not None:
        item.status = 'sold'
        db.session.commit()
        flash('Sold {}!'.format(item.title))
        #return redirect(url_for('manage_items'))
    return str(id)

@app.route('/set_id', methods=['GET', 'POST'])
@login_required
def set_id():
    session['sold_id'] = request.args.get('sold_id')
    return session['sold_id']
@app.route('/profile/profile_landing')
@login_required
def profile_landing():
    total = Product.query.filter_by(user_id=current_user.id).count()
    available = Product.query.filter_by(user_id=current_user.id, status='available').count()
    expected = db.session.query(func.sum(Product.price).label('Sum')).filter_by(user_id=current_user.id, status='available').scalar()
    current = db.session.query(func.sum(Product.price).label('Sum')).filter_by(user_id=current_user.id, status='sold').scalar()
    return render_template('profile.html', title='Profile', page='profile_landing', total=total, available=available,
                           expected=expected, current=current, items_in_cart=get_num_items())

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form1 = RegistrationForm()
    form2 = LoginForm()
    form = RequestForgetPasswordForm()
    if form.validate_on_submit():
        message = True
        serializer = URLSafeTimedSerializer('asdfghjkl')
        token = serializer.dumps(form.email.data)
        user = User.query.filter_by(email=form.email.data)
        user.token = token
        db.session.commit()
        link = 'https://pyraspace.com'
        link += url_for('reset_password', token=token)
        msg = Message('Reset Password | PyraSpace.com', sender='orifha360@gmail.com', recipients=[form.email.data], body=link)
        with app.app_context():
            mail.send(msg)
            flash('Please check your email for instructions to reset your password.')
            return render_template('register.html', title='Sign Up | Sign In', form=form1, form1=form2)
    return render_template('forgot_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    serializer = URLSafeTimedSerializer('asdfghjkl')
    try:
        email = serializer.loads(token, 86400)
    except SignatureExpired:
        return 'Token Expired'
    user = User.query.filter_by(email=email).first()
    if user:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.password_hash = user.hash_password(form.new_password.data)
            db.session.commit()
            flash('Password Changed!')
            return redirect(url_for('register'))
        return render_template('reset_password.html', form=form)
    return 'Password Reset Link Expired'

@app.route('/add_to_cart')
def add_to_cart():
     if  not current_user.is_authenticated:
         flash('You must log in to perform that action.')
         return str('login')
     try: session['items']
     except KeyError:
         session['items'] = []
         session['items'].append(request.args.get('id'))
         return session['items'][0]
     items = session['items']
     if request.args.get(str('id')) not in session['items']:
        items.append(request.args.get(str('id')))
        session['items'] = items
        item = ''
        j = 0
        for i in session['items']:
            if j != 0:
                item += ',' + i
            else:
                item += i
            j+=1
        return item
     else:
         flash('Item already in basket!')
         return 'Already in cart.'

@app.route('/item/<id>')
def item(id):
    item = Product.query.filter_by(id=id).first()
    if item is None:
        return render_template('item.html', error=True, title='Item Not Found', items_in_cart=get_num_items())

    return render_template('item.html', product=item, title=item.title, items_in_cart=get_num_items())

@app.route('/cart')
@login_required
def cart():
    string = ''
    try:
        items = session['items']
        num = len(items)
    except KeyError:
        flash('No items in Basket')
        return redirect(url_for('index'))
    if len(session['items']) is 0:
        flash('No items in Basket')
        return redirect(url_for('index'))
    items = session['items']
    db_items = Product.query.filter(Product.id.in_(items)).all()
    total = db.session.query(func.sum(Product.price).label('Sum')).filter(Product.id.in_(items)).scalar()
    return render_template('cart.html', products=db_items, total=total, items_in_cart = len(items), title='Basket | PyraSpace')

@app.route('/remove_item')
def remove_item():
    id = request.args.get('id')
    items = session['items']
    items.remove(id)
    session['items'] = items
    return ''

@app.route('/confirm_order')
def confirm_order():
    if len(session['items']) is 0:
        flash('Cart is empty.')
        return redirect(url_for('index'))
    for i in session['items']:
        product = Product.query.filter_by(id=i).first()
        product.status = 'sold'
        user = User.query.filter_by(id=product.user_id).first()
        order = Order(product_id=product.id, title=product.title,description=product.description,
                      price=product.price, category=product.category, image_link=product.image_link, status='not_fulfiled',
                      buyer_id=current_user.id, seller_id=product.user_id, ad_fee_paid='No')
        db.session.add(order)
        db.session.commit()
        body = 'Hi, {}!<br><br> You have found a buyer for the following item.<br><hr>{}<br>'.format(user.first_name,
                                                                                                     product.title)
        if product.ad_fee_paid == 'No':
            fees = '<br>Since you have an outstanding balance of R10 on this ad, please settle as soon as possible to be' \
                   ' able to interact with your buyer. Please note this is a once off fee. Once settled, you will be able to ' \
                   'interact with unlimited number of buyers for the item.'
        else:
            fees = '<br>Please find your buyer\'s info below.<br>First Name: {}<br>Last Name: {}<br>' \
                   'Email: {}<br>'.format(current_user.first_name, current_user.last_name, current_user.email)
        body += fees
        msg = Message('You\'ve got a buyer! | PyraSpace.com', sender='orders@pyraspace.com', recipients=[user.email],
                      html=body)
        send_email(app, msg)
    session.pop('items')
    flash('Order Successfully Placed! Please check your email ({}) for our email.'.format(current_user.email))
    return redirect(url_for('index'))

@app.route('/notify/', methods=['POST', 'GET'])
def notify():
    SANDBOX_MODE = True
    if SANDBOX_MODE:
        host = 'sandbox.payfast.co.za'
    else:
        host = 'www.payfast.co.za'
    if request.method == 'POST':
        if request.values.get('payment_status') == 'COMPLETE':
            p_id = request.values.get('custom_int1')
            product = Product.query.filter_by(id=p_id).first()
            product.ad_fee_paid = 'Yes'
            db.session.commit()
            user = request.values.get('custom_int2')
            body = 'Hi, {}!<br><br> You have found a buyer for the following item.<br><hr>{}<br>'.format(
                user.first_name, product.title)
            fees = '<br>Please find your buyer\'s info below.<br>First Name: {}<br>Last Name: {}<br>' \
                   'Email: {}<br>'.format(current_user.first_name, current_user.last_name, current_user.email)
            body += fees
            msg = Message('You\'ve got a buyer! | PyraSpace.com', sender='orders@pyraspace.com', recipients=[user.email],
                          html=body)
            send_email(msg)
            return product.ad_fee_paid
        else:
            return 0
    else:
        return 'Method'
@app.route('/contact')
def contact():
    return render_template('contact_us.html')

@app.route('/', methods=['POST', 'GET'])
def landing():
    return render_template('landing.html', title='Introducing PyraSpace.com')
#_________________________________________ END MAIN SITE _________________________________________________________#
#_________________________________________ ADMIN SITE ____________________________________________________________#

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    form = AdminLogin()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user.password == form.password.data:
            return redirect(url_for('admin_home'))
    return render_template('admin_login.html', form=form, title = 'PyraSpace | Admin')


@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html', title = 'PyraSpace Admin')







@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', items_in_cart=get_num_items(), title = 'Page Not Found')

@app.errorhandler(500)
def error_500(error):
    message = Message(subject='Server Error',sender=['orders@pyraspace.com'], recipients=['support@pyraspace.com'],
                      body=error)
    send_email(app, message)
    return render_template('404.html', items_in_cart=get_num_items(), title='Server Error')

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

