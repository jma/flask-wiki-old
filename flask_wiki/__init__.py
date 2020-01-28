# -*- coding: utf-8 -*-
#
# This file is part of Flask-Wiki
# Copyright (C) 2020 RERO
#
# Flask-Wiki is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""This extension create a wiki from a tree directory."""

from flask import current_app
import os
from .views import blueprint
from werkzeug.middleware.shared_data import SharedDataMiddleware

class Wiki(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('WIKI_HOME', 'home')
        app.config.setdefault('WIKI_URL_PREFIX', '/wiki')
        app.config.setdefault('WIKI_CONTENT_DIR', './data')
        app.config.setdefault('WIKI_UPLOAD_FOLDER', os.path.join(app.config.get('WIKI_CONTENT_DIR'), 'files'))
        app.register_blueprint(
            blueprint,
            url_prefix=app.config.get('WIKI_URL_PREFIX')
        )
        app.add_url_rule(app.config.get('WIKI_URL_PREFIX') + '/files/<filename>', 'uploaded_files',
                 build_only=True)
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            app.config.get('WIKI_URL_PREFIX') + '/files':  app.config['WIKI_UPLOAD_FOLDER']
        })

