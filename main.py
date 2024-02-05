from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import desc
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
UPLOAD_FOLDER = './static/assets/img/profile_img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ckeditor = CKEditor(app)
Bootstrap5(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            error = 'Sorry, this page is Admin only, please log in as Admin to access'
            return redirect(url_for('login', error=error))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    img_url = db.Column(db.String(1000))
    password = db.Column(db.String(100))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        error=None
        email = form.data['email']
        password = generate_password_hash(form.data['password'], method='pbkdf2:sha256', salt_length=8)
        # checking if email is already in database and referring to login page
        result = db.session.execute(db.select(User).where(User.email == email))
        existing_user = result.scalar()
        if existing_user:
            error = "Sorry, this email already exists, try logging in instead:"
            return redirect(url_for('login',error=error))

        # Save the uploaded image to the server
        img_file = form.img_url.data
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = filename
        else:
            img_url = None

        new_user = User(
            name=form.data['name'],
            email=email,
            password=password,
            img_url = img_url
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('get_all_posts'))
    return render_template("register.html", form=form)



@app.route('/login', methods=["GET","POST"])
def login():
    error = request.args.get('error')
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']

        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            error= "E-mail not found. If you don't have an account, register instead."
        elif not check_password_hash(user.password, password):
            error = 'Wrong password, please try again'
        else:
            login_user(user)
            flash('You were successfully logged in')
            return redirect(url_for('get_all_posts'))
    print(error)
    return render_template("login.html", error=error, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost).order_by(desc(BlogPost.id)))
    posts = result.scalars().all()
    # Check if there are any posts
    if len(posts) == 0:
        # If no posts are available, render a template indicating that there are no posts.
        return render_template("no_posts.html")
    return render_template("index.html", all_posts=posts)



@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    post_list = db.session.execute(db.select(BlogPost).order_by(desc(BlogPost.id)))
    posts = post_list.scalars().all()
    if form.validate_on_submit():
        new_comment = Comment(
        comment = form.data['comment'],
        post_id=requested_post.id,
        author = current_user.name,
        img_url = current_user.img_url,
        date = date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_comment)
        db.session.commit()
        result = db.session.execute(db.select(Comment).order_by(desc(Comment.id)))
        comments = result.scalars().all()
        return redirect(url_for("show_post", post_id=post_id, all_comments=comments, all_posts=posts))
    result = db.session.execute(db.select(Comment).order_by(desc(Comment.id)))
    comments = result.scalars().all()
    return render_template("post.html", post=requested_post, form=form, all_comments=comments, all_posts=posts)



@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user.name,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)



@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user.name
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)



@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/delete/<int:comment_id>/<int:post_id>")
@admin_only
def delete_comment(comment_id, post_id):
    comment_to_delete = db.get_or_404(Comment, comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))

@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True, port=5002)
