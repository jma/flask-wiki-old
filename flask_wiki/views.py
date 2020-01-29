# -*- coding: utf-8 -*-
#
# This file is part of Flask-Wiki
# Copyright (C) 2020 RERO
#
# Flask-Wiki is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Views to respond to HTTP requests."""

import os
import glob
from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request, jsonify
from .api import current_wiki, Processor
from .forms import EditorForm
from werkzeug.utils import secure_filename


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


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['WIKI_UPLOAD_FOLDER'], filename))
            return url_for('uploaded_files', filename=filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@blueprint.route('/files', methods=['GET', 'POST'])
def list_files():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            output_filename = os.path.join(current_app.config['WIKI_UPLOAD_FOLDER'], filename)
            if os.path.isfile(output_filename):
                flash('File already exists', category='danger')
            else:
                file.save(output_filename)
    files = [os.path.basename(f) for f in sorted(glob.glob('/'.join([current_app.config.get('WIKI_UPLOAD_FOLDER'), '*'])), key=os.path.getmtime)]
    return render_template('wiki/files.html', files=files)

@blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('wiki/404.html'), 404
