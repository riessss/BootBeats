from app.app import create_app
from app.database import instert_intruments, inster_default_song
from app.models import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        instert_intruments()
        inster_default_song()
    app.run(debug=True)
