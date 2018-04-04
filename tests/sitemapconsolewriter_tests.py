import unittest
import os

from unittest.mock import patch, call

from src.sitemapcli.sitemapconsolewriter import TreeConsoleWriter


class TreeConsoleWriterTests(unittest.TestCase):

    def setUp(self):
        self.mock_sys = patch('src.sitemapcli.sitemapconsolewriter.sys').start()

    def test_sitemap_with_no_children_ensure_console_print_correct(self):
        sut = TreeConsoleWriter()

        sut.write([[None, "https://monzo.com/", []]])

        self.mock_sys.stdout.write.assert_has_calls([
            call(f"|     https://monzo.com/{os.linesep}")
        ])

    def test_sitemap_with_single_child_ensure_console_print_correct(self):
        sut = TreeConsoleWriter()

        sut.write([
            [None, "https://monzo.com/", [1]],
            [0, "/blog", []]
        ])

        self.mock_sys.stdout.write.assert_has_calls([
            call(f"|     https://monzo.com/{os.linesep}"),
            call(f"|    |     /blog{os.linesep}"),
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
            call(f"|     https://monzo.com/{os.linesep}"),
            call(f"|    |     /blog{os.linesep}"),
            call(f"|    |     /contact{os.linesep}"),
            call(f"|    |     /news{os.linesep}"),
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
            call(f"|     https://monzo.com/{os.linesep}"),
            call(f"|    |     /blog{os.linesep}"),
            call(f"|    |    |     /blog/post-1{os.linesep}"),
            call(f"|    |     /contact{os.linesep}"),
            call(f"|    |    |     /contact/contact-1{os.linesep}"),
            call(f"|    |    |    |     /contact/contact-1/contact-2{os.linesep}"),
            call(f"|    |    |    |    |     /contact/contact-1/contact-2/contact-3{os.linesep}"),
            call(f"|    |     /news{os.linesep}"),
            call(f"|    |    |     /news/news-1{os.linesep}"),
            call(f"|    |    |    |     /news/news-1/news-2{os.linesep}"),
            call(f"|    |    |    |     /news/news-1/news-3{os.linesep}"),
        ])
