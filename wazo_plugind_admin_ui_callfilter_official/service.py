# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.confd import confd
from wazo_admin_ui.helpers.service import BaseConfdService


class CallFilterService(BaseConfdService):
    resource_confd = 'call_filters'

    def create(self, resource):
        callfilter_id = super().create(resource)['id']
        confd.call_filters(callfilter_id).update_user_recipients(resource['recipients_user'])
        confd.call_filters(callfilter_id).update_user_surrogates(resource['surrogates_user'])

    def update(self, resource):
        super().update(resource)
        confd.call_filters(resource['id']).update_user_recipients(resource['recipients_user'])
        confd.call_filters(resource['id']).update_user_surrogates(resource['surrogates_user'])
        confd.call_filters(resource['id']).update_fallbacks(resource['fallbacks'])

    def list_sound(self):
        return confd.sounds.list()

    def find_sound_by_path(self, sound_path):
        sounds = self.list_sound()['items']
        for sound in sounds:
            for file_ in sound['files']:
                for format_ in file_['formats']:
                    if sound['name'] == 'system':
                        if file_['name'] == sound_path:
                            return file_, format_
                    else:
                        if format_['path'] == sound_path:
                            return file_, format_
        return None, None

    def get_extensions_features_by_type(self, extension_feature_type):
        extensions_features = confd.extensions_features.list()['items']
        for extension_feature in extensions_features:
            if extension_feature['feature'] == extension_feature_type:
                return extension_feature

    def get_user_by_uuid(self, uuid):
        return confd.users.get(uuid)
