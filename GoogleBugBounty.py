from bs4 import BeautifulSoup
import wikipedia
import re
import datetime
import smtplib
import arrow
import sys


def sendusinggmail():
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(GMAILUSER, GMAILPASS)
    headers = "\r\n".join(["from: " + GMAILUSER,
                           "subject: " + "Bug Bounty Alert",
                           "to: " + SENDTOEMAIL,
                           "mime-version: 1.0",
                           "content-type: text/html"])
    linksend = '<html><body>'

    for a in companynames[-5:]:
        linksend += '<br>'
        linksend += "<h1>"
        linksend += unicode(str(a)).rstrip() ##Get just the company name no new lines
        linksend += "</h1> Will be eligible for submitting Google Bounty bugs in 7 days; go get them sport..."
        linksend += '<br>'
    content = headers + "\r\n\r\n" + linksend
    session.sendmail(GMAILUSER, SENDTOEMAIL, content)


def sevendaycheck():
    #grab the wikipedia page and search for the table that holds the company name and dates
    acq = wikipedia.page('List_of_mergers_and_acquisitions_by_Google')
    test = acq.html()
    soup = BeautifulSoup(test)
    table = soup.find('table', {'class': 'wikitable sortable'})
    for row in table.findAll('tr'):
        cells = row.findAll('td')
        #Extract the company name and date from the table
        if len(cells) == 8:
            date1 = cells[1].get_text()
            company = cells[2].get_text()
            date1 = re.findall('0000(.*)', date1)
            str1 = ''.join(date1)
            try:
                #Take the date and adds 6 months then subtracts 7 days and compares it to today's date.
                #If it matches add to the list to include in the email.
                dt = datetime.datetime.strptime(str1, "%B %d, %Y")
                dt = dt.date()
                dt = arrow.get(dt)
                dt = dt.replace(months=+6)
                dt = dt.replace(days=-7)
                dt = dt.date()
                today = arrow.utcnow()
                today = today.date()
                checkdate = dt == today
                if checkdate:
                    companynames.append(company.encode('utf-8'))
                else:
                    pass
            except:
                pass

# Vars
GMAILUSER = ''
GMAILPASS = ''
SENDTOEMAIL = ''
companynames = []
company = ""
date1 = ""



sevendaycheck()

#Check to see if a company has been put in the list if so it will create and send the email if not it will exit.
if len(companynames) == 0:
    sys.exit()

else:
    sendusinggmail()