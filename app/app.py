
import os
from dotenv import load_dotenv, find_dotenv
import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


load_dotenv(find_dotenv())
#
app = Flask(__name__)
connectionString = 'postgresql+psycopg2://{***REMOVED***}:{passwd}@{host}:{port}/{db}'.format(
    ***REMOVED***=os.environ.get('POSTGRES_USER'),
    passwd=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('POSTGRES_HOST'),
    port=os.environ.get('POSTGRES_PORT'),
    db=os.environ.get('POSTGRES_DB'))

# connectionString = 'postgresql+psycopg2://{***REMOVED***}:{passwd}@{host}:{port}/{db}'.format(
#     ***REMOVED***=os.environ.get('POSTGRES_USER', '***REMOVED***'),
#     passwd=os.environ.get('POSTGRES_PASSWORD', '***REMOVED***'),
#     host=os.environ.get('POSTGRES_HOST', 'test_app_db_1'),
#     port=os.environ.get('POSTGRES_PORT', '5432'),
#     db=os.environ.get('POSTGRES_DB', 'testdb'))
# print(connectionString)
# connectionString = "postgresql://***REMOVED***:***REMOVED***@test_app_db_1/testdb"
app.config['SQLALCHEMY_DATABASE_URI'] = connectionString

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)
# db.create_all()

class Cand(db.Model):
    id = db.Column('cand_id', db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    secondname = db.Column(db.String(20))
    about = db.Column(db.String(200))

    def __init__(self, name, secondname, about):
        self.name = name
        self.secondname = secondname
        self.about = about


def database_initialization_sequence():
    db.create_all()
    test_rec = Cand(
            'Илья',
            'Самарцев',
            'Программист')

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


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
    print("Start:" + "01")
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
            print("ERROR:" + "DB")
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0', port=8080)
