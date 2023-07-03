from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database URI
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))

    def __init__(self, content):
        self.content = content


@app.route('/', methods=['GET', 'POST'])
def home():
    #Get content from the form, create a message from the content, add to database and commit those changes
    if request.method == 'POST':
        content = request.form['content']
        message = Message(content)
        db.session.add(message)
        db.session.commit()
        return 'Message added to the database.'
    #get all messages and display in index.html
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

#Flask stuff - create database tables and run app in debug mode
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
