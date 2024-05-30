from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request, session, jsonify
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import setuptools
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, IncomingForm, OutgoingForm
from flask_migrate import Migrate
import pymysql
import zipfile
import os
import requests
import json
from restcountries import RestCountryApiV2 as rapi

# flask setup
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')

# html setup
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# CONNECT TO DB
username = "root" #Your username
password = "EmeR2023" #Your password
host = "localhost"
port = 3306
database = "dbms_project" #Your database name
connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif','zip'}


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blogpost"
    blogpost_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    upload_date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)
    author_id = db.Column(db.String(250),db.ForeignKey('user.user_id'), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    img_folder = db.Column(db.String(250), nullable=True)
    comments = db.relationship("Comment",backref="post",cascade='all, delete')
    reacts = db.relationship("React", backref="post",cascade='all, delete')
    tagged = db.relationship("Tagged_user", backref="post",cascade='all, delete')

class User(UserMixin, db.Model):
    def get_id(self):
           return (self.user_id)
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    profile_img_url = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    posts = db.relationship("BlogPost", backref="author",cascade='all, delete')
    comments = db.relationship("Comment",backref="user",cascade='all, delete')
    reacts = db.relationship("React", backref="user",cascade='all, delete')
    tagged = db.relationship("Tagged_user", backref="user",cascade='all, delete')


class Comment(db.Model):
    __tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blogpost.blogpost_id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(250), db.ForeignKey('user.user_id'), nullable=False)
    comment_time = db.Column(db.String(250), nullable=False)

class Incoming_user(db.Model):
    __tablename__ = "incoming_user"
    incoming_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    origin_school = db.Column(db.String(250),nullable = False)
    continent = db.Column(db.String(250),nullable = False)
    country = db.Column(db.String(250),nullable = False)
    region = db.Column(db.String(250),nullable = True)
    info = db.Column(db.Text, nullable=True)


class Outgoing_user(db.Model):
    __tablename__ = "outgoing_user"
    outgoing_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    exchanging_school = db.Column(db.String(250),nullable = False)
    continent = db.Column(db.String(250),nullable = False)
    country = db.Column(db.String(250),nullable = False)
    region = db.Column(db.String(250),nullable = True)
    info = db.Column(db.Text, nullable=True)

class React(db.Model):
    __tablename__ = "react"
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blogpost.blogpost_id'), primary_key=True)

class Tagged_user(db.Model):
    __tablename__ = "tagged_user"
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blogpost.blogpost_id'), primary_key=True)

with app.app_context():
    db.create_all()

#define functions

def is_post_author(post_id):
    query = BlogPost.query.filter_by(blogpost_id=post_id).first()
    if query.author_id == current_user.get_id():
        return True
    else:
        return False
    
def is_profile_user(user_id):
    query = User.query.filter_by(user_id=user_id).first()
    if query.user_id == current_user.get_id():
        return True
    else:
        return False
    
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        email = form.data['email']
        user_id = form.data['id']
        #confirm password
        if form.data['password'] != form.data['confirm_password']:
            flash("Passwords do not match", "danger")
            error = "Passwords do not match"
        password = generate_password_hash(form.data['password'], method='pbkdf2:sha256', salt_length=8)
        
        # checking if email is already in database
        result = db.session.execute(db.select(User).where(User.email == email))
        existing_userEmail = result.scalar()
        if existing_userEmail:
            flash("This email already exists", "danger")
            error = "This email already exists"
        else:
            result = db.session.execute(db.select(User).where(User.user_id == user_id))
            existing_userID = result.scalar()
            if existing_userID:
                flash("This ID already exists", "danger")
                error = "This ID already exists"

        if not error:
            # Save the uploaded image to the server
            img_file = form.img_url.data
            if img_file and allowed_file(img_file.filename):
                filename = secure_filename(img_file.filename)
                img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img_url = filename
            else:
                img_url = None

            # Store user data in session instead of committing to the database
            session['user_data'] = {
                'user_id': user_id,
                'user_name': form.data['name'],
                'email': email,
                'password': password,
                'profile_img_url': img_url,
                'student_type': form.student_type.data
            }

            # Redirect based on student type
            if form.student_type.data == 'incoming':
                return redirect(url_for('incoming'))
            else:
                return redirect(url_for('outgoing'))

    return render_template("register.html", form=form)

