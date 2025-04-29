from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app.secret_key = os.getenv('SECRET_KEY', 'default-key')

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/name')
    messages = Message.query.order_by(Message.timestamp).all()
    return render_template('chat.html', messages=messages, username=session['username'])

@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect('/')
    return render_template('name.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/name')

@app.route('/send', methods=['POST'])
def send():
    if 'username' in session:
        content = request.form['message']
        message = Message(sender=session['username'], content=content)
        db.session.add(message)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists('chat.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
