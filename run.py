from archiver import app
import os


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', post=int(os.environ.get("PORT", 5000)))
