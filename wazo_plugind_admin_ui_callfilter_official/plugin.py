# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.destination import register_listing_url, register_destination_form

from .form import CallfilterDestinationForm
from .service import CallfilterService
from .view import CallfilterView, CallfilterListingView

callfilter = create_blueprint('callfilter', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        CallfilterView.service = CallfilterService()
        CallfilterView.register(callfilter, route_base='/callfilters')
        register_flaskview(callfilter, CallfilterView)

        CallfilterListingView.service = CallfilterService()
        CallfilterListingView.register(callfilter, route_base='/callfilters_listing')

        register_destination_form('callfilter', 'Callfilter', CallfilterDestinationForm)

        register_listing_url('callfilter', 'callfilter.CallfilterListingView:list_json')

        core.register_blueprint(callfilter)