@app.route('/register/incoming', methods=["GET", "POST"])
def incoming():
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for('register'))

    form = IncomingForm()
    if form.validate_on_submit():
        country = form.data['country']
        if not country:
            flash("Please Select a Country", "danger")
        else:
            # Use a transaction to ensure data consistency
            try:
                with db.session.begin_nested():
                    new_user = User(
                        user_id=user_data['user_id'],
                        user_name=user_data['user_name'],
                        email=user_data['email'],
                        password=user_data['password'],
                        profile_img_url=user_data['profile_img_url']
                    )
                    db.session.add(new_user)
                    db.session.flush()  # Flush to assign the user_id

                    new_incominguser = Incoming_user(
                        incoming_user_id=user_data['user_id'],
                        origin_school=form.data['origin_school'],
                        continent=form.data['continent'],
                        country=country,
                        region=form.data['region'],
                        info=form.data['info']
                    )
                    db.session.add(new_incominguser)

                db.session.commit()
                session.pop('user_data', None)
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred: " + str(e), "danger")

    return render_template("register_stage2.html", is_out=False, form=form, user_id=user_data['user_id'])

@app.route('/register/outgoing', methods=["GET", "POST"])
def outgoing():
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for('register'))

    form = OutgoingForm()
    if form.validate_on_submit():
        country = form.data['country']
        if not country:
            flash("Please Select a Country", "danger")
        else:
            # Use a transaction to ensure data consistency
            try:
                with db.session.begin_nested():
                    new_user = User(
                        user_id=user_data['user_id'],
                        user_name=user_data['user_name'],
                        email=user_data['email'],
                        password=user_data['password'],
                        profile_img_url=user_data['profile_img_url']
                    )
                    db.session.add(new_user)
                    db.session.flush()  # Flush to assign the user_id

                    new_outgoinguser = Outgoing_user(
                        outgoing_user_id=user_data['user_id'],
                        exchanging_school=form.data['exchanging_school'],
                        continent=form.data['continent'],
                        country=country,
                        region=form.data['region'],
                        info = form.data['info']
                    )
                    db.session.add(new_outgoinguser)

                db.session.commit()
                session.pop('user_data', None)
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred: " + str(e), "danger")

    return render_template("register_stage2.html", is_out=True, form=form, user_id=user_data['user_id'])
    
# @app.route('/get_countries/<region>', methods=['GET'])
# def get_countries(region):
#     try:
#         countries = rapi.get_countries_by_region(region)
#         country_list = [{'name': country['name']} for country in countries]
#         return jsonify(country_list)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/login', methods=["GET", "POST"])
def login():
    error = request.args.get('error')
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.data['id']
        password = form.data['password']

        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.user_id == user_id))
        user = result.scalar()
        if not user:
            error = "ID not found. If you don't have an account, register instead."
        elif not check_password_hash(user.password, password):
            error = 'Wrong password, please try again'
        else:
            login_user(user)
            flash('login successfully! Welocme, '+user.user_name)
            return redirect(url_for('get_all_posts'))
    print(error)
    return render_template("login.html", error=error, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('logout successfully')
    return redirect(url_for('get_all_posts'))

@app.route('/')
def get_all_posts():
    if not current_user.is_authenticated:
        isLogin = False
    else:
        isLogin = True
    result = db.session.execute(db.select(BlogPost).order_by(desc(BlogPost.views)))
    popular_posts = result.scalars().all()
    result2 = db.session.execute(db.select(BlogPost).filter_by(author_id = 1))
    exchange_informations = result2.scalars().all()
    # Check if there are any posts
    if len(popular_posts) == 0:
        # If no posts are available, render a template indicating that there are no posts.
        return render_template("no_posts.html")
    return render_template("index.html", isLogin=isLogin, popular_posts=popular_posts, exchange_informations=exchange_informations)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    tagged_users = Tagged_user.query.filter_by(post_id=post_id).all()
    tagged_users_data = [{"id": user.user_id, "name": user.user.user_name} for user in tagged_users]

    if not current_user.is_authenticated:
        is_like = False
    else:
        like = React.query.filter_by(user_id=current_user.get_id(), post_id=post_id).first()
        if not like:
            is_like = False
        else:
            is_like = True

    requested_post = db.get_or_404(BlogPost, post_id)
    requested_post.views += 1
    db.session.commit()
    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login to comment on a post.")
            return redirect(url_for("show_post", post_id=post_id))
        else:
            new_comment = Comment(
                comment=form.data['comment'],
                post_id=requested_post.blogpost_id,
                user_id=current_user.user_id,
                comment_time=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("show_post", post_id=post_id))

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.comment_id.desc()).all()
    image_files = []

    if requested_post.img_folder:
        img_folder_path = requested_post.img_folder
        # Get list of directory names (gallery names) in the img_folder_path
        gallery_names = os.listdir(img_folder_path)

        # Iterate over each gallery and get the list of filenames within each gallery
        for gallery_name in gallery_names:
            gallery_path = os.path.join(img_folder_path, gallery_name)
            if os.path.isdir(gallery_path):
                filenames = os.listdir(gallery_path)
                # Extend the image_files list with filenames within this gallery
                image_files.extend(filenames)

    return render_template("post.html", post=requested_post, form=form,
                           all_comments=comments, image_files=image_files, post_id=str(post_id), is_author = is_post_author(post_id),
                           tagged_users = tagged_users_data, is_like=is_like)

