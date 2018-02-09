from archiver import app, db
import os


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
