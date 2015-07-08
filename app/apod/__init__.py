from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
# from flask_admin import Admin
# from .views.admin import AdminIndexView
import mongoengine

def register_blueprints(app_instance):
    """This function prevents circular imports."""
    from .views.pages import pages_bp
    from .views.pictures import pictures_bp

    app_instance.register_blueprint(pages_bp)
    app_instance.register_blueprint(pictures_bp)


app = Flask(__name__, instance_relative_config=True)

# From default to overridden
app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.debug = True

# Debug toolbar must come after app.debug = True
toolbar = DebugToolbarExtension(app)

mongoengine.connect(app.config['MONGODB_DB'])

register_blueprints(app)
