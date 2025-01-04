import os

def create_file(filepath, content):
    """Creates a file and writes content to it."""
    with open(filepath, 'w') as f:
        f.write(content)

def scaffold_railway_project():
    # Create project directory
    project_name = input("Enter your project name (default: flask-redirect-app): ") or "flask-redirect-app"
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    # app.py
    app_py_content = """\
from flask import Flask, redirect
import os

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    target_redirect = os.getenv("TARGET_REDIRECT", "https://example.com")
    return redirect(target_redirect, code=301)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
"""
    create_file("app.py", app_py_content)

    # requirements.txt
    requirements_txt_content = """\
flask==2.3.2
gunicorn==21.2.0
"""
    create_file("requirements.txt", requirements_txt_content)

    # Dockerfile
    dockerfile_content = """\
# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt requirements.txt
COPY app.py app.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application's port
EXPOSE 5000

# Start the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
"""
    create_file("Dockerfile", dockerfile_content)

    # Print success message
    print(f"🚀 Your Railway Flask project '{project_name}' has been created!")
    print("Next steps:")
    print(f"1. Navigate to the project directory: cd {project_name}")
    print("2. Test locally with Docker:")
    print("   docker build -t flask-redirect-app .")
    print("   docker run -p 5000:5000 -e TARGET_REDIRECT=https://example.com flask-redirect-app")
    print("3. Deploy to Railway and set TARGET_REDIRECT as an environment variable.")

if __name__ == "__main__":
    scaffold_railway_project()

