from flask import Flask, request
app = Flask(__name__)

@app.route('/eval')
def dangerous():
    code = request.args.get('code')
    return str(eval(code))

app.run()
