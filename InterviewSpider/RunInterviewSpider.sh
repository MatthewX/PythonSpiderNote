#!/bin/sh
echo "type the number of pages you want to scrape"
read pages
echo "type the company you want to search, the first character should be uppercase"
read company
echo "type the interview type you want to search"
echo "you should pick from 在线笔试 or 技术电面 or Onsite"
read interview
echo "type the date which the interviews are taken after, the format should be y-m-d"
read date

python3 InterviewSpider.py $pages $company $interview $date
