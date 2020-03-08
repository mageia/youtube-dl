#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import re
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtube_dl.utils import YoutubeDLCookieJar


class TestYoutubeDLCookieJar(unittest.TestCase):
    def __assert_cookie_has_value(self, cookiejar, key):
        self.assertEqual(cookiejar._cookies['www.foobar.foobar']['/'][key].value, key + '_VALUE')

    def test_keep_session_cookies(self):
        cookiejar = YoutubeDLCookieJar('./test/testdata/cookies/session_cookies.txt')
        cookiejar.load(ignore_discard=True, ignore_expires=True)
        tf = tempfile.NamedTemporaryFile(delete=False)
        try:
            cookiejar.save(filename=tf.name, ignore_discard=True, ignore_expires=True)
            temp = tf.read().decode('utf-8')
            self.assertTrue(re.search(
                r'www\.foobar\.foobar\s+FALSE\s+/\s+TRUE\s+0\s+YoutubeDLExpiresEmpty\s+YoutubeDLExpiresEmptyValue', temp))
            self.assertTrue(re.search(
                r'www\.foobar\.foobar\s+FALSE\s+/\s+TRUE\s+0\s+YoutubeDLExpires0\s+YoutubeDLExpires0Value', temp))
        finally:
            tf.close()
            os.remove(tf.name)

    def test_strip_httponly_prefix(self):
        cookiejar = YoutubeDLCookieJar('./test/testdata/cookies/httponly_cookies.txt')
        cookiejar.load(ignore_discard=True, ignore_expires=True)
        self.__assert_cookie_has_value(cookiejar, 'HTTPONLY_COOKIE')
        self.__assert_cookie_has_value(cookiejar, 'JS_ACCESSIBLE_COOKIE')

    def test_convert_spaces_to_tabs(self):
        cookiejar = YoutubeDLCookieJar('./test/testdata/cookies/cookie_file_with_spaces.txt')
        cookiejar.load(ignore_discard=True, ignore_expires=True)
        self.__assert_cookie_has_value(cookiejar, 'COOKIE')


if __name__ == '__main__':
    unittest.main()
