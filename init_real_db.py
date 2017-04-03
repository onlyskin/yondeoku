from yondeokuApp import app, db

ctx = app.app_context()
ctx.push()

db.init_app(app)
db.create_all()
