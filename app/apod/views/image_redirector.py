from flask import Blueprint, redirect

redirect_bp = Blueprint('redirect', __name__, url_prefix='/apod/image')


@redirect_bp.route('/<img_path>')
def img_redirect(img_path):
    """Redirects the image URLs from the old site to the new locations in the Flask app."""
    return redirect('/static/images/{}'.format(img_path))
