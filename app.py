# app.py

from flask import Flask
from application.config import LocalDevlopmentConfig
from application.models import User, Reservation, Parkinglot, ParkingSpot
from application.database import db
from application.security import jwt
from flask_cors import CORS
from application.routes import routes
from application.celery_init import celery_init_app
from celery.schedules import crontab
from flask_caching import Cache

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevlopmentConfig)
    cache = Cache(config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': 'redis://localhost:6379/0'
    })
    cache.init_app(app)
    celery_init_app(app)
    db.init_app(app)
    
    jwt.init_app(app)
    CORS(app,supports_credentials=True, origins=["http://localhost:5173"])

    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(is_admin=True).first():
            db.session.add(User(
                email_id='admin@email.com',
                full_name='Bruce Wayne',
                password='admin',
                is_admin=True,
                address='Gotham City',
                pincode='123456'
            ))
            db.session.commit()

    return app


app = create_app()
celery=celery_init_app(app)
celery.autodiscover_tasks(['application'])

@celery.on_after_finalize.connect
def setup_periodic_task(sender,**kwargs):
    print(">>> Registering periodic tasks")
    sender.add_periodic_task(
        crontab(minute='*/2'),
        monthly_report.s()
        )
    sender.add_periodic_task(
        crontab(hour=7, minute=0),
        daily_reminder_mail.s(),
    )

from application.routes import *

if __name__ == '__main__':
    app.run(use_reloader=False)