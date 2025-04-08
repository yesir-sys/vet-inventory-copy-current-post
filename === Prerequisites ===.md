=== Prerequisites ===
1. Download Python 3.x from python.org
2. Check "Add Python to PATH" during installation
3. Verify installation:
   > python --version

=== Project Setup ===
1. Create & activate virtual environment:
   > mkdir vet-inventory
   > cd vet-inventory
   > python -m venv venv
   > .\venv\Scripts\activate

2. Install required packages:
   > pip install django
   > pip install openpyxl
   > pip install pillow
   > pip install mysqlclient
   > pip install psycopg2

3. Configure settings.py:
   - Update DATABASES setting to use SQLite
   - Set correct static files directory for Windows

4. Initialize database:
   > python manage.py makemigrations
   > python manage.py migrate
   > python manage.py createsuperuser

5. Start development server:
   > python manage.py runserver

=== System Requirements ===
- Windows 10 or 11
- Minimum 4GB RAM
- 500MB free disk space
- Internet connection

=== VS Code Setup ===
1. Install VS Code from code.visualstudio.com
2. Install Python extension
3. Select Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter")
4. Open integrated terminal (Ctrl+`)

=== Access Points ===
Admin interface: http://127.0.0.1:8000/admin/
Main app: http://127.0.0.1:8000/

=== Troubleshooting ===
- If 'python' not found, ensure Python is added to PATH
- Run Command Prompt as Administrator if permission errors occur
- Check firewall settings if unable to access localhost