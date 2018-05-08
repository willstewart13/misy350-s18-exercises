from flask import Flask, render_template
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users(username):
    return render_template('users.html', uname=username)

@app.route('/form')
def form():
    #return "hello world"
    return render_template('form.html')


if __name__ == '__main__':
    app.run()
