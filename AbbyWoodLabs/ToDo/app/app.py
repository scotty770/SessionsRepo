from flask import Flask, render_template, request, redirect, make_response
import os
import secrets

# Problems
# With testing - incognito mode retains the same cookies as regular mode - apparently!
# Make some more user posts or make the entropy smaller to encourage collisions.


app = Flask(__name__)
posts = {
    "1":[{
        "content": "I implemented OAuth2 in Flask recently! Would love some tips."
    }],
    "2":[{
        "content": "Reminder: Always sanitize user inputs before rendering them on the frontend!"
    }],
    "3":[{
        "content": "Has anyone managed to play with some of the cool javascript functions available within this site?<script>console.log('Directory Fuzzing at its best.')</script>"
    }]
}


# with open("/app/flag.txt", "r") as f:
#     FLAG = f.read().strip()

# ADMIN_COOKIE = secrets.token_hex(16)
# print(f"[+] Admin cookie set to: {ADMIN_COOKIE}")


# with open("/tmp/admin_cookie.txt", "w") as f:
#     f.write(ADMIN_COOKIE)

@app.route("/")
def forum():
    try:
        sessionID = request.cookies.get('sessionID')
        if not sessionID:
            5/0
        if sessionID in posts:
            resp = make_response(render_template('forum.html', posts=posts[sessionID]))
        else:
           resp = make_response(render_template('forum.html')) 
    except:
        resp = make_response(render_template('forum.html'))
        resp.set_cookie('sessionID', secrets.token_hex(16))
        
    return resp

@app.route("/post", methods=["POST"])
def post():
    try:
        sessionID = request.cookies.get('sessionID')
        content = request.form.get("content")
        if sessionID in posts:
            posts[sessionID].append({"content": content})
        else:
            posts[sessionID] = [{"content": content}]
    except:
        sessionID = secrets.token_hex(16)
        posts[sessionID] = [{"content": content}]
        response = make_response(redirect('/home'))
        response.set_cookie('sessionID', sessionID)
        return response
    return redirect("/")

@app.route("/change")
def change_token():
    resp = make_response(redirect('/'))
    resp.set_cookie('sessionID', secrets.token_hex(16))
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
    


