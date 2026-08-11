from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categoria')
def categoria():
    return render_template('categoria.html')

@app.route('/termo')
def termo():
    return render_template('termo.html')

if __name__ == '__main__':
    app.run(debug=True)