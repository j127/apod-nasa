from flask import Blueprint, render_template, url_for, redirect
# from ..models.posts import Post

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    """Renders the homepage of the site."""
    return redirect('apod/astropix.html')

@pages_bp.route('/about')
def about():
    """Renders the about page."""
    data = {
        'title': 'About this Website'
    }
    return render_template('pages/about.html', data=data)
