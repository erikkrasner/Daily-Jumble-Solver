#!/usr/bin/env python

import os
import cgi
import datetime
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#import json

class HomePage(webapp.RequestHandler):
    def get(self):
        html = template.render('home.html',{})
        self.response.out.write(html)

class AjaxHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("hello world")

application = webapp.WSGIApplication([
    ('/',HomePage),
    ('/solve',AjaxHandler)
    ],debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)
    
