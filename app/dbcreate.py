from app import db, cand

db.create_all()


test_rec = cand(
        'Иван',
        'Иванов',
        'Инженер',
        '12345'
        )


db.session.add(test_rec)
db.session.commit()
