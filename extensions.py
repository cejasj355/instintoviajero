from flask_mail import Mail
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()