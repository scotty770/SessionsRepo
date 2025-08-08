from flask import Flask, render_template, request, redirect, make_response
import os
import secrets
import base64
import json

app = Flask(__name__)
posts = [
    {
        "author": "Steve",
        "content": "How much is behind the bar for the summer party?"
    },
    {
        "author": "Bob",
        "content": "Reminder: Always sanitize user inputs before rendering them on the frontend!"
    },
    {
        "author": "Greta",
        "content": "Has anyone managed to play with some of the cool javascript functions available within this site?"
    }
]

# with open("/app/flag.txt", "r") as f:
#     FLAG = f.read().strip()

# ADMIN_COOKIE = secrets.token_hex(16)
# print(f"[+] Admin cookie set to: {ADMIN_COOKIE}")

# with open("/tmp/admin_cookie.txt", "w") as f:
#     f.write(ADMIN_COOKIE)

@app.route("/")
def forum():
    cookie = request.cookies.get("auth")
    resp = make_response(render_template('forum.html', posts=posts))
    if not cookie:
        resp.set_cookie('auth', str(base64.b64encode('{"name":"guest", "role":"user"}'.encode()))[2:-1])
    return resp

@app.route("/post", methods=["POST"])
def post():
    author = request.form.get("author")
    content = request.form.get("content")
    posts.append({"author": author, "content": content})
    return redirect("/")

@app.route("/admin")
def admin():
    cookie = request.cookies.get("auth")
    if not cookie:
        return render_template("unauthorised.html"), 403
    check = is_admin(cookie)

    if check == "success":
        return render_template("admin.html", secret="SUCCESS!")
    
    else:
        return render_template("unauthorised.html", reason=check), 403
    

def is_admin(token):
    # try:
    token = base64.b64decode(token).decode("utf-8")
    form = json.loads(token)
    
    if "admin" not in form["role"].lower():
        return "Incorrect role"
    
    if form["name"] == "guest":
        return "Guests cannot be administrators"

    if form["name"] == "Bob" or form["name"] == "Steve" or form["name"] == "Greta":
        return "Name does not match administrator accounts"
    return "success"
    # except:
    #     return "Unknown Reason for Auth Failure"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

