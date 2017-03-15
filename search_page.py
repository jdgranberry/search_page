from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('template.html', my_string="Hello World!", my_list=[0, 1, 2, 3, 4, 5])
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
