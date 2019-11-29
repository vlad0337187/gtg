from unittest import TestCase

from GTG.tools.urlregex import match


class TestURLRegex(TestCase):
    """ URL Regex """

    def test_allows_ampersand_in_anchor(self):
        # Reproducer for https://bugs.launchpad.net/gtg/+bug/1023555
        url = "http://test.com/#hi&there"
        matched_url = match(url).group(0)
        self.assertEqual(url, matched_url)
