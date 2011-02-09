# This Python program accesses the PayPal X DevZone blog and document
# RSS feeds via Yahoo! Query Language calls, downloads the feed data, 
# and organizes the data before writing it out to CSV for separate analysis.
#
# Copyright (c) 2011, Bill Day; for more information see http://billday.com

# Import the modules supporting Yahoo! Query Language operations
# and reading/writing to comma separated (CSV) files.  For more
# information on the Python-YQL module, please refer to:
# http://python-yql.org/
#
import yql
import csv

# Setup public access to YQL (no authentication required).
y = yql.Public()

# Specify where DevZone CSV data files are to be written to and read from.
devzonedir = "DevZone.Generated/"


# Let's download the data from the PayPal X DevZone "Documents"
# RSS feed which includes both articles and book excerpts.  Results
# are returned as a yql.YQLObj containing rows where each row
# contains a dictionary whose value contains key:value pairs
# for one article or book excerpt RSS item.
#
# For more information see:
# http://python-yql.org/code.html
#
# NOTE:  For some reason setting 'numItems' any bigger than '38'
#        results in no documents being returned, some kind of
#        PayPal X.com server issue, maybe a config problem?
#
articlequery = "select * from rss where url in ('https://www.x.com/community/feeds/documents?community=2133&numItems=38')"
articles = y.execute(articlequery)
print "-----"
print "Harvested", articles.count, "articles and book excerpts.\n"


# Now let's download the data for all of the PayPal X DevZone "Blog" posts
# including the four principle contributors' pre-cutover blogs, too.
# As with "Documents" results above, this query's results are returned
# as a yql.YQLObj containing rows where each row contains a dictionary
# whose value contains key:value pairs for one blog post RSS item.
#
# For more information see:
# http://python-yql.org/code.html
#
# NOTE:  'numItems' is set bigger than expected number to catch all.
#
blogpostsquery = "select * from rss where url in ('https://www.x.com/people/ptwobrussell/blog/feeds/posts?numItems=20', 'https://www.x.com/people/billday/blog/feeds/posts?numItems=20', 'https://www.x.com/people/travis/blog/feeds/posts?numItems=20', 'https://www.x.com/blogs/Ethan/feeds/posts?numItems=20', 'https://www.x.com/community/feeds/blogs?community=2133&numItems=1000')"
posts = y.execute(blogpostsquery)
print "Harvested", posts.count, "blog posts.\n"


# Now that we have all the data that PayPal's RSS feeds will return,
# let's format it.  We add a field to note if each row's item is an
# 'articleOrBlog', then clip out some unwanted junk from the RSS
# pubDate field to leave just MM/DD/YYYY HH:MM, then add an item
# with key name of 'hitCount' and empty value to each row.  Then
# we output the desired data fields into a CSV summary file.
#
# Note:  Because Python dictionary contents order is randomized
#        for quick lookup, we will need to sort as desired when
#        we perform our analysis later.
#
csvfile = open(devzonedir+"devzone.harvest.csv", "wb")
csvwriter = csv.DictWriter(csvfile, fieldnames=['pubDate', 'articleOrBlog', 'title', 'link', 'hitCount', 'description'], restval='', extrasaction='ignore', dialect='excel')

for row in articles.rows:
    row["articleOrBlog"] = "article"
    date = row["pubDate"]
    date = date[5:-4]
    row["pubDate"] = date
    csvwriter.writerow(row)

for row in posts.rows:
    row["articleOrBlog"] = "blog"
    date = row["pubDate"]
    date = date[5:-4]
    row["pubDate"] = date
    csvwriter.writerow(row)

csvfile.close()
print "Article, book excerpt, and blog post data for all", articles.count + posts.count, "items saved to:\n", csvfile.name
print "-----"