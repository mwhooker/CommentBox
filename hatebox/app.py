import random
import glob
import os
from datetime import datetime

from flask import Flask, request, redirect, url_for
from flask import render_template
from flaskext.sqlalchemy import SQLAlchemy
import sqlalchemy.exc
from sqlalchemy.sql.expression import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

def get_hater_image(image_dir):
    return random.choice(glob.glob( os.path.join(image_dir, '*') ))

def vote(hate_obj):
    hate_obj.votes += 1
    db.session.add(hate_obj)
    db.session.commit()

class Hate(db.Model):
    __tablename__ = 'hate'
    id = db.Column(db.Integer, primary_key=True)
    hate = db.Column(db.String(1024), unique=True)
    name = db.Column(db.String(80))
    created = db.Column(db.DateTime(), default=datetime.now)
    votes = db.Column(db.Integer, server_default='1')

    def __init__(self, hate):
        self.hate = hate


@app.route('/hate', methods=['POST'])
def hate():
    try:
        h = Hate(request.form['hate'])
        db.session.add(h)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        h = db.session.query(Hate).filter(Hate.hate == request.form['hate']).one()
        vote(h)
    return redirect(url_for('main'))


@app.route("/")
def main():
    hater_img = get_hater_image('static/haters')
    hate = db.session.query(Hate).order_by(desc(Hate.votes)).limit(25).all()
    return render_template('main.html', hater_img=hater_img, hate=hate)

if __name__ == "__main__":
    app.debug = True
    app.run()
