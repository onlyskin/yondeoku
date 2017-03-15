from yondeokuApp import db, app, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/fake.db'

ctx = app.app_context()
ctx.push()

db.create_all()

fakeUser = User(username='fakeUser', password='password')
db.session.add(fakeUser)
db.session.commit()

