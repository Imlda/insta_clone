from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images/posts')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile', username=username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if user.password != form.old_pass.data:
            flash("ur old password is wrong")
        user.password = form.new_pass.data
        user.password_Confirm = form.confirm_pass.data

        db.session.commit()
        flash("password has been reset", 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    return render_template('reset_password.html', title='ResetPassword', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        

        user = User.query.filter_by(email=email).first()
        if user:
            flash('An email has been sent to your email address.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email not found.', 'error')

    return render_template('forgot_password.html', title='Forgot Password', form=form)

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    form = VerificationForm()

    if form.validate_on_submit():
        code = form.code.data

        if code == '123456':
            flash('Your password has been reset.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid code.', 'error')

    return render_template('verification.html', title='Verification', form=form)

@app.route('/<string:username>')
@login_required
def profile(username):
    form = EditProfileForm()

    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author_id=user.id).all()
    return render_template('profile.html', title=f'{user.fullname} Profile', user=user, posts=posts)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if form.username.data != user.username:
            user.username = form.username.data
        user.fullname = form.fullname.data
        user.bio = form.bio.data

        if form.profile_pic.data:
            file = form.profile_pic.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_pic = filename

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))

    form.username.data = current_user.username
    form.fullname.data = current_user.fullname
    form.bio.data = current_user.bio

    return render_template('edit_profile.html', title=f'Edit {current_user.username} Profile', form=form)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    form = EditPostForm()

    post = Post.query.get(post_id)
    if form.validate_on_submit():
        post.caption = form.caption.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))

    elif request.method == 'GET':
        form.caption.data = post.caption

    return render_template('edit_post.html', title='Edit Post', form=form, post=post)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            author_id = current_user.id,
            caption = form.caption.data
        )
        post.photo = save_image(form.post_pic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted!', 'success')
        
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id = current_user.id)\
                        .order_by(Post.post_date.desc())\
                        .paginate(page=page, per_page=3)

    return render_template('index.html', title='Home', form=form, posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    
    if form.validate_on_submit():
        user = User(
            fullname = form.fullname.data,
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    data = request.json
    post_id = int(data['postId'])
    like = Like.query.filter_by(user_id=current_user.id,post_id=post_id).first()
    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return make_response(jsonify({"status" : True}), 200)
    
    db.session.delete(like)
    db.session.commit()
    return make_response(jsonify({"status" : False}), 200)