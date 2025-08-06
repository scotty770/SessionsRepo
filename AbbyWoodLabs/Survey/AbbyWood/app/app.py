from flask import Flask, render_template, request, redirect
import secrets

app = Flask(__name__)

answers = {}

@app.route('/')
def index():
    if request.args.get('session_id'):
        session = request.args.get('session_id')
    else:
        session = secrets.token_hex(16)
    return render_template('survey.html', session=session)

@app.route('/submit')
def submit():
    # try:
    sessionID = request.args.get('session_id')
    name = request.args.get('name')
    secret = request.args.get('secret')
    answers[sessionID] = [name, secret]
    return redirect('/results?session_id=' + sessionID)
    # except:
    #     return redirect('/')


@app.route('/results', methods=['GET'])
def results():
    sessionID = request.args.get('session_id')

    if not sessionID:
        return redirect('/')
    
    if sessionID in answers:
        flag = answers[sessionID]
        return render_template('survey2.html', session=sessionID, name=flag[0], secret=flag[1])
    
    return redirect('/')
        
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3004)

