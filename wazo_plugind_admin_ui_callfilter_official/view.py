# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_babel import lazy_gettext as l_
from flask_menu.classy import classy_menu_item
from requests.exceptions import HTTPError

from wazo_admin_ui.helpers.classful import BaseView, LoginRequiredView
from wazo_admin_ui.helpers.classful import extract_select2_params, build_select2_response
from wazo_admin_ui.helpers.destination import listing_urls

from .form import CallFilterForm, bs_strategy_map


class CallFilterView(BaseView):
    form = CallFilterForm
    resource = 'callfilter'

    @classy_menu_item('.callfilters', l_('BS Filters'), order=8, icon='filter')
    def index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resource_list,
                               listing_urls=listing_urls,
                               bs_strategy_map=bs_strategy_map)

    def _map_resources_to_form(self, resource):
        surrogates_user = {}
        surrogates_user['user_uuids'] = [user['uuid'] for user in resource['surrogates']['users']]
        surrogates_user['users'] = self._build_surrogates_user(resource['surrogates']['users'])
        recipients_user = self._build_recipients_user(resource['recipients']['users'])
        fallbacks = self._build_sound(resource['fallbacks'])
        form = self.form(
            data=resource,
            fallbacks=fallbacks,
            surrogates_user=surrogates_user,
            recipients_user=recipients_user,
        )
        return form

    def _build_surrogates_user(self, surrogates_user):
        for surrogate_user in surrogates_user:
            user = self.service.get_user_by_uuid(surrogate_user['uuid'])
            surrogate_user['id'] = user['id']
        return surrogates_user

    def _build_sound(self, fallbacks):
        if not fallbacks['noanswer_destination'] or fallbacks['noanswer_destination']['type'] != 'sound':
            return
        file_, format_ = self.service.find_sound_by_path(fallbacks['noanswer_destination']['filename'])
        if file_:
            fallbacks['noanswer_destination']['name'] = file_['name']
            fallbacks['noanswer_destination']['format'] = format_['format']
            fallbacks['noanswer_destination']['language'] = format_['language']
        return fallbacks

    def _build_recipients_user(self, recipients_user):
        for user in recipients_user:
            return user
        return None

    def _populate_form(self, form):
        sounds = self.service.list_sound()
        form.fallbacks.form.noanswer_destination.choices = self._build_set_choices_sound(sounds)
        form.surrogates_user.user_uuids.choices = self._build_set_choices_surrogates_user(form.surrogates_user.users)
        form.recipients_user.uuid.choices = self._build_set_choices_recipients_users([form.recipients_user])
        return form

    def _build_set_choices_recipients_users(self, users):
        results = []
        for user in users:
            if user.lastname.data:
                text = '{} {}'.format(user.firstname.data, user.lastname.data)
            else:
                text = user.firstname.data
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_surrogates_user(self, users):
        extension_features_bsfilter = self.service.get_extensions_features_by_type('bsfilter')
        bsfilter_extension = None
        if extension_features_bsfilter:
            bsfilter_extension = extension_features_bsfilter['exten'][1:-1]
        results = []
        for user in users:
            text = '{}{}{}'.format(
                user.firstname.data,
                ' {}'.format(user.lastname.data) if user.lastname.data else '',
                ' ({}{})'.format(bsfilter_extension, user['id'].data) if bsfilter_extension else '',
            )
            results.append((user.uuid.data, text))
        return results

    def _build_set_choices_sound(self, sounds):
        results = [('', l_('None'))]
        for sound in sounds['items']:
            for file_ in sound['files']:
                for format_ in file_['formats']:
                    name = format_['path'] if sound['name'] != 'system' else file_['name']
                    label = self._prepare_sound_filename_label(file_, format_)
                    results.append((name, label))
        return results

    def _prepare_sound_filename_label(self, file_, format_):
        return '{}{}{}'.format(
            file_['name'],
            ' [{}]'.format(format_['format']) if format_['format'] else '',
            ' ({})'.format(format_['language']) if format_['language'] else '',
        )

    def _map_form_to_resources(self, form, form_id=None):
        resource = super()._map_form_to_resources(form, form_id)
        resource['recipients_user'] = [resource['recipients_user']]
        resource['surrogates_user'] = [{'uuid': uuid} for uuid in resource['surrogates_user']['user_uuids']]
        return resource


class CallFilterListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        callfilters = self.service.list(**params)
        results = [{'id': callfilter['id'], 'text': callfilter['name']} for callfilter in callfilters['items']]
        return jsonify(build_select2_response(results, callfilters['total'], params))


class CallFilterListingUserSurrogatesView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        users = self.service.list_user(**params)
        extension_features_bsfilter = self.service.get_extensions_features_by_type('bsfilter')
        bsfilter_extension = None
        if extension_features_bsfilter:
            bsfilter_extension = extension_features_bsfilter['exten'][1:-1]
        results = []
        for user in users['items']:
            text = '{}{}{}'.format(
                user['firstname'],
                ' {}'.format(user['lastname']) if user['lastname'] else '',
                ' ({}{})'.format(bsfilter_extension, user['id']) if bsfilter_extension else '',
            )

            results.append({'id': user['uuid'], 'text': text})

        return jsonify(build_select2_response(results, users['total'], params))
