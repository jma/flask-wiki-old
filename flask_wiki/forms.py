# -*- coding: utf-8 -*-
#
# This file is part of Flask-Wiki
# Copyright (C) 2020 RERO
#
# Flask-Wiki is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Forms class."""

from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import InputRequired
from flask_babel import gettext as _


class EditorForm(Form):
    title = TextField(_('title'), [InputRequired()])
    body = TextAreaField(_('body'), [InputRequired()])
    tags = TextField(_('tags'))