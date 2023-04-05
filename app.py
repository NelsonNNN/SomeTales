from tales import create_app


app = create_app()
from tales.models import User
from tales import db

with app.app_context():
    db.create_all()


if __name__ == '__main__':
        app.run(debug=True)
