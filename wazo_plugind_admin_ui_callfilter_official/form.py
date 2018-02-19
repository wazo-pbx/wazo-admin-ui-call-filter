# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from wtforms.fields import (
    BooleanField,
    SubmitField,
    StringField,
    IntegerField,
    FormField,
    HiddenField,
    SelectMultipleField,
    FieldList
)
from wtforms.validators import InputRequired, NumberRange

from wazo_admin_ui.helpers.destination import DestinationField, DestinationHiddenField
from wazo_admin_ui.helpers.form import BaseForm, SelectField

bs_strategy_map = {
    'all-surrogates-then-all-recipients': l_('All secretaries, then boss'),
    'linear-surrogates-then-all-recipients': l_('Secretaries sequentially, then boss'),
    'all-recipients-then-linear-surrogates': l_('Boss, then secretaries sequentially'),
    'all-recipients-then-all-surrogates': l_('Boss, then all secretaries'),
    'all': l_('Boss and all secretaries')
}


class FallbacksForm(BaseForm):
    noanswer_destination = DestinationField(destination_label='')


class UserForm(BaseForm):
    uuid = HiddenField()
    firstname = HiddenField(l_('Firstname'))
    lastname = HiddenField(l_('Lastname'))


class UserRecipientsForm(UserForm):
    uuid = SelectField(l_('Boss'), choices=[], validators=[InputRequired])
    timeout = IntegerField(l_('Boss Timeout'))


class UserSurrogateForm(UserForm):
    id = HiddenField()
    funckey = HiddenField(l_('Extension'))


class UserSurrogatesForm(BaseForm):
    user_uuids = SelectMultipleField(l_('Secretaries'), choices=[], validators=[InputRequired])
    users = FieldList(FormField(UserSurrogateForm), min_entries=1)


class CallFilterForm(BaseForm):
    name = StringField(l_('Name'), validators=[InputRequired()])
    strategy = SelectField(l_('Ring Strategy'), choices=[(k, v) for k, v in bs_strategy_map.items()])
    caller_id_mode = SelectField(l_('Caller ID mode'), choices=[
        ('', l_('None')),
        ('prepend', l_('Prepend')),
        ('overwrite', l_('Overwrite')),
        ('append', l_('Append'))
    ])
    caller_id_name = StringField(l_('Caller ID name'))
    source = SelectField(l_('Call From'), choices=[
        ('internal', l_('Internal')),
        ('external', l_('External')),
        ('all', l_('All'))
    ])
    fallbacks = FormField(FallbacksForm)
    surrogates_timeout = IntegerField(l_('Secretaries ringing time'))
    recipients_user = FormField(UserRecipientsForm)
    surrogates_user = FormField(UserSurrogatesForm)
    description = StringField(l_('Description'))
    enabled = BooleanField(l_('Enabled'))
    submit = SubmitField(l_('Submit'))


class CallFilterDestinationForm(BaseForm):
    set_value_template = '{callfilter_name}'

    callfilter_id = SelectField(l_('CallFilter'), [InputRequired()], choices=[])
    callfilter_name = DestinationHiddenField()
    ring_time = IntegerField(l_('Ring Time'), [NumberRange(min=0)])
