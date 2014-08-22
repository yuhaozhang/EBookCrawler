##################################################
# Main code for crawling "Xu Yun He Shang Zhuan" #
##################################################

# Utilities
import time
from Crawler import Crawler
from Configuration import Conf

def main():
  conf = Conf()
  conf.loads('example_conf.json')

  crawler = Crawler()
  crawler.loadConf(conf)

  outfilename = conf.output_book_name

  while crawler.hasNext():
    content = crawler.getNextPage()

    # Append to file
    with open(outfilename, 'a+') as outfile:
      outfile.write(content)

    # Console information
    print 'Page ' + str(crawler.getCurrentPage()) + ' finished!'

    # Sleep to prevent the server from blacklisting my IP
    time.sleep(1)

if __name__ == "__main__":
  main()
