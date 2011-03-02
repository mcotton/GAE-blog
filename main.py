#!/usr/bin/env python


import wsgiref.handlers, logging
import cgi, os, time, datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from usermodels import *  #I'm storing my models in usermodels.py


class MainHandler(webapp.RequestHandler):
  def get(self):
    render_template(self, 'templates/index.html')

class e(webapp.RequestHandler):
  def get(self):
    render_template(self, 'templates/expreso.html')
    
class a(webapp.RequestHandler):
  def get(self):
    render_template(self, 'templates/assist.html')
    
class o(webapp.RequestHandler):
  def get(self):
    render_template(self, 'templates/on-call.html')
    
class BlogHandler(webapp.RequestHandler):
  def get(self, resource=''):
  
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/blog/")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/blog/")
      admin_url_text = 'Login'
    
    #Did anything come in on the url /blog/:resource
    if resource:  
      posts = Blog().gql("where tag = :1 order by date desc", resource).fetch(10)
    else:
      posts = Blog().gql("order by date desc").fetch(10)
    
    #Build the SideBar
    tags = SideBar().gql("order by title asc").fetch(20)
    tags_list = []
    for t in tags:
      tags_list.append(t.title)
    
    
    template_values = {
      'tags': list(set(tags_list)),
      'resource': resource,
      'posts': posts,
      'admin': admin,
      'admin_url': admin_url,
      'admin_url_text': admin_url_text
    }
    
    render_template(self, 'templates/blog.html', template_values)
    
  def post(self, resource):
    if users.is_current_user_admin():
      b = Blog()
      s = SideBar()
      b.title = self.request.get("title")
      b.content = self.request.get("body")
      b.tag = self.request.get("category")
      s.path = self.request.get("category")
      s.title = self.request.get("category")
      #this is weird, but this is a batch put to the datastore
      updated = []
      updated.append(b)
      updated.append(s)
      db.put(updated)
    
    self.redirect("/blog/")
    
    
def render_template(call_from, template_name, template_values=dict()):
  path = os.path.join(os.path.dirname(__file__), template_name)
  call_from.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/expreso', e),
                                        ('/assist', a),
                                        ('/on-call', o),
                                        ('/blog/([^/]+)?', BlogHandler),
                                        ('/blog', BlogHandler)],
                                         debug=True)
                                         
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
