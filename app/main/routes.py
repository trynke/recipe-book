from flask import render_template, flash, redirect, url_for, request, g, \
    current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException
from app import db
from app.main.forms import EditProfileForm, EmptyForm, RecipeForm
from app.models import User, Recipe
from app.main import bp


@bp.before_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        try:
            language = detect(form.recipe.data)
        except LangDetectException:
            language = ''
        recipe = Recipe(name=form.recipe.data, author=current_user,
                        language=language)
        db.session.add(recipe)
        db.session.commit()
        flash(_('You just added a new recipe!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    recipes = current_user.followed_recipes().paginate(
        page=page, per_page=current_app.config['RECIPES_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('main.index', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           recipes=recipes.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    recipes = user.recipes.order_by(Recipe.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['RECIPES_PER_PAGE'], error_out=False)
    next_url = url_for('main.user', username=user.username, page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('main.user', username=user.username, page=recipes.prev_num) \
        if recipes.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, recipes=recipes.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You are following %(username)s!', username=username))
        return redirect(url_for('main.user', username=username))
    return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You are not following %(username)s.', username=username))
        return redirect(url_for('main.user', username=username))
    return redirect(url_for('main.index'))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['RECIPES_PER_PAGE'], error_out=False)
    next_url = url_for('main.explore', page=recipes.next_num) \
        if recipes.has_next else None
    prev_url = url_for('explore', page=recipes.prev_num) \
        if recipes.has_prev else None
    return render_template('index.html', title=_('Explore'), recipes=recipes.items,
                          next_url=next_url, prev_url=prev_url)
