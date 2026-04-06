# 🚀 Server LIB - Ephemeral SSH Access System

This project provides a lightweight web-based system to generate temporary Linux users for SSH access.  
Users are created via a browser request and expire automatically after a set duration.

---

## 🧱 Requirements

- Debian / Ubuntu system
- Python 3.10+
- Nginx
- sudo access

---

## 📦 Installation

### 1. Install Required Packages

```bash
sudo apt update
sudo apt install nginx python3-venv python3-pip -y
````

---

## 📂 Project Structure

```
server_lib/
├── app.py
├── requirements.txt
├── run.sh
└── venv/ (auto-created)
```

---

## ⚙️ Nginx Configuration

### Create Configuration File

```bash
sudo nano /etc/nginx/sites-available/tempusers
```

### Add the Following Config

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5001;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

### Enable the Site

```bash
sudo ln -s /etc/nginx/sites-available/tempusers /etc/nginx/sites-enabled/
```

---

### Remove Default Site (Important)

```bash
sudo rm /etc/nginx/sites-enabled/default
```

---

### Test and Restart Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🐍 Python Environment Setup

### Install venv (if not already installed)

```bash
sudo apt install python3-venv -y
```

---

### Make Script Executable

```bash
chmod +x run.sh
```

---

## ▶️ Run the Application

```bash
./run.sh
```

### What `run.sh` Does

* Creates virtual environment (if missing)
* Activates it
* Installs dependencies
* Starts Gunicorn on:

```
127.0.0.1:5001
```

---

## 🌐 Access the Application

Open in browser:

```
http://<YOUR_SERVER_IP>
```

---

## 🔍 Verification

### Check Gunicorn

```bash
ps aux | grep gunicorn
```

---

### Check Port

```bash
lsof -i :5001
```

---

### Check Nginx

```bash
systemctl status nginx
```

---

## 🔐 Sudo Permissions (IMPORTANT)

The application requires system-level commands:

* `useradd`
* `passwd`
* `chage`

Grant passwordless access:

```bash
sudo visudo
```

Add:

```
youruser ALL=(ALL) NOPASSWD: /usr/sbin/useradd, /usr/bin/passwd, /usr/bin/chage
```

---

## ⚠️ Security Recommendations

### Restrict Access by IP

```nginx
location / {
    allow YOUR_IP;
    deny all;

    proxy_pass http://127.0.0.1:5001;
}
```

---

### Enable Rate Limiting

Add at top of config:

```nginx
limit_req_zone $binary_remote_addr zone=one:10m rate=5r/m;
```

Inside location:

```nginx
limit_req zone=one burst=5;
```

---

## ❌ Common Issues

### 502 Bad Gateway

Gunicorn not running:

```bash
./run.sh
```

---

### Port Already in Use

```bash
fuser -k 5001/tcp
```

---

### Permission Denied

Check `sudoers` configuration.

---

### Changes Not Applied

```bash
sudo systemctl restart nginx
```

---

## 🧠 Architecture

```
Browser
   ↓
Nginx (Port 80)
   ↓
Gunicorn (127.0.0.1:5001)
   ↓
Flask App
   ↓
Linux System (useradd / chage / passwd)
```

---

## 🏁 Features

* Temporary SSH user creation
* Automatic expiry
* Web-based provisioning
* Nginx reverse proxy
* Lightweight deployment

---

## 🚀 Future Improvements

* HTTPS (Let's Encrypt)
* User dashboard UI
* Auto cleanup of expired users
* Docker-based isolation
* Authentication system

---

## ⚡ Notes

⚠️ This system executes privileged commands.
Ensure proper access control and security hardening before exposing publicly.

