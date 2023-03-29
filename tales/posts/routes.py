from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user, login_required
from models import Post
from posts.forms import UpdatePost
from tales import db

posts = Blueprint('posts', __name__)

@posts.route('/post/new/', methods=['GET', 'POST'])
@login_required
def new_post():
    form=UpdatePost()
    if form.validate_on_submit():
        flash('Your post has been created', 'success')
        post = Post(title=form.title.data, content=form.content.data, author=current_user )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('addpost.html', title='Post', form=form, legend='New Post')

@posts.route('/post/<int:post_id>/')
def edit_post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('editpost.html', post=post)

@posts.route('/post/<int:post_id>/update/', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdatePost()     
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data      
        db.session.commit()
        flash('Post has been updated successfully', 'success')
        return redirect(url_for('posts.edit_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('addpost.html', form=form, post=post, legend='Update Post')

@posts.route('/post/<int:post_id>/', methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted', 'success')
    return redirect(url_for('main.home'))