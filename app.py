from flask import Flask, request
import random
import string
import subprocess
from datetime import datetime, timedelta

app = Flask(__name__)

def generate_username():
    return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Temp User Manager</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            display: flex;
        }}

        .sidebar {{
            width: 220px;
            background: #020617;
            padding: 20px;
            height: 100vh;
        }}

        .sidebar h2 {{
            color: #38bdf8;
        }}

        .sidebar button {{
            width: 100%;
            padding: 10px;
            margin-top: 15px;
            background: #1d4ed8;
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 6px;
        }}

        .content {{
            flex: 1;
            padding: 40px;
        }}

        .card {{
            background: #020617;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}

        .btn {{
            padding: 10px 15px;
            background: #22c55e;
            border: none;
            border-radius: 6px;
            color: white;
            cursor: pointer;
        }}

        .delete-btn {{
            background: #ef4444;
        }}

        input {{
            padding: 8px;
            margin: 5px 0;
            width: 200px;
            border-radius: 5px;
            border: none;
        }}

        .user-box {{
            margin-top: 10px;
            padding: 10px;
            background: #1e293b;
            border-radius: 6px;
        }}
    </style>
</head>
<body>


<div class="content">

    <div class="card">
        <h2>Create Temp User</h2>

        <form method="post" action="/">
            <input name="username" placeholder="Username (optional)">
            <br>
            <input name="password" placeholder="Password (optional)">
            <br><br>
            <button class="btn" type="submit">Create User</button>
        </form>
    </div>

    {content}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def create_user():

    content = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            username = generate_username()
        if not password:
            password = "temp123"

        subprocess.run(["sudo", "useradd", "-m", "-G", "tempusers", username])

        subprocess.run(["sudo", "passwd", username],
                       input=f"{password}\n{password}\n",
                       text=True)

        subprocess.run(["sudo", "chage", "-d", "0", username])

        expiry_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        subprocess.run(["sudo", "chage", "-E", expiry_date, username])

        # get expiry info
        result = subprocess.run(["chage", "-l", username],
                                capture_output=True,
                                text=True)

        content = f"""
        <div class="card">
            <h3>✅ User Created</h3>
            <div class="user-box">
                <p><b>Username:</b> {username}</p>
                <p><b>Password:</b> {password}</p>
                <pre>{result.stdout}</pre>
            </div>
        </div>
        """

    return HTML_TEMPLATE.format(content=content)


@app.route("/users")
def list_users():
    try:
        result = subprocess.run(
            ["getent", "group", "tempusers"],
            capture_output=True,
            text=True
        )

        parts = result.stdout.strip().split(":")
        users = parts[-1].split(",") if parts[-1] else []

        users_html = ""

        for u in users:
            if not u:
                continue

            chage_info = subprocess.run(
                ["chage", "-l", u],
                capture_output=True,
                text=True
            ).stdout

            users_html += f"""
            <div class="user-box">
                <b>{u}</b>
                <pre>{chage_info}</pre>

                <form method="post" action="/delete">
                    <input type="hidden" name="username" value="{u}">
                    <button class="btn delete-btn" type="submit">Delete</button>
                </form>
            </div>
            """

        if not users_html:
            users_html = "<p>No active users</p>"

    except Exception as e:
        users_html = f"<p>Error: {str(e)}</p>"

    content = f"""
    <div class="card">
        <h2>👥 Active Users</h2>
        {users_html}
    </div>
    """

    return HTML_TEMPLATE.format(content=content)


@app.route("/delete", methods=["POST"])
def delete_user():
    username = request.form.get("username")

    if username:
        subprocess.run(["sudo", "userdel", "-r", username])

    return list_users()


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)