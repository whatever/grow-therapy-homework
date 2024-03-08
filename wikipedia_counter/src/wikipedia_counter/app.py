import gunicorn.app.base


class WikipediaCounterApp(gunicorn.app.base.BaseApplication):
    """
    WikipediaCounterApp is a custom Gunicorn application
    This is really just because I hate running my apps with:
    `gunicorn wikipedia_counter.server:app`
    """

    def __init__(self, app, options=None):
        """Initialize the application with an app"""

        self.options = options or {}
        self.application = app
        super(WikipediaCounterApp, self).__init__()

    def load_config(self):
        """Override the default configuration"""

        config = dict([
            (key, value)
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        ])

        for key, value in config.items():
            self.cfg.set(key.lower(), value)
        return

    def load(self):
        """Return the application"""

        return self.application
