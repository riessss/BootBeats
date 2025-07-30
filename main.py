from app.app import create_app
from app.database import instert_intruments
from app.models import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        instert_intruments()
    app.run(debug=True)
