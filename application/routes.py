from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image


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
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        email = form.email.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash('An email has been sent to your email address.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email not found.', 'error')

    return render_template('reset_password.html', title='Reset Password', form=form)

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
    posts = user.posts
    return render_template('profile.html', title=f'{user.fullname} Profile', user=user, posts=posts)

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
            pass
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    form.username.data = current_user.username
    form.fullname.data = current_user.fullname
    form.bio.data = current_user.bio

    return render_template('edit_profile.html', title='Edit (current_user.username) Profile', form=form)

@app.route('/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post():
    form = EditPostForm()

    post = Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        post.caption = form.caption.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))

    elif request.method == 'GET':
        form.caption.data = post.caption

    return render_template('edit_post.html', title='Edit Post', form=form)

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

if __name__ == '__main__':
    app.run(debug=True)
