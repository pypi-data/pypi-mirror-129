# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
App Handler
"""

from __future__ import unicode_literals, absolute_import

import os
# import re
import tempfile

from rattail.util import load_object, pretty_quantity, progress_loop
from rattail.files import temp_path
from rattail.mail import send_email


class AppHandler(object):
    """
    Base class and default implementation for top-level Rattail app handler.

    aka. "the handler to handle all handlers"

    aka. "one handler to bind them all"
    """
    default_autocompleters = {
        'brands': 'rattail.autocomplete.brands:BrandAutocompleter',
        'customers': 'rattail.autocomplete.customers:CustomerAutocompleter',
        'customers.neworder': 'rattail.autocomplete.customers:CustomerNewOrderAutocompleter',
        'customers.phone': 'rattail.autocomplete.customers:CustomerPhoneAutocompleter',
        'employees': 'rattail.autocomplete.employees:EmployeeAutocompleter',
        'departments': 'rattail.autocomplete.departments:DepartmentAutocompleter',
        'people': 'rattail.autocomplete.people:PersonAutocompleter',
        'people.employees': 'rattail.autocomplete.people:PersonEmployeeAutocompleter',
        'people.neworder': 'rattail.autocomplete.people:PersonNewOrderAutocompleter',
        'products': 'rattail.autocomplete.products:ProductAutocompleter',
        'products.all': 'rattail.autocomplete.products:ProductAllAutocompleter',
        'products.neworder': 'rattail.autocomplete.products:ProductNewOrderAutocompleter',
        'vendors': 'rattail.autocomplete.vendors:VendorAutocompleter',
    }

    def __init__(self, config):
        self.config = config

    def get_autocompleter(self, key, **kwargs):
        """
        Returns a new :class:`~rattail.autocomplete.base.Autocompleter`
        instance corresponding to the given key, e.g. ``'products'``.

        The app handler has some hard-coded defaults for the built-in
        autocompleters (see ``default_autocompleters`` in the source
        code).  You can override any of these, and/or add your own
        with custom keys, via config, e.g.:

        .. code-block:: ini

           [rattail]
           autocomplete.products = poser.autocomplete.products:ProductAutocompleter
           autocomplete.otherthings = poser.autocomplete.things:OtherThingAutocompleter

        With the above you can then fetch your custom autocompleter with::

           autocompleter = app.get_autocompleter('otherthings')

        In any case if it can locate the class, it will create an
        instance of it and return that.

        :params key: Unique key for the type of autocompleter you
           need.  Often is a simple string, e.g. ``'customers'`` but
           sometimes there may be a "modifier" with it to get an
           autocompleter with more specific behavior.

           For instance ``'customers.phone'`` would effectively give
           you a customer autocompleter but which searched by phone
           number instead of customer name.

           Note that each key is still a simple string though, and that
           must be "unique" in the sense that only one autocompleter
           can be configured for each key.

        :returns: An :class:`~rattail.autocomplete.base.Autocompleter`
           instance if found, otherwise ``None``.
        """
        spec = self.config.get('rattail', 'autocomplete.{}'.format(key))
        if not spec:
            spec = self.default_autocompleters.get(key)
        if spec:
            return load_object(spec)(self.config)

        raise NotImplementedError("cannot locate autocompleter for key: {}".format(key))

    def get_auth_handler(self, **kwargs):
        if not hasattr(self, 'auth_handler'):
            spec = self.config.get('rattail', 'auth.handler',
                                   default='rattail.auth:AuthHandler')
            factory = load_object(spec)
            self.auth_handler = factory(self.config, **kwargs)
        return self.auth_handler

    def get_batch_handler(self, key, **kwargs):
        from rattail.batch import get_batch_handler
        return get_batch_handler(self.config, key, **kwargs)

    def get_board_handler(self, **kwargs):
        if not hasattr(self, 'board_handler'):
            from rattail.board import get_board_handler
            self.board_handler = get_board_handler(self.config, **kwargs)
        return self.board_handler

    def get_clientele_handler(self, **kwargs):
        if not hasattr(self, 'clientele_handler'):
            from rattail.clientele import get_clientele_handler
            self.clientele_handler = get_clientele_handler(self.config, **kwargs)
        return self.clientele_handler

    def get_employment_handler(self, **kwargs):
        if not hasattr(self, 'employment_handler'):
            from rattail.employment import get_employment_handler
            self.employment_handler = get_employment_handler(self.config, **kwargs)
        return self.employment_handler

    def get_feature_handler(self, **kwargs):
        if not hasattr(self, 'feature_handler'):
            from rattail.features import FeatureHandler
            self.feature_handler = FeatureHandler(self.config, **kwargs)
        return self.feature_handler

    def get_email_handler(self, **kwargs):
        if not hasattr(self, 'email_handler'):
            from rattail.mail import get_email_handler
            self.email_handler = get_email_handler(self.config, **kwargs)
        return self.email_handler

    # TODO: is it helpful to expose this? or more confusing?
    get_mail_handler = get_email_handler

    def get_membership_handler(self, **kwargs):
        """
        Returns a reference to the configured Membership Handler.

        See also :doc:`rattail-manual:base/handlers/other/membership`.
        """
        if not hasattr(self, 'membership_handler'):
            spec = self.config.get('rattail', 'membership.handler',
                                   default='rattail.membership:MembershipHandler')
            factory = load_object(spec)
            self.membership_handler = factory(self.config, **kwargs)
        return self.membership_handler

    def get_people_handler(self, **kwargs):
        """
        Returns a reference to the configured People Handler.

        See also :doc:`rattail-manual:base/handlers/other/people`.
        """
        if not hasattr(self, 'people_handler'):
            spec = self.config.get('rattail', 'people.handler',
                                   default='rattail.people:PeopleHandler')
            factory = load_object(spec)
            self.people_handler = factory(self.config, **kwargs)
        return self.people_handler

    def get_products_handler(self, **kwargs):
        if not hasattr(self, 'products_handler'):
            from rattail.products import get_products_handler
            self.products_handler = get_products_handler(self.config, **kwargs)
        return self.products_handler

    def get_report_handler(self, **kwargs):
        if not hasattr(self, 'report_handler'):
            from rattail.reporting import get_report_handler
            self.report_handler = get_report_handler(self.config, **kwargs)
        return self.report_handler

    def progress_loop(self, *args, **kwargs):
        return progress_loop(*args, **kwargs)

    def get_session(self, obj):
        """
        Returns the SQLAlchemy session with which the given object is
        associated.  Simple convenience wrapper around
        ``sqlalchemy.orm.object_session()``.
        """
        from sqlalchemy import orm

        return orm.object_session(obj)

    def make_session(self, **kwargs):
        """
        Creates and returns a new SQLAlchemy session for the Rattail DB.
        """
        from rattail.db import Session
        return Session(**kwargs)

    def cache_model(self, session, model, **kwargs):
        """
        Convenience method which invokes
        :func:`rattail.db.cache.cache_model()` with the given model
        and keyword arguments.
        """
        from rattail.db import cache
        return cache.cache_model(session, model, **kwargs)

    def make_temp_dir(self, **kwargs):
        """
        Create a temporary directory.  This is mostly a convenience wrapper
        around the built-in ``tempfile.mkdtemp()``.
        """
        if 'dir' not in kwargs:
            workdir = self.config.workdir(require=False)
            if workdir:
                tmpdir = os.path.join(workdir, 'tmp')
                if not os.path.exists(tmpdir):
                    os.makedirs(tmpdir)
                kwargs['dir'] = tmpdir
        return tempfile.mkdtemp(**kwargs)

    def make_temp_file(self, **kwargs):
        """
        Reserve a temporary filename.  This is mostly a convenience wrapper
        around the built-in ``tempfile.mkstemp()``.
        """
        if 'dir' not in kwargs:
            workdir = self.config.workdir(require=False)
            if workdir:
                tmpdir = os.path.join(workdir, 'tmp')
                if not os.path.exists(tmpdir):
                    os.makedirs(tmpdir)
                kwargs['dir'] = tmpdir
        return temp_path(**kwargs)

    def normalize_phone_number(self, number):
        """
        Normalize the given phone number, to a "common" format that
        can be more easily worked with for sync logic etc.
        """
        from rattail.db.util import normalize_phone_number

        return normalize_phone_number(number)

    def phone_number_is_invalid(self, number):
        """
        This method should validate the given phone number string, and if the
        number is *not* considered valid, this method should return the reason
        as string.  If the number is valid, returns ``None``.
        """
        # strip non-numeric chars, and make sure we have 10 left
        normal = self.normalize_phone_number(number)
        if len(normal) != 10:
            return "Phone number must have 10 digits"

    def format_phone_number(self, number):
        """
        Returns a "properly formatted" string based on the given phone number.
        """
        from rattail.db.util import format_phone_number

        return format_phone_number(number)

    def render_currency(self, value, scale=2, **kwargs):
        """
        Must return a human-friendly display string for the given currency
        value, e.g. ``Decimal('4.20')`` becomes ``"$4.20"``.
        """
        if value is not None:
            if value < 0:
                fmt = "(${{:0,.{}f}})".format(scale)
                return fmt.format(0 - value)
            fmt = "${{:0,.{}f}}".format(scale)
            return fmt.format(value)

    def render_quantity(self, value, **kwargs):
        """
        Return a human-friendly display string for the given quantity
        value, e.g. ``1.000`` becomes ``"1"``.
        """
        return pretty_quantity(value, **kwargs)

    def render_date(self, value, **kwargs):
        """
        Must return a human-friendly display string for the given ``date``
        object.
        """
        if value is not None:
            return value.strftime('%Y-%m-%d')

    def render_datetime(self, value, **kwargs):
        """
        Must return a human-friendly display string for the given ``datetime``
        object.
        """
        if value is not None:
            return value.strftime('%Y-%m-%d %I:%M:%S %p')

    def send_email(self, key, data={}, **kwargs):
        """
        Send an email message of the given type.

        See :func:`rattail.mail.send_email()` for more info.
        """
        send_email(self.config, key, data, **kwargs)


class GenericHandler(object):
    """
    Base class for misc. "generic" feature handlers.

    Most handlers which exist for sake of business logic, should inherit from
    this.
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.enum = self.config.get_enum()
        self.model = self.config.get_model()
        self.app = self.config.get_app()

    def progress_loop(self, *args, **kwargs):
        return self.app.progress_loop(*args, **kwargs)

    def get_session(self, obj):
        """
        Convenience wrapper around :meth:`AppHandler.get_session()`.
        """
        return self.app.get_session(obj)

    def make_session(self):
        """
        Convenience wrapper around :meth:`AppHandler.make_session()`.
        """
        return self.app.make_session()

    def cache_model(self, session, model, **kwargs):
        """
        Convenience method which invokes :func:`rattail.db.cache.cache_model()`
        with the given model and keyword arguments.
        """
        return self.app.cache_model(session, model, **kwargs)


def make_app(config, **kwargs):
    """
    Create and return the configured :class:`AppHandler` instance.
    """
    spec = config.get('rattail', 'app.handler')
    if spec:
        factory = load_object(spec)
    else:
        factory = AppHandler
    return factory(config, **kwargs)
