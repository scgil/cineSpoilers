#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import logging
from google.appengine.ext import ndb
import jinja2
import webapp2

from models import MovieQuote

jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

# Using parent and ancestor
# When a Datastore entity is "put" into the Datastore really what happens
# is an event is created to do the "put" eventually, but flow is returned
# for speed reasons immediately (the real "put" is slow and done later on
# another thread). Then the page was reloading before the "put" actually
# finished and new quotes weren't displayed.
#We added a parent key to all MovieQuote entities, then did an Ancesotr Query
# for entities that had that parent key. Ancestor Queries will look for unfinished
# events within the entity group and wait for them to complete before running the query.
#If you had a million users you wouldn't want to lock down the entire Datastore using a single
# shared parent for all users. If you were worried about scaling to milllions of people there needs
# to be a more clever mechanism in place where there are MANY entity groups using different parent keys if Strong Consistency
# is required.

class MovieQuotesPage(webapp2.RequestHandler):
    def get(self):
        #Recupero el objeto de la DATA STORE y el orden segun el tiempo y en orden inverso poniendo el mens

        ancestor_key = ndb.Key("Entity", "moviequote_root")

        moviequotes_query = MovieQuote.query_moviequote(ancestor_key).fetch(20)

        #Cargo la plantilla

        template = jinja_env.get_template("templates/moviequotes.html")

        #Imprimo la plantilla y paso como parametros el objeto en forma de diccionario
        self.response.out.write(template.render({"moviequotes_query": moviequotes_query}))

class InsertQuoteAction(webapp2.RequestHandler):

    def post(self):
        if self.request.get("entity_key"):

            moviequote_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            moviequote = moviequote_key.get()
            moviequote.quote = self.request.get("quote")
            moviequote.movie = self.request.get("movie")
            moviequote.put()
        else:
            quote = self.request.get("quote")
            movie = self.request.get("movie")
            new_moviequote = MovieQuote(parent=ndb.Key("Entity", "moviequote_root"), quote=quote, movie=movie)

            #Guardar el objeto en la DATA STORE

            new_moviequote.put()

    #Volver a donde ha sido enviado

        self.redirect(self.request.referer)

class DeleteQuoteAction(webapp2.RequestHandler):

    def post(self):

        moviequote_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        moviequote_key.delete()
        self.redirect(self.request.referer)


app = webapp2.WSGIApplication([
    ("/", MovieQuotesPage),
    ("/insertquote", InsertQuoteAction),
    ("/deletequote", DeleteQuoteAction)
], debug=True)
