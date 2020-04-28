#! python3

import requests
import bs4
import re
import datetime
import ezgmail
import os
# TODO: Get geekhack website html code
# TODO: Get thread titles if they were created/edited today
# TODO: Return retrieved thread titles
# TODO: Send email with thread titles (and links maybe)

res = requests.get('https://geekhack.org/index.php?board=70.0')
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

soup = bs4.BeautifulSoup(res.text, 'html.parser')

# Regular expression to find CSS selector for geekhack thread titles
postRegex = re.compile(r'''
# Example: #msg_1234567 > a
msg 				# msg
_ 					# underscore
\d{7,8}				# seven or eight digits
''', re.VERBOSE)

# Regular expression to find CSS selector for thread date
dateRegex = re.compile(r'''
# Example: 22 February 2020
\d\d			# number
\s				# space
\w{3,9}			# month
\s				# space
\d\d\d\d		# year
''', re.VERBOSE)

# Get all CSS selectors that point to the thread's title
extractedPost = postRegex.findall(res.text)

# A list that stores all of the dictionaries that hold the thread's title and date
threadList = []

# Loop through and put all thread titles and thread dates into lists
for msg in range(5, len(extractedPost)):
	title = '#' + extractedPost[msg] + ' > a'
	date = '#messageindex > table > tbody > tr:nth-child(' + str(msg+3) + ') > td.lastpost.windowbg2'
	elemsTitle = soup.select(title)
	elemsDate = soup.select(date)
	extractedDate = dateRegex.findall(elemsDate[0].text.strip())
	threadDict = {'title': elemsTitle[0].text, 'date': extractedDate}
	threadList.append(threadDict)

dt = datetime.datetime.now()
currentDate = dt.strftime("['%d %B %Y']")

for i in range(len(threadList)):
 	# print(str(threadList[i]['date']))
	if currentDate == str(threadList[i]['date']):
		print(threadList[i]['title'])

#elems = soup.select('#msg_2814304 > a')
# #messageindex > table > tbody > tr:nth-child(8) > td.lastpost.windowbg2