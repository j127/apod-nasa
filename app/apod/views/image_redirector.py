from flask import Blueprint, redirect

redirect_bp = Blueprint('redirect', __name__, url_prefix='/apod/image')


@redirect_bp.route('/<img_path>')
def img_redirect(img_path):
    return redirect('/static/images/{}'.format(img_path))
