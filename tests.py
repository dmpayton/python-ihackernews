#!/usr/bin/env python

import unittest
from ihackernews import iHackerNewsAPI, iHackerNewsResponse

TEST_USERNAMES = ('dmpayton', 'grellas', 'patio11', 'pg')

class iHackerNewsTests(unittest.TestCase):
    def setUp(self):
        self.hn = iHackerNewsAPI()

    def validate_response(self, response):
        self.assertIsInstance(response, iHackerNewsResponse)
        self.assertEqual(response.response.status_code, 200)

    def test_getid(self):
        url = 'http://edweissman.com/53640595' # Thanks edw519!
        response = self.hn.getid(url=url)
        self.validate_response(response)
        self.assertIn(2564099, response.data)

    def test_post(self):
        post_id = 89615 # Ah, memories... Wish the gang was still together!
        response = self.hn.post(post_id)
        self.validate_response(response)
        self.assertEqual(response.data.get('id'), post_id)

    def test_page(self):
        response = self.hn.page()
        self.validate_response(response)
        if response.data.get('nextId'):
            next_page = self.hn.page(response.data['nextId'])
            self.validate_response(next_page)

    def test_new(self):
        response = self.hn.new()
        self.validate_response(response)
        if response.data.get('nextId'):
            next_page = self.hn.new(response.data['nextId'])
            self.validate_response(next_page)

    def test_ask(self):
        response = self.hn.ask()
        self.validate_response(response)
        if response.data.get('nextId'):
            next_page = self.hn.ask(response.data['nextId'])
            self.validate_response(next_page)

    def test_newcomments(self):
        response = self.hn.newcomments()
        self.validate_response(response)

    def test_profile(self):
        for username in TEST_USERNAMES:
            response = self.hn.profile(username)
            self.assertEqual(response.data.get('username'), username)

    def test_by(self):
        for username in TEST_USERNAMES:
            response = self.hn.by(username)
            self.validate_response(response)
            if response.data.get('nextId'):
                next_page = self.hn.by(username, response.data['nextId'])
                self.validate_response(next_page)

    def test_threads(self):
        for username in TEST_USERNAMES:
            response = self.hn.threads(username)
            self.validate_response(response)


if __name__ == '__main__':
    unittest.main()
