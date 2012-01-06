# -*- coding: utf-8 -*-
"""Module interfaces"""

from zope import schema
from zope.interface import Interface

class IDisqusSettings(Interface):
    """ Disqus settings. Credentials for access to the disqus api.
        Obtainable via plone.registry.
    """
    access_token = schema.TextLine(
        title = u'Access Token',
        description = u'Access token to retrive information from the disqus forum.',
        required = True,
        )

    app_public_key = schema.TextLine(
        title = u'Application public key',
        description = u'',
        required = True,
        )

    app_secret_key = schema.TextLine(
        title = u'Application secret key',
        description = u'',
        required = True,
        )

