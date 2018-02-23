# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_listing_url

from .service import CallFilterService
from .view import CallFilterView, CallFilterListingView, CallFilterListingUserSurrogatesView

call_filter = create_blueprint('call_filter', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        CallFilterView.service = CallFilterService()
        CallFilterView.register(call_filter, route_base='/callfilters')
        register_flaskview(call_filter, CallFilterView)

        CallFilterListingView.service = CallFilterService()
        CallFilterListingView.register(call_filter, route_base='/callfilters_listing')

        CallFilterListingUserSurrogatesView.service = CallFilterService()
        CallFilterListingUserSurrogatesView.register(call_filter, route_base='/callfilters_listing_surrogates')

        register_listing_url('call_filter', 'call_filter.CallFilterListingView:list_json')
        register_listing_url('user_surrogates', 'call_filter.CallFilterListingUserSurrogatesView:list_json')

        core.register_blueprint(call_filter)
