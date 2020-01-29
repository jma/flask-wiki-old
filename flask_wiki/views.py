# -*- coding: utf-8 -*-
#
# This file is part of Flask-Wiki
# Copyright (C) 2020 RERO
#
# Flask-Wiki is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Views to respond to HTTP requests."""

from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from .api import current_wiki, Processor
from .forms import EditorForm

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


@blueprint.route('/edit/<path:url>/', methods=['GET', 'POST'])
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('wiki/editor.html', form=form, page=page)


@blueprint.route('/preview/', methods=['POST'])
def preview():
    data = {}
    processor = Processor(request.form['body'])
    print(request.form.get('body'))
    data['html'], data['body'], data['meta'], data['toc'] = processor.process()
    return data['html']


@blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('wiki/404.html'), 404
