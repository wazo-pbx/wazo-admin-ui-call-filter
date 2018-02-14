# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_admin_ui.helpers.confd import confd
from wazo_admin_ui.helpers.service import BaseConfdService


class CallfilterService(BaseConfdService):
    resource_confd = 'call_filters'

    def create(self, resource):
        callfilter_id = super().create(resource)['id']
        self.update_user_recipients(callfilter_id, resource['recipients_user'])
        self.update_user_surrogates(callfilter_id, resource['surrogates_user'])

    def update(self, resource):
        super().update(resource)
        self.update_user_recipients(resource['id'], resource['recipients_user'])
        self.update_user_surrogates(resource['id'], resource['surrogates_user'])
        self.update_fallbacks(resource['id'], resource['fallbacks'])

    def update_user_recipients(self, callfilter_id, users):
        return confd.call_filters(callfilter_id).update_user_recipients(users)

    def update_user_surrogates(self, callfilter_id, users):
        return confd.call_filters(callfilter_id).update_user_surrogates(users)

    def update_fallbacks(self, callfilter_id, fallbacks):
        return confd.call_filters(callfilter_id).update_fallbacks(fallbacks)

    def list_sound(self):
        return confd.sounds.list()

    def list_sound_filename(self, sound_name):
        return confd.sounds.get(sound_name)

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
