#!/usr/bin/env python

__version__ = (1, 0, 0)

import requests
import urllib
import urlparse

## Try to import a JSON library from somewhere, anywhere
try:
    ## Python >= 2.6
    import json
except ImportError:
    try:
        ## Python < 2.6
        import simplejson as json
    except ImportError:
        try:
            ## Django and/or Google App Engine
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError("A suitable JSON library could not be found")


class iHackerNewsException(Exception):
    pass


class iHackerNewsResponse(object):
    '''A simple Response class to hold the original response and parse the JSON data '''
    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.response.url)

    @property
    def data(self):
        ## Parse the JSON data and store it on the
        if not hasattr(self, '_data'):
            try:
                self._data = json.loads(self.response.content)
            except ValueError:
                raise iHackerNewsException('No JSON data could be parsed from the response.')
        return self._data


class iHackerNewsAPI(object):
    '''The iHackerNews API class'''
    API_URL = 'http://api.ihackernews.com/'
    TIMEOUT = 15.0
    USER_AGENT = 'python-ihackernews/v%s.%s.%s' % __version__

    ## Core

    def build_url(self, *args, **kwargs):
        '''Build the API URL to request. *args builds the URL path, **kwargs builds the GET params.'''
        path = '/'.join([str(x) for x in args if x])
        url = urlparse.urljoin(self.API_URL, path)
        url += '?%s' % urllib.urlencode(kwargs) if kwargs else ''
        return url

    def make_request(self, *args, **kwargs):
        '''Make a request to the API'''
        api_url = self.build_url(*args, **kwargs)
        try:
            response = requests.get(api_url, timeout=self.TIMEOUT, headers={
                'User-Agent': self.USER_AGENT
                })
        except requests.Timeout:
            raise iHackerNewsException('The API request has timed out.')
        if response.status_code != 200:
            raise iHackerNewsException('The API endpoint returned a non-200 status code.')
        return iHackerNewsResponse(response)

    ## General

    def getid(self, url):
        '''Find submitted articles by URL'''
        return self.make_request('getid', url=url)

    def post(self, post_id):
        '''Retrieve Post (includes url, title, comments, etc...)'''
        return self.make_request('post', post_id)

    ## Pages

    def page(self, next=None):
        '''Retrieve Front Page News'''
        return self.make_request('page', next)

    def new(self, next=None):
        '''Retrieve Front Page News'''
        return self.make_request('new', next)

    def ask(self, next=None):
        '''Retrieve AskHN Posts'''
        return self.make_request('ask', next)

    def newcomments(self):
        '''Retrieve Newly Submitted Comments'''
        return self.make_request('newcomments')

    ## User data

    def profile(self, user):
        '''Retrieve a user's profile'''
        return self.make_request('profile', user)

    def by(self, user, next=None):
        '''Retrieve Posts Submitted By User'''
        return self.make_request('by', user, next)

    def threads(self, user):
        '''Retrieve Comment Threads for a user'''
        return self.make_request('threads', user)
