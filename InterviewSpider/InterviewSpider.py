#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys
import re


def write_to_csv(file_name, company_tag, link):
    file = open(file_name, "a")
    file.write(company_tag + " " + link + "\n")
    file.close()


def one_page_spider(url, company, interview, date):
    print("start grabbing " + url)
    # Send the request and get the response
    response = urlopen(url)
    # Parse response to be a tree format by BeautifulSoup
    bsObj = BeautifulSoup(response, "html.parser")
    # Traverse each snippet where stores the interview information
    for snippet in bsObj.findAll("tbody", id = re.compile("normalthread_.*")):
        company_tag = snippet.tr.th.span.u.findAll("b")[3].text
        interview_tag = snippet.tr.th.span.findAll("b")[4].text
        date_tag = snippet.find("td", {"class", "by"}).em.text
        # We have two lines code at the beginning to help system read chinese character
        if u"前" in date_tag or u"天" in date_tag:
            time_stamp = time.time()
        else:
            time_stamp = datetime.strptime(date_tag, "%Y-%m-%d").timestamp()
        if company_tag == company and interview in interview_tag and time_stamp > date.timestamp():
            link = snippet.tr.th.find("a", {"class", "s xst"}).attrs["href"]
            write_to_csv("InterviewSpider.csv", company_tag, link)


def interview_spider(num_of_page, url, company, interview, date):
    dt = datetime.strptime(date, "%Y-%m-%d")
    for page in range(2, int(num_of_page) + 2):
        one_page_spider(url, company, interview, dt)
        url = url[:url.index("-")] + "-145-" + str(page) + ".html"


if __name__ == "__main__":
    print("start")
    start_url = "http://www.1point3acres.com/bbs/forum-145-1.html"
    interview_spider(sys.argv[1], start_url, sys.argv[2], sys.argv[3], sys.argv[4])
