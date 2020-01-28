# -*- coding: utf-8 -*-
#
# This file is part of Flask-Wiki
# Copyright (C) 2020 RERO
#
# Flask-Wiki is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Views to respond to HTTP requests."""

from flask import Blueprint, render_template, current_app
from .api import current_wiki

blueprint = Blueprint(
    'wiki',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/')
def index():
    return display(current_app.config.get('WIKI_HOME'))

@blueprint.route('/<path:url>/')
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('wiki/index.html', page=page)