import unittest

from unittest.mock import patch, call
from src.treeconsolewriter import TreeConsoleWriter


class TreeConsoleWriterTests(unittest.TestCase):

    def setUp(self):
        self.mock_sys = patch('src.treeconsolewriter.sys').start()

    def test_sitemap_with_no_children_ensure_console_print_correct(self):
        sut = TreeConsoleWriter()

        sut.write([[None, "https://monzo.com/"]])

        self.mock_sys.stdout.write.assert_has_calls([
            call("|____ https://monzo.com/")
        ])

    def test_sitemap_with_single_child_ensure_console_print_correct(self):
        sut = TreeConsoleWriter()

        sut.write([
            [None, "https://monzo.com/", [1]],
            [0, "/blog", []]
        ])

        self.mock_sys.stdout.write.assert_has_calls([
            call("|____ https://monzo.com/"),
            call("|____|____ /blog"),
        ])

    def test_sitemap_with_three_children_ensure_console_print_correct(self):
        sut = TreeConsoleWriter()

        sut.write([
            [None, "https://monzo.com/", [1, 2, 3]],
            [0, "/blog", []],
            [0, "/contact", []],
            [0, "/news", []]
        ])

        self.mock_sys.stdout.write.assert_has_calls([
            call("|____ https://monzo.com/"),
            call("|____|____ /blog"),
            call("|____|____ /contact"),
            call("|____|____ /news"),
        ])

    def test_sitemap_with_multi_depth_children_ensure_console_print_correct(self):
        sut = TreeConsoleWriter()

        sut.write([
            [None, "https://monzo.com/", [1, 3, 7]],
            [0, "/blog", [2]],
            [1, "/blog/post-1", []],
            [0, "/contact", [4]],
            [3, "/contact/contact-1", [5]],
            [4, "/contact/contact-1/contact-2", [6]],
            [5, "/contact/contact-1/contact-2/contact-3", []],
            [0, "/news", [8]],
            [0, "/news/news-1", [9, 10]],
            [0, "/news/news-1/news-2", []],
            [0, "/news/news-1/news-3", []]
        ])

        self.mock_sys.stdout.write.assert_has_calls([
            call("|____ https://monzo.com/"),
            call("|____|____ /blog"),
            call("|____|____|____ /blog/post-1"),
            call("|____|____ /contact"),
            call("|____|____|____ /contact/contact-1"),
            call("|____|____|____|____ /contact/contact-1/contact-2"),
            call("|____|____|____|____|____ /contact/contact-1/contact-2/contact-3"),
            call("|____|____ /news"),
            call("|____|____|____ /news/news-1"),
            call("|____|____|____|____ /news/news-1/news-2"),
            call("|____|____|____|____ /news/news-1/news-3"),
        ])
