from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(**config_overrides):
	app = Flask(__name__, static_url_path='/static')

	# env config
	app.config.from_pyfile("settings.py")

	# config obj
	from .config import Config
	app.config.from_object(Config)

	# config overrides
	app.config.update(config_overrides)

	# extensions	
	from .models.models import db
	db.init_app(app)

	from .extensions import fbcrypt, login_manager
	fbcrypt.init_app(app)
	login_manager.init_app(app)

	# register blueprints
	from .blueprints.admin.views import admin
	from .blueprints.public.views import public
	from .blueprints.users.views import users

	
	app.register_blueprint(admin)
	app.register_blueprint(public)
	app.register_blueprint(users)

	return app


def init_db(**config_overrides):
	app = Flask(__name__, static_url_path='/static')

	# env config
	app.config.from_pyfile("settings.py")

	# config obj
	from .config import Config
	app.config.from_object(Config)

	# config overrides
	app.config.update(config_overrides)

	# extensions	
	from .models.models import db
	db.init_app(app)

	from .extensions import fbcrypt, login_manager
	fbcrypt.init_app(app)
	login_manager.init_app(app)


	from .models.tests import populate

	with app.app_context():
		db.drop_all()
		db.create_all()
		populate.populate_roles(db)
		populate.populate_categories(db)
		populate.populate_sub_categories(db)

	return None
