from google.appengine.ext import db

  
class Blog(db.Model):
  date = db.DateTimeProperty(auto_now=True)
  title = db.StringProperty()
  tag = db.StringProperty()
  content = db.TextProperty()
  
class SideBar(db.Model):
  title = db.StringProperty()
  path = db.StringProperty()