from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import time
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
        if u"前" in date_tag or u"天" in date_tag:
            time_stamp = time.time()
        else:
            time_stamp = datetime.strptime(date_tag, "%Y-%m-%d").timestamp()
        if company_tag == company and interview in interview_tag and time_stamp > date.timestamp():
            link = snippet.tr.th.find("a", {"class", "s xst"}).attrs["href"]
            write_to_csv("InterviewSpider.csv", company_tag, link)


def interview_spider(num_of_page, url, company, interview, date):
    for page in range(2, num_of_page):
        one_page_spider(url, company, interview, date)
        url = url[:url.index("-")] + "-145-" + str(page) + ".html"

# response = urlopen("http://www.1point3acres.com/bbs/forum-145-1.html")
# bsObj = BeautifulSoup(response, "html.parser")
# print(bsObj.find("div", {"class", "pg"}).a)


interview_spider(10, "http://www.1point3acres.com/bbs/forum-145-1.html", "Amazon", "Onsite", datetime.strptime("2016-9-1", "%Y-%m-%d"))
