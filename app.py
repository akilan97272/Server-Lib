from flask import Flask
from flask import request
import os
import random
import string
import subprocess
from datetime import datetime, timedelta

app = Flask(__name__)

def generate_username():
    return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
@app.route("/")
def create_user():
    # if request.remote_addr != "YOUR_IP":
    #     return "Unauthorized", 403
    username = generate_username()

    # create user + add to group
    subprocess.run(["sudo", "useradd", "-m", "-G", "tempusers", username])

    # set temp password
    subprocess.run(["sudo", "passwd", username], input="temp123\ntemp123\n", text=True)

    # force password change
    subprocess.run(["sudo", "chage", "-d", "0", username])

    # set expiry (1 day)
    expiry_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    subprocess.run(["sudo", "chage", "-E", expiry_date, username])

    return f"""
    <h2>Your temporary SSH account</h2>
    <p>Username: <b>{username}</b></p>
    <p>Temp Password: <b>temp123</b></p>
    <p>Expires in 24 hours</p>
    """
    
@app.route("/users")
def list_users():
    try:
        result = subprocess.run(
            ["getent", "group", "tempusers"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return "Error fetching users"

        group_info = result.stdout.strip()

        # format: tempusers:x:1001:user1,user2
        parts = group_info.split(":")
        users = parts[-1].split(",") if parts[-1] else []

        user_list_html = "<br>".join(users) if users else "No active users"

        return f"""
        <h2>Active Temp Users</h2>
        <p>{user_list_html}</p>
        """

    except Exception as e:
        return f"Error: {str(e)}"
    
# FOR TESTING PURPOUS
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)