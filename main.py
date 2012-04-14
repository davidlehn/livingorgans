import hashlib
import json
import logging
import os
import random
import re
import sys
import urllib
import datetime

#sys.path[0:0] = ['lib']

import webapp2
from webapp2 import Route
from webapp2_extras import routes
from webapp2_extras import jinja2
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import deferred
from google.appengine.api import files

logging.getLogger().setLevel(logging.DEBUG)

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, **template_args):
        self.response.write(self.jinja2.render_template(filename, **template_args))

    def render_json(self, data, debug=False):
        separators = (',',':')
        indent = None
        if debug:
            indent = 2
            separators = (', ',': ')
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(data, indent=indent, separators=separators))

class ResourceHandler(BaseHandler):
    def __init__(self, *args, **kwds):
        super(ResourceHandler, self).__init__(*args, **kwds)
        self._type_map = {
            'text/html': self.get_html,
            'application/json': self.get_json,
        }
        self._types = self._type_map.keys()

    def get(self, *args, **kwds):
        ct = self.request.accept.best_match(self._types)
        get_type = self._type_map[ct]
        return get_type(*args, **kwds)

    def get_html(self, *args, **kwds):
        self.abort(500)

    def get_json(self, *args, **kwds):
        self.abort(500)

class HomeHandler(BaseHandler):
    def get(self):
        pairs = Pair.query().fetch(100)
        args = {
            'pairs': pairs,
        }
        #self.render_template('index.html', name=self.request.get('name'))
        self.render_template('home.html', **args)

class Person(ndb.Model):
    name = ndb.StringProperty()
    contact = ndb.StringProperty()
    blood_type = ndb.StringProperty()

    @staticmethod
    def clear():
        q = Person.query()
        data = q.fetch(100)
        while len(data):
            for d in data:
                d.delete()
            data = q.fetch(100)

class Pair(ndb.Model):
    donor = ndb.KeyProperty(required=True, kind=Person)
    recipient = ndb.KeyProperty(required=True, kind=Person)

    @staticmethod
    def clear():
        q = Pair.query()
        data = q.fetch(100)
        while len(data):
            for d in data:
                d.delete()
            data = q.fetch(100)

    @staticmethod
    def add(dn, dc, dbt, rn, rc, rbt):
        d = Person(name=dn, contact=dc, blood_type=dbt)
        r = Person(name=dn, contact=dc, blood_type=dbt)
        d.put()
        r.put()

        first, last = Pair.allocate_ids(1)
        p = Pair(id=str(first))
        p.donor = d.key
        p.recipient = r.key
        p.put()

class PairsHandler(BaseHandler):
    def get(self):
        pairs = Pair.query().fetch(100)
        args = {
            'pairs': pairs,
        }
        #self.render_template('index.html', name=self.request.get('name'))
        self.render_template('pairs-all.html', **args)

    def post(self):
        Pair.add(
           self.request.get(pre + "d_name"),
           self.request.get(pre + "d_contact"),
           self.request.get(pre + "d_blood_type"),
           self.request.get(pre + "r_name"),
           self.request.get(pre + "r_contact"),
           self.request.get(pre + "r_blood_type"))
        logging.info("pair created")
        self.redirect('/pairs')

class AddPairHandler(BaseHandler):
    def get(self):
        args = {}
        self.render_template('pairs-add.html', **args)

class PairHandler(ResourceHandler):
    def get(self, pair_id):
        pair_id = int(pair_id)
        key = ndb.Key('Pair', pair_id)
        pair = key.get()
        args = {
            'pair': pair,
        }
        self.render_template('pairs-pair.html', **args)

    def get_html(self, pair_id):
        pair = Pair.get_by_id(pair_id)
        args = {
            'pair': pair,
        }
        self.render_template('pair-pair.html', **args)

    def get_json(self, fc):
        pair = Pair.get_by_id(pair_id)
        data = {
            '@id': '/pairs/' + pair.key.id(),
            '@type': 'Pair',
            'pair': pair,
        }
        self.render_json(data)

    def post(self):
        return # FIXME
        p = Pair()
        p.foo = self.request.get("...")
        p.put()
        logging.info("pair created")

class EditPairHandler(BaseHandler):
    def get(self):
        args = {}
        self.render_template('pair-edit.html', **args)

def find_groups(pairs):
   return []

class MatchesHandler(BaseHandler):
    def get(self):
        q = Pair.query()
        pairs = q.fetch(100)
        _pairs = []
        #while len(pairs):
        #    for p in pairs:
        #        d = p.donor.get()
        #        r = p.recipient.get()
        #        _pairs.append({
        #            'donor': {
        #                'name': d.name,
        #                'contact': d.contact,
        #                'blood_type': d.blood_type,
        #            },
        #            'recipient': {
        #                'name': r.name,
        #                'contact': r.contact,
        #                'blood_type': r.blood_type,
        #            }
        #        })
        #    pairs = q.fetch(100)

        groups = find_groups(_pairs)

        args = {
            'groups': groups,
        }
        self.render_template('matches.html', **args)

class InfoHandler(BaseHandler):
    def get(self, page):
        self.render_template('%s.html' % (page))

class Test1(BaseHandler):
    def post(self):
        logging.info('TEST1')
        Pair.clear()
        Person.clear()
        Pair.add(
           'Donor 1', '@D1', 'A',
           'Recipient 1', '@R1', 'AB')
        Pair.add(
           'Donor 2', '@D2', 'B',
           'Recipient 2', '@R2', 'A')
        self.redirect('/pairs')

class Test2(BaseHandler):
    def post(self):
        pass

class Test3(BaseHandler):
    def post(self):
        pass

routes = [
        Route(r'/', handler='main.HomeHandler'),
        Route(r'/pairs', handler='main.PairsHandler'),
        routes.PathPrefixRoute(r'/pairs', [
            Route(r'/', handler='main.PairsHandler'),
            Route(r'/-/add', handler='main.AddPairHandler'),
            Route(r'/<pair>/edit', handler='main.EditPairHandler'),
            Route(r'/<pair>/matches', handler='main.PairMatchesHandler'),
            Route(r'/<pair>', handler='main.PairHandler'),
            Route(r'/-/tests/1', handler='main.Test1'),
            Route(r'/-/tests/2', handler='main.Test2'),
            Route(r'/-/tests/3', handler='main.Test3'),
        ]),
        Route(r'/matches', 'main.MatchesHandler'),
        Route(r'/<:(about|contact|legal|privacy|terms|help|api)>', 'main.InfoHandler'),
]
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
config = {}
config['webapp2_extras.jinja2'] = {
    'template_path': ''
}

app = ndb.toplevel(webapp2.WSGIApplication(
            routes=routes, debug=debug, config=config))