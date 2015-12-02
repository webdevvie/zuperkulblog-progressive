#!/usr/bin/env python
#
# Copyright 2015 Google Inc.
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

__author__ = 'Eric Bidelman <ebidel@>'

import os
import sys
import webapp2
import jinja2
import http2push as http2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), 'dist/static')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
    variable_start_string='{{{',
    variable_end_string='}}}')


class ListHandler(http2.PushHandler):

    @http2.push('push_manifest.json')
    def get(self, category=None):
        if category is None:
            category = 'art'
        self.push_urls[u'/data/' + category + '.json'] = 1;
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

class SlugHandler(http2.PushHandler):

    @http2.push('push_manifest.json')
    def get(self, slug):
        self.push_urls[u'/data/' + slug + '.json'] = 1;
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', ListHandler),
    ('/(.*)/list', ListHandler),
    ('/.*/detail/(.*)', SlugHandler)
], debug=True)
