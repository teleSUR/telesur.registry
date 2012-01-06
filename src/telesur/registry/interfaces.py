# -*- coding: utf-8 -*-
"""Module interfaces"""

from zope import schema
from zope.interface import Interface

from telesur.registry import _

class IDisqusSettings(Interface):
    """ Disqus settings. Credentials for access to the disqus api.
        Obtainable via plone.registry.
    """
    access_token = schema.TextLine(
        title = _(u'Access Token'),
        description = _(u'Access token to retrive information from the disqus forum.'),
        required = True,
        )

    app_public_key = schema.TextLine(
        title = _(u'Application public key'),
        description = _(u'public key'),
        required = True,
        )

    app_secret_key = schema.TextLine(
        title = u'Application secret key',
        description = _(u'secret key'),
        required = True,
        )

