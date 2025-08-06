from flask import Flask, render_template, request, redirect, make_response
import os
import secrets

app = Flask(__name__)
posts = [
    {
        "author": "Alice",
        "content": "Has anyone implemented OAuth2 in Flask recently? Would love some tips."
    },
    {
        "author": "Bob",
        "content": "Reminder: Always sanitize user inputs before rendering them on the frontend!"
    },
    {
        "author": "Mallory",
        "content": "Has anyone managed to play with some of the cool javascript functions available within this site?<script>console.log('Directory Fuzzing at its best.')</script>"
    }
]

with open("/app/flag.txt", "r") as f:
    FLAG = f.read().strip()

ADMIN_COOKIE = secrets.token_hex(16)
print(f"[+] Admin cookie set to: {ADMIN_COOKIE}")

with open("/tmp/admin_cookie.txt", "w") as f:
    f.write(ADMIN_COOKIE)

@app.route("/")
def forum():
    return render_template("forum.html", posts=posts)

@app.route("/post", methods=["POST"])
def post():
    author = request.form.get("author")
    content = request.form.get("content")
    posts.append({"author": author, "content": content})
    return redirect("/")

@app.route("/admin")
def admin():
    cookie = request.cookies.get("auth")
    if cookie == ADMIN_COOKIE:
        return render_template("admin.html", secret=FLAG)
    return render_template("unauthorised.html"), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

