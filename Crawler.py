########################################
# Crawler class:                       #
#   Crawl and parse pages from the web #
########################################
# For web request
import urllib2
# For parsing HTML
from bs4 import BeautifulSoup
# Utilities
import re

from Configuration import Conf
import sys

class Crawler:
    def __init__(self):
        self._curr_page = 0

    def loadURLConf(self, prefix, suffix):
        self.url_prefix = prefix
        self.url_suffix = suffix

    def loadPageConf(self, firstpage, lastpage, all_two_digit):
        self.firstpage = firstpage
        self.lastpage = lastpage
        self.all_two_digit = all_two_digit

    def loadEncodingConf(self, source_encoding, target_encoding):
        self.source_encoding = source_encoding
        self.target_encoding = target_encoding

    def loadFileConf(self, output_book_name):
        self.output_book_name = output_book_name

    def loadEscapeConf(self, escape_tags):
        self.escape_tags = escape_tags

    def loadContentConf(self, body_tag, body_attrs, contain_p_tags):
        self.body_tag = body_tag
        self.body_attrs = body_attrs
        self.contain_p_tags = contain_p_tags

    def loadConf(self, conf):
        if not isinstance(conf, Conf):
            print "Wrong input conf type: should be instance of Conf class."
            sys.exit(-1)

        self.loadURLConf(conf.base_url_prefix, conf.base_url_suffix)
        self.loadPageConf(conf.first_page, conf.last_page, conf.all_two_digit_number)
        self.loadEncodingConf(conf.source_encoding, conf.target_encoding)
        self.loadFileConf(conf.output_book_name)
        self.loadEscapeConf(conf.escape_tags)
        self.loadContentConf(conf.content_body_tag, conf.content_body_tag_attrs, conf.content_contain_p_tags)

        self._curr_page = self.firstpage

    def hasNext(self):
        if self._curr_page <= self.lastpage:
            return True
        else:
            return False

    def getCurrentPage(self):
        return self._curr_page

    def getNextPage(self):
        pagestr = str(self._curr_page)

        # Handle one-digit number
        if self.all_two_digit:
            if len(pagestr) == 1:
              pagestr = '0' + pagestr

        # Compose the URL
        url = self.url_prefix + pagestr + self.url_suffix

        # Send web request
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)

        # First decode the document using the specified encoding format in the HTML tag
        # (For unknown reason, GB2312 is problematic, but GBK works fine.
        content = res.read().decode(self.source_encoding)

        # Encode the document using unicode utf-8.
        # (1) for BeautifulSoup to parsing; (2) good for postprocessing
        content = content.encode(self.target_encoding)

        # Eliminate escape tag
        for t in self.escape_tags:
            t = t.encode(self.target_encoding)
            content = content.replace(t, '')

        clean_content = ''

        # Initialize BeatifulSoup class
        soup = BeautifulSoup(content)

        # Find target tags in the HTML body. Here the target tag is the table with the specific attrs.
        # After finding the table, extract all the content in <p> tags and remove all html tags from the content.
        # This part should be different for every book: depends on how the page is formatted.
        if self.contain_p_tags:
            paras = soup.find(self.body_tag, attrs=self.body_attrs).find_all('p')
            for p in paras:
              clean_content += re.sub('<[^>]*>', '', str(p))
        else:
            paras = soup.find(self.body_tag, attrs=self.body_attrs)
            clean_content += re.sub('<[^>]*>', '', str(paras))

        # Strip each page and append it with newline
        clean_content = clean_content.strip() + '\n'

        self._curr_page += 1

        return clean_content

