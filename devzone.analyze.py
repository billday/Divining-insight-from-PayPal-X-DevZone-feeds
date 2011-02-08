# This Python program reads in PayPal X DevZone blog and document feed items
# saved from a prior execution of 'devzone.harvest.py' in the CSV file
# 'devzone.harvest.csv'.
#
# It then saves out a master file containing all the article and blog post items
# minus the description (contents) as that is no longer needed after topic filtering.
#
# Copyright (c) 2011, Bill Day; for more information see http://billday.com

# Import the modules supporting reading/writing to comma separated (CSV) files
# and regular expression searching.
#
import csv
import re

# Specify where DevZone CSV data files are to be written to and read from.
devzonedir = "DevZone.Generated/"


# Read in all items from the harvest data file.
#
# Note:  Because Python dictionary contents order is randomized
#        for quick lookup, we will need to sort as desired when
#        we perform our analysis later using external tools.
#
csvinput = open(devzonedir+"devzone.harvest.csv", "rb")
itemreader = csv.DictReader(csvinput, fieldnames=['pubDate', 'articleOrBlog', 'title', 'link', 'hitCount', 'description'], dialect='excel')


# Write out all items into a master analysis CSV data file.
# Note that we've removed 'description' (contents) from the
# master output as it is not needed in that file.
#
csvallitems = open(devzonedir+"devzone.analysis.allItems.csv", "wb")
csvmaster = csv.DictWriter(csvallitems, fieldnames=['pubDate', 'articleOrBlog', 'title', 'link', 'hitCount'], restval='', extrasaction='ignore', dialect='excel')
csvmaster.writerows(itemreader)
csvallitems.close()


# Now we begin filtering based upon an input file containing a list
# of topics we search against the 'title' and 'description' values.
# 
# Note:  This input file 'devzone.topics.csv' is currently manually
#        generated; a future release may autogenerate this using
#        NLTK or a similar language processing toolkit to analyze
#        important topics emergent from the content itself.
# 
# For each topic, we write out a CSV file containing only those items
# whose 'title' or 'description' contained the topic's text string.
#
csvtopics = open("devzone.topics.csv", "rb")
topicreader = csv.reader(csvtopics, dialect='excel')

for topic in topicreader:
    currenttopic = topic[0]
    topicfile = (currenttopic.replace(' ', '')).replace('.', 'dot')
    csvcurrenttopic = open(devzonedir+"devzone.analysis.topic."+topicfile+".csv", "wb")
    csvtopic = csv.DictWriter(csvcurrenttopic, fieldnames=['pubDate', 'articleOrBlog', 'title', 'link', 'hitCount'], restval='', extrasaction='ignore', dialect='excel')
    csvinput.seek(0)
    for row in itemreader:
#        print "Topic =", currenttopic
#        print "Title =", row["title"]
#        print "Description =", row['description']
        if re.search(currenttopic,row['title']) or re.search(currenttopic,row['description']):
            csvtopic.writerow(row)
    csvcurrenttopic.close()

#for row in itemreader:
#    print row
#     save back out master file without the description


# Close the harvest input and topic list files when completely finished.
#
csvtopics.close()
csvinput.close()
