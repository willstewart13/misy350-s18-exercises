from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    #return "hello world"
    return render_template('index.html')


@app.route('/form-basics')
def form_basics():
    #return "hello world"
    return render_template('form-basics.html')

@app.route('/form-demo')
def form_demo():

    first_name = request.args.get('first_name')
    return first_name

@app.route('/users')
def users(username):
    #return "<h1>hello %s</h1>" % username
    return render_template('user.html',uname=username)


@app.route('/user')
def user():
    return "this is a page for users"


if __name__ == '__main__':
    app.run()
