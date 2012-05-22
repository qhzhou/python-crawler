import urllib2
import sys
from cgi import escape
import urlparse
from BeautifulSoup import BeautifulSoup

__version__ = "1.0"

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__

AGENT = "%s/%s" % (__name__, __version__)

class Fetcher(object):

    def __init__(self, url):
        self.url = url
        self.urls = []

    def __getitem__(self, x):
        return self.urls[x]

    def _addHeaders(self, request):
        request.add_header("User-Agent", AGENT)

    def openUrl(self):
        url = self.url
        try:
            request = urllib2.Request(url)
            handle = urllib2.build_opener()
        except IOError:
            return None
        return (request, handle)

    def fetch(self):
        request, handle = self.openUrl()
        self._addHeaders(request)
        if handle:
            try:
                content = unicode(handle.open(request).read(), "utf-8",
                        errors="replace")
                soup = BeautifulSoup(content)
                tags = soup('a')
            except urllib2.HTTPError, error:
                if error.code == 404:
                    print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
                else:
                    print >> sys.stderr, "ERROR: %s" % error
                tags = []
            except urllib2.URLError, error:
                print >> sys.stderr, "ERROR: %s" % error
                tags = []
            for tag in tags:
                href = tag.get("href")
                if href is not None:
                    url = urlparse.urljoin(self.url, escape(href))
                    if url not in self:
                        self.urls.append(url)
                        
def fetch_all_links(url):
    fetcher = Fetcher(url)
    fetcher.fetch()
    urls = fetcher.urls
    del fetcher
    return urls
                        
                        
def main():
    url1 = fetch_all_links("http://translate.google.com.hk/?hl=zh-TW&amp;tab=wT")
    url2 = fetch_all_links("http://www.dianping.com")
    for url in (url1 + url2):
        print url
    
    
if __name__ == "__main__":
    main()