@app.route("/like/<int:post_id>")
def like_post(post_id):
    if not current_user.is_authenticated:
        flash("You need to login to like a post.")
        return redirect(url_for("show_post", post_id=post_id))
    like = React.query.filter_by(user_id=current_user.user_id, post_id=post_id).first()
    if not like:
        new_like = React(user_id=current_user.user_id, post_id=post_id)
        db.session.add(new_like)
    else:
        db.session.delete(like)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))

@app.route("/new-post", methods=["GET", "POST"])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        # Save uploaded folder to server
        images_folder = form.images_folder.data
        if images_folder:
            # Ensure that the uploaded file has a valid extension
            if not allowed_file(images_folder.filename):
                flash("File does not have an approved extension.")
                return redirect(url_for("add_new_post"))

            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(images_folder.filename))
            images_folder.save(folder_path)
            # Extract the uploaded zip file
            extract_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted')
            os.makedirs(extract_folder, exist_ok=True)  # Create folder if not exists
            try:
                with zipfile.ZipFile(folder_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
            except zipfile.BadZipFile:
                flash('Error: Uploaded file is not a valid zip file.')
                os.remove(folder_path)  # Remove the uploaded zip file
                return redirect(url_for("add_new_post"))
            image_files = os.listdir(extract_folder)
        else:
            extract_folder = None
            image_files = []

        new_post = BlogPost(
            title=form.title.data,
            upload_date=date.today().strftime("%B %d, %Y"),
            body=form.body.data,
            img_url=form.img_url.data,
            img_folder=extract_folder,  # Set the extracted folder path
            author_id=current_user.user_id,
            views=0
        )
        db.session.add(new_post)
        db.session.commit()

        post_id = new_post.blogpost_id
        tagged_users_data = request.form.get('tagged_users_data')
        if tagged_users_data:
            tagged_users = json.loads(tagged_users_data)
            for user in tagged_users:
                tagged_user = Tagged_user(user_id=int(user['id']), post_id=post_id)
                db.session.add(tagged_user)
        
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    
    return render_template("make-post.html", form=form,is_edit = False)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if not is_post_author(post_id):
        flash("You are not the author of this post.", "danger")
        return redirect(url_for("show_post",post_id=post_id))
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(obj=post)
    
    # 获取已标记的用户
    tagged_users = Tagged_user.query.filter_by(post_id=post_id).all()

    tagged_users_data = [{"id": user.user_id, "name": user.user.user_name} for user in tagged_users]
    

    if edit_form.validate_on_submit():
        images_folder = edit_form.images_folder.data
        if images_folder:
            if not allowed_file(images_folder.filename):
                flash("File does not have an approved extension.")
                return redirect(url_for("edit_post", post_id=post_id))

            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(images_folder.filename))
            images_folder.save(folder_path)
            extract_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted')
            os.makedirs(extract_folder, exist_ok=True)
            try:
                with zipfile.ZipFile(folder_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
            except zipfile.BadZipFile:
                flash('Error: Uploaded file is not a valid zip file.')
                os.remove(folder_path)
                return redirect(url_for("edit_post", post_id=post_id))
            image_files = os.listdir(extract_folder)
        else:
            extract_folder = None
            image_files = []

        post.title = edit_form.title.data
        post.img_url = edit_form.img_url.data
        post.author_id = current_user.user_id
        post.img_folder = extract_folder
        post.body = edit_form.body.data

        db.session.commit()

        tagged_users_data = request.form.get('tagged_users_data')
        if tagged_users_data:
            tagged_users = json.loads(tagged_users_data)
            Tagged_user.query.filter_by(post_id=post_id).delete()
            for user in tagged_users:
                tagged_user = Tagged_user(user_id=int(user['id']), post_id=post_id)
                db.session.add(tagged_user)

        db.session.commit()

        return redirect(url_for("show_post", post_id=post.blogpost_id))

    return render_template("make-post.html", form=edit_form, post=post, is_edit=True, tagged_users_data=tagged_users_data)

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    if not is_post_author(post_id):
        flash("You are not the author of this post.", "danger")
        return redirect(url_for("show_post",post_id=post_id))
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/delete/<int:comment_id>/<int:post_id>")
def delete_comment(comment_id, post_id):
    comment_to_delete = db.get_or_404(Comment, comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/test")
def test():
    return render_template("test.html")


@app.route('/check_user', methods=['POST'])
def check_user():
    user_id = request.form['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return jsonify({'status': 'found', 'user': {'id': user.user_id, 'name': user.user_name}})
    else:
        return jsonify({'status': 'not found'})

@app.route('/profile/<int:user_id>', methods=['POST', 'GET'])
def profile(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        abort(404)
    #check whether the user is the incoming or outgoing student
    incoming_user = Incoming_user.query.filter_by(incoming_user_id=user_id).first()
    outgoing_user = Outgoing_user.query.filter_by(outgoing_user_id=user_id).first()
    if incoming_user:
        user_student_type = 'International Student'
        detailed_info = incoming_user
    elif outgoing_user:
        user_student_type = 'Taiwanese Student'
        detailed_info = outgoing_user
    else:
        user_student_type = 'Xchange'
        detailed_info = {
            'info': 'It is the official account of the website.'
        }
    posts = BlogPost.query.filter_by(author_id=user_id).all()
    tagged_posts = Tagged_user.query.filter_by(user_id=user_id).all()
    tagged_posts = [post.post for post in tagged_posts]
    return render_template("profile.html", user=user, posts=posts, tagged_posts=tagged_posts, detailed_info=detailed_info, 
                           user_student_type=user_student_type,is_profile_user=is_profile_user(user_id))

@app.route('/edit-profile/<int:user_id>', methods=['POST', 'GET'])
def edit_profile(user_id):
    if not is_profile_user(user_id):
        flash("You are not the owner of this profile.", "danger")
        return redirect(url_for('profile', user_id=user_id))
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        abort(404)
    incoming_user = Incoming_user.query.filter_by(incoming_user_id=user_id).first()
    outgoing_user = Outgoing_user.query.filter_by(outgoing_user_id=user_id).first()
    if incoming_user:
        form=IncomingForm(obj=incoming_user)
    elif outgoing_user:
        form=OutgoingForm(obj=outgoing_user)
    else:
        redirect(url_for('profile', user_id=user_id))
    if form.validate_on_submit():
        if incoming_user:
            incoming_user.origin_school = form.origin_school.data
            incoming_user.continent = form.continent.data
            incoming_user.country = form.country.data
            incoming_user.region = form.region.data
            incoming_user.info = form.info.data
        elif outgoing_user:
            outgoing_user.exchanging_school = form.exchanging_school.data
            outgoing_user.continent = form.continent.data
            outgoing_user.country = form.country.data
            outgoing_user.region = form.region.data
            outgoing_user.info = form.info.data
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    return render_template("edit-profile.html", form=form, user_id=user_id)

    

#check password
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')
    
    user = User.query.filter_by(user_id=user_id).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'status': 'correct'})
    else:
        return jsonify({'status': 'incorrect'})

if __name__ == "__main__":
    app.run(debug=False)
