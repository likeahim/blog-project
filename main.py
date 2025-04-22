from blog import create_app, db
from flask_migrate import upgrade
from blog.models import Entry

app = create_app()

with app.app_context():
    upgrade()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)