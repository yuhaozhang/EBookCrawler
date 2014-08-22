########################################
# Conf class:                          #
#   Load and read configuration file   #
########################################

import json
import sys

# Load json file to configure the task
class Conf:
  def __init__(self):
    pass

  def loads(self, conf_file):
    with open(conf_file, 'r') as infile:
      f = infile.read()
    conf = json.loads(f)

    # Load configuration file
    try:
      self.base_url_prefix = conf['url_conf']['base_url_prefix']
      self.base_url_suffix = conf['url_conf']['base_url_suffix']

      self.first_page = conf['page_conf']['first_page']
      self.last_page = conf['page_conf']['last_page']
      self.all_two_digit_number = conf['page_conf']['all_two_digit_number']

      self.source_encoding = conf['encoding_conf']['source_encoding']
      self.target_encoding = conf['encoding_conf']['target_encoding']
      
      self.content_body_tag = conf['content_conf']['content_body_tag']
      self.content_body_tag_attrs = conf['content_conf']['content_body_tag_attrs']
      self.content_contain_p_tags = conf['content_conf']['content_contain_p_tags']
      
      self.output_book_name = conf['file_conf']['output_book_name']
      self.escape_tags = conf['escape_conf']['escape_tags']

    except KeyError as e:
      print "Invalid configuration file, please check! Possible error key: " + e.message
      sys.exit(-1)

    # Check configuration
    if(len(self.base_url_suffix) < 1 or len(self.base_url_prefix) < 1):
      print "Wrong url configuration!"
      sys.exit(-1)

    elif(self.first_page < 0 or self.last_page < 0 or self.last_page < self.first_page):
      print "Wrong page configuration!"
      sys.exit(-1)

    elif(len(self.source_encoding) == 0):
      self.source_encoding = "utf-8"

    elif(len(self.target_encoding) == 0):
      self.target_encoding = "utf-8"

    elif(len(self.output_book_name) == 0):
      print "Wrong output book name!"
      sys.exit(-1)


