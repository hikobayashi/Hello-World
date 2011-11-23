import os
import wsgiref.handlers
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template

class Bookmark(db.Model):
    title = db.StringProperty(required=True)
    url=db.LinkProperty(required=True)
    comment = db.TextProperty()
    
class ListBookmark(webapp.RequestHandler):
    def get(self):
        bookmarks = Bookmark.all()
        data = {'bookmarks':bookmarks}
        path = os.path.join(os.path.dirname(__file__),"bookmark_list.html")
        self.response.out.write(template.render(path,data))

class AddBookmark(webapp.RequestHandler):
    

class EditBookmark(webapp.RequestHandler):
    

class DeleteBookmark(webapp.RequestHandler):
    

def main():
    application = webapp.WSGIApplication([
                                          ('/',ListBookmark),
                                          ('/add/',AddBookmark),
                                          ('/edit/(\d+)/',EditBookmark),
                                          ('/delete/(\d+)/',DeleteBookmark)
                                          ],debug=True)
    wsgiref.handlers.CGIHandler().run(application)