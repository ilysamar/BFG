
import os
from dotenv import load_dotenv, find_dotenv
import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

app = Flask(__name__)
connectionString = 'postgresql+psycopg2://{usr}:{passwd}@{host}:{port}/{db}'.format(
    usr=os.environ.get('POSTGRES_USER'),
    passwd=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('POSTGRES_HOST'),
    port=os.environ.get('POSTGRES_PORT'),
    db=os.environ.get('POSTGRES_DB'))

app.config['SQLALCHEMY_DATABASE_URI'] = connectionString

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)

class Cand(db.Model):
    id = db.Column('cand_id', db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    secondname = db.Column(db.String(20))
    about = db.Column(db.String(200))

    def __init__(self, name, secondname, about):
        self.name = name
        self.secondname = secondname
        self.about = about




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['secondname'] or not request.form['about']:
            flash('Пожалуйста, заполните все поля', 'error')
        else:
            cand = Cand(
                    request.form['name'],
                    request.form['secondname'],
                    request.form['about'])

            db.session.add(cand)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('show_all.html', cand=Cand.query.all())


if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
            print("ERROR:" + "DB")
        else:
            dbstatus = True
    app.run(debug=True, host='0.0.0.0', port=8080)
