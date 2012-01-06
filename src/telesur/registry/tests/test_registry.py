# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry import Registry
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from telesur.registry import config
from telesur.registry.interfaces import IDisqusSettings
from telesur.registry.testing import INTEGRATION_TESTING


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Set up the settings registry
        self.registry = Registry()
        self.registry.registerInterface(IDisqusSettings)

    def test_controlpanel_view(self):
        # control panel view exists
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name=config.CONTROLPANEL_ID)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        # control panel view can not be accessed by anonymous users
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@telesur-disqus-controlpanel')

    def test_entry_in_controlpanel(self):
        # there must be an entry in the control panel
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.assertTrue('telesur.registry.disqusettings' in [a.getAction(self)['id']
                        for a in self.controlpanel.listActions()])

    def test_record_access_token(self):
        # access_token record must be in the registry
        record_access_token = self.registry.records[
            'telesur.registry.interfaces.IDisqusSettings.access_token']
        self.assertTrue('access_token' in IDisqusSettings)
        self.assertEquals(record_access_token.value, None)

    def test_record_app_public_key(self):
        # app_public_key record must be in the registry
        record_app_public_key = self.registry.records[
            'telesur.registry.interfaces.IDisqusSettings.app_public_key']
        self.assertTrue('app_public_key' in IDisqusSettings)
        self.assertEquals(record_app_public_key.value, None)

    def test_record_app_secret_key(self):
        # app_secret_key record must be in the registry
        record_app_secret_key = self.registry.records[
            'telesur.registry.interfaces.IDisqusSettings.app_secret_key']
        self.assertTrue('app_secret_key' in IDisqusSettings)
        self.assertEquals(record_app_secret_key.value, None)


from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login


class RegistryUninstallTest(unittest.TestCase):
    """ensure registry is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.registry = getUtility(IRegistry)
        # uninstall the package
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[config.PROJECTNAME])

    def test_records_uninstalled(self):
        # Test that the records were removed from the control panel
        records = [
            'telesur.registry.interfaces.IDisqusSettings.access_token',
            'telesur.registry.interfaces.IDisqusSettings.app_public_key',
            'telesur.registry.interfaces.IDisqusSettings.app_secret_key',
            ]
        for r in records:
            self.assertFalse(r in self.registry)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
