# -*- coding: utf-8 -*-
"""Configlets for the plone control panel"""

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from telesur.registry.interfaces import IDisqusSettings
from plone.z3cform import layout

class DisqusControlPanelForm(RegistryEditForm):
    """ Disqus setting configlet for the control panel.
    """
    schema = IDisqusSettings

DisqusControlPanelView = layout.wrap_form(
    DisqusControlPanelForm, ControlPanelFormWrapper)
DisqusControlPanelView.label = u"Disqus settings"
