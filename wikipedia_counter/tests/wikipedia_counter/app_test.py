import unittest


from wikipedia_counter.app import WikipediaCounterApp
from wikipedia_counter.routes import flask_app


class AppTest(unittest.TestCase):
    def test_app(self):
        """Test whether a server can be initialized (but not run)"""
        options = {
            "bind": "127.0.0.1:8181",
            "workers": 1,
        }
        WikipediaCounterApp(flask_app, options)
