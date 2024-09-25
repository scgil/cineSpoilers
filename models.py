from google.appengine.ext import ndb

class MovieQuote(ndb.Model):

    quote = ndb.StringProperty()
    movie = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def query_moviequote(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.last_touch_date_time)