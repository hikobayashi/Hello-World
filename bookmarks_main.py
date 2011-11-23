import os,logging
import wsgiref.handlers
from google.appengine.ext import db, webapp
from google.appengine.dist import use_library
use_library('django', '1.2')
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
    def post(self):
        self.redirect("/")

class AddBookmark(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),"bookmark_add.html")
        data = {}
        self.response.out.write(template.render(path,data))

    def post(self):
        url = self.request.POST['url']
        title = self.request.POST['title']
        bookmark = Bookmark(url=url,title=title)
        bookmark.comment=self.request.POST['comment']
        bookmark.put()
        
        self.redirect("/edit/%d/" % (bookmark.key().id()))
        

class EditBookmark(webapp.RequestHandler):
    def get(self,bookmark_id):
        bookmark_id=int(bookmark_id)
        bookmark = Bookmark.get_by_id(bookmark_id)
        logging.info(bookmark.key().id())
        data = {
                'bookmark':bookmark,
                'bookmark_id':bookmark_id,
                }
        path = os.path.join(os.path.dirname(__file__),"bookmark_edit.html")
        self.response.out.write(template.render(path,data))
        
    def post(self,bookmark_id):
        bookmark_id=int(bookmark_id)
        bookmark = Bookmark.get_by_id(bookmark_id)
        bookmark.url = self.request.POST['url']
        bookmark.title = self.request.POST['title']
        bookmark.comment=self.request.POST['comment']
        bookmark.put()
        
        self.redirect("/")

class DeleteBookmark(webapp.RequestHandler):
    def post(self,bookmark_id):
        bookmark = Bookmark.get_by_id(int(bookmark_id))

        if bookmark:
            logging.info(bookmark.title)
            bookmark.delete()
        self.redirect("/")

def main():
    application = webapp.WSGIApplication([
                                          ('/',ListBookmark),
                                          ('/add/',AddBookmark),
                                          ('/edit/(\d+)/',EditBookmark),
                                          ('/delete/(\d+)/',DeleteBookmark)
                                          ],debug=True)
    wsgiref.handlers.CGIHandler().run(application)
