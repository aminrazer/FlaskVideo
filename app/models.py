from app import db
import datetime

class video(db.Model):
	__tablename__ = 'Video'
	id = db.Column(db.Integer, primary_key = True)
	Title = db.Column(db.String(64), index = True)
	Description =  db.Column(db.String(120),index = True)
	IP = db.Column(db.String(64))
	location = db.Column(db.String(64))
	Created = db.Column(db.DateTime, default=datetime.datetime.now)
	Views = db.Column(db.Integer,index = True)
	Rating = db.Column(db.Integer,index = True)
	Duration = db.Column(db.String(10),index = True)

	def __repr__(self):
		return '<video %r>' %(self.Title)
# class post(db.Model):
# 	__tablename__ = 'post'
# 	id = db.Column(db.Integer, primary_key = True)
# 	link =  db.Column(db.String(120),index = True)
# 	def __repr__(self):
# 		return '<post %r>' %(self.link)	
class posting(db.Model):
	__tablename__ = 'Posting'
	id = db.Column(db.Integer, primary_key = True)
	link =  db.Column(db.String(120),index = True)
	def __repr__(self):
		return '<post %r>' %(self.link)	