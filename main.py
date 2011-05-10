#!/usr/bin/env python

import os
import cgi
import datetime
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class HomePage(webapp.RequestHandler):
    def get(self):
        html = template.render('home.html',{})
        self.response.out.write(html)

class DisplaySolutions(webapp.RequestHandler):
    def post(self):
        html = template.render('display_solutions.html',{})
        self.response.out.write(html)

application = webapp.WSGIApplication([
    ('/',HomePage),
    ('/display',DisplaySolutions)
    ],debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)
    
