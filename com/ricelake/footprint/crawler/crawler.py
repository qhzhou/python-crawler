import UrlFetcher
import UrlDbHelper
import re


MAX_DEPTH = 15

def traverse(root, pattern):
    UrlDbHelper.initDB()
    count = 0
    traverse_inner([root,], pattern, count, 0)
    UrlDbHelper.commit()
    print str(count) + " tuples have been added"

def traverse_inner(list, pattern, depth, count):
    for url in list:
        if re.match(pattern, url) and (not UrlDbHelper.inCheckedTable(url)):
            try:
                UrlDbHelper.addToCheckedTable(url)
                count += 1
                print "  "*depth + url + " depth:" + str(depth)
            except:
                print "error adding url:" + url
            if count % 100 == 0:
                UrlDbHelper.commit()
            if depth < MAX_DEPTH:
                try:
                    result = UrlFetcher.fetch_all_links(url)
                    traverse_inner(result, pattern, depth+1, count)
                except:
                    continue
            
    return

def main():
    rootUrl = "http://www.dianping.com"
    pattern = "https?://[a-zA-Z0-9]+.dianping.com"
    
#    urls = UrlFetcher.fetch_all_links(rootUrl)
#    for url in (urls):
#        print url
    traverse(rootUrl, pattern)
    
    
if __name__ == "__main__":
    main()