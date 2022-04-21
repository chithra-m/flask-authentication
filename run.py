from flaskauth import create_app, db
import logging

# db.init_app(app)
app = create_app()
with app.app_context():
    db.create_all()
logging.info('Db tables created')

if __name__ == '__main__':
    app.run(debug=True)