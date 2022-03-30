from flaskauth import app, db
import logging

db.init_app(app)

with app.app_context():
    db.create_all()
logging.info('Db tables created')

if __name__ == '__main__':
    app.run(debug=True)