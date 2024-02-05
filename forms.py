from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your E-Mail Address", validators=[DataRequired()])
    password = PasswordField("Your Password", validators=[DataRequired()])
    img_url = FileField("Profile Picture", validators=[DataRequired()])
    submit = SubmitField("Get Started!")

# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("Your E-Mail Address", validators=[DataRequired()])
    password = PasswordField("Your Password", validators=[DataRequired()])
    submit = SubmitField("Get Started!")

# TODO: Create a CommentForm so users can leave comments below posts

class CommentForm(FlaskForm):
    comment = CKEditorField("Add a Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
