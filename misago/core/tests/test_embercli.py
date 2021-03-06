from django.conf import settings
from django.test import TestCase

from misago.core.embercli import is_ember_cli_request, get_embercli_host


class MockRequest(object):
    def __init__(self, origin):
        self.META = {'HTTP_ORIGIN': origin}


class EmberCLITests(TestCase):
    def test_is_ember_cli_request(self):
        """is_ember_cli_request test works"""
        with self.settings(DEBUG=True):
            valid_request = MockRequest(settings.MISAGO_EMBER_CLI_ORIGIN)
            self.assertTrue(is_ember_cli_request(valid_request))

            valid_origin = '%s/page.html' % settings.MISAGO_EMBER_CLI_ORIGIN
            valid_request = MockRequest(valid_origin)
            self.assertTrue(is_ember_cli_request(valid_request))

            invalid_request = MockRequest('http://somewhere.com/page.html')
            self.assertFalse(is_ember_cli_request(invalid_request))

        with self.settings(DEBUG=False):
            valid_request = MockRequest(settings.MISAGO_EMBER_CLI_ORIGIN)
            self.assertFalse(is_ember_cli_request(valid_request))

            valid_origin = '%s/page.html' % settings.MISAGO_EMBER_CLI_ORIGIN
            valid_request = MockRequest(valid_origin)
            self.assertFalse(is_ember_cli_request(valid_request))

            invalid_request = MockRequest('http://somewhere.com/page.html')
            self.assertFalse(is_ember_cli_request(invalid_request))

    def test_get_embercli_host(self):
        """get_embercli_host returns ember-cli host"""
        with self.settings(MISAGO_EMBER_CLI_ORIGIN='http://somewhere:1234'):
            self.assertEqual(get_embercli_host(), 'somewhere:1234')

        with self.settings(MISAGO_EMBER_CLI_ORIGIN=''):
            self.assertIsNone(get_embercli_host())
