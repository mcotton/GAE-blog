#!/usr/bin/env python


import os

# They are changing Django version, need to include this
# http://code.google.com/appengine/docs/python/tools/libraries.html#Django
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template

import wsgiref.handlers, logging
import cgi, time, datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from usermodels import *  #I'm storing my models in usermodels.py


class MainHandler(webapp.RequestHandler):
  def get(self):
    render_template(self, 'templates/index.html')
    
    
class PartialHandler(webapp.RequestHandler):
  def get(self, resource=''):
    #Did anything come in on the url /partial/:resource
    if resource:  
      posts = Blog().gql("where tag = :1 order by date desc", resource).fetch(1)
      if posts:
        for p in posts:
          self.response.out.write('<div class=\"block-3\" id=\"partial\"><p>' + p.content + '</p></div>')
      else:
        self.response.out.write('There is nothing in the database about ' + resource)  
    else:
      self.response.out.write('Content not found')
    
    
class DeleteHandler(webapp.RequestHandler):
  def get(self, resource=''):
    #check if there is a key
    if resource:
      #check if they are allowed to delete things
      if users.is_current_user_admin():  
        b = Blog().get(resource)
        if b:
          b.delete() 
        
    self.redirect("/blog")
    
class BlogHandler(webapp.RequestHandler):
  def get(self, resource=''):
  
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/blog")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/blog")
      admin_url_text = 'Login'
    
    #Did anything come in on the url /blog/:resource
    if resource:  
      posts = Blog().gql("where tag = :1 order by date desc", resource).fetch(10)
      if len(posts) == 0:
        posts = Blog().gql("order by date desc").fetch(10)
    else:
      posts = Blog().gql("order by date desc").fetch(10)
    
    #Build the SideBar
    tags = SideBar().gql("order by title asc")
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
      b.content = self.request.get("html_body")
      b.markdown = self.request.get("user_input")
      b.tag = self.request.get("category").lower()
      s.path = self.request.get("category").lower()
      s.title = self.request.get("category").lower()
      #this is weird, but this is a batch put to the datastore
      updated = []
      updated.append(b)
      updated.append(s)
      db.put(updated)
    
    self.redirect("/blog")


class EditHandler(webapp.RequestHandler):
  def get(self, resource=''):
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/blog")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/blog")
      admin_url_text = 'Login'
  
    #reject anything that doesn't have a key
    if resource == '' or not admin:
      self.redirect("/blog")
      
    else: 
      b = Blog().get(resource)
      if b is None:
        self.redirect('/blog')
      else:
        template_values = {
          'resource': resource,
          'b': b,
          'admin': admin,
          'admin_url': admin_url,
          'admin_url_text': admin_url_text
          }
    
        render_template(self, 'templates/edit.html', template_values)
      

  def post(self, resource=''):
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/blog")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/blog")
      admin_url_text = 'Login'
      
    #reject anything that doesn't have a key
    if resource == '':
      self.redirect("/blog")
      
    b = Blog().get(resource)
    #check if it found anything
    if b and admin:
      b.title = self.request.get("title")
      b.content = self.request.get("html_body")
      b.markdown = self.request.get("user_input")
      b.tag = self.request.get("category").lower()
      b.put()
      
    self.redirect("/blog")


class PostHandler(webapp.RequestHandler):
  def get(self, resource=''):
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/blog")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/blog")
      admin_url_text = 'Login'
  
    #reject anything that doesn't have a key
    if resource == '':
      self.redirect("/blog")
    
    else:
      b = Blog().get(resource)
      template_values = {
        'resource': resource,
        'b': b,
        'admin': admin,
        'admin_url': admin_url,
        'admin_url_text': admin_url_text
        }
    
      render_template(self, 'templates/post.html', template_values)





    
def render_template(call_from, template_name, template_values=dict()):
  path = os.path.join(os.path.dirname(__file__), template_name)
  call_from.response.out.write(template.render(path, template_values))

def isLocal():
    return os.environ["SERVER_NAME"] in ("localhost") 

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/delete/([^/]+)?', DeleteHandler),
                                        ('/blog/([^/]+)?', BlogHandler),
                                        ('/blog', BlogHandler),
                                        ('/partial/([^/]+)?', PartialHandler),
                                        ('/edit', BlogHandler),
                                        ('/edit/([^/]+)?', EditHandler),
                                        ('/post', BlogHandler),
                                        ('/post/([^/]+)?', PostHandler)],
                                         debug=isLocal())
                                         
  from gae_mini_profiler import profiler
  application = profiler.ProfilerWSGIMiddleware(application)

  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
