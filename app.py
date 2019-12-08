from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/deneme')
def deneme():
    return render_template('deneme.html')
app.run(debug=True)