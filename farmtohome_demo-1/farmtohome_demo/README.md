
# Farm to Home - Farmer Portal (Functional Demo)

**What this is**
- A simple functional demo of a "Farm to Home" Farmer Portal built with Flask + SQLite.
- Farmers can register and add crop listings.
- Customers can view listings and send contact messages.

**Important (demo)**: This is a demonstration project. For production use:
- Use secure password hashing (bcrypt/argon2) and secure sessions.
- Add input validation, rate-limiting, and file upload sanitization.
- Host on a proper server (Gunicorn + Nginx) and enable HTTPS.

**How to run locally**
1. Make sure Python 3.9+ is installed.
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Initialize database:
   ```
   flask --app app.db_init init
   ```
4. Run the app:
   ```
   flask --app app run --host=0.0.0.0 --port=5000
   ```
5. Open http://localhost:5000 in your browser.

**Credentials**
- For this demo you can register a farmer account from the "Farmer Register" page.

**Files**
- app.py            : Flask application
- templates/        : HTML templates (Jinja2)
- static/           : CSS and images
- farmtohome.db     : SQLite DB after initialization (created when you run the init command)

