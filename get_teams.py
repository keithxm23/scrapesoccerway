#B!/usr/bin/env python
""" Scrapes all team details from soccerway and dumps to csv"""
__author__ = "Keith Mascarenhas"
__email__ = "keithxm23@gmail.com"

import requests, csv, datetime, re
from bs4 import BeautifulSoup as BS

BASE_URL = 'http://us.soccerway.com/teams/x/x/%d/'
def main():
  file_name = 'teams_%si.csv' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(file_name, 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['club_id', 'name', 'founded', 'address', 'country',
                     'phone', 'fax', 'email', 'website', 'logo', 'venue_id'])

    for x in range(0,99999):
      print x
      if requests.head(BASE_URL % x).status_code == requests.codes.ok:
        r = requests.get(BASE_URL % x)
        soup = BS(r.text, 'html.parser')
        team_data = []
        team_data.append(x) #club_id
        name_node = soup.select('#subheading > h1')
        team_data.append(name_node[0].text.encode('utf-8') if name_node else '')
        team_data.append(get_detail('Founded', soup))
        team_data.append(get_detail('Address', soup))
        team_data.append(get_detail('Country', soup))
        team_data.append(get_detail('Phone', soup))
        team_data.append(get_detail('Fax', soup))
        team_data.append(get_detail('E-mail', soup))
        website_node = soup.find('a', text='Official website')
        team_data.append(website_node['href'].encode('utf-8') if website_node else '')
        team_data.append(soup.find('div', 'logo').img['src'].encode('utf-8'))
        team_data.append(get_venue_id(x))
        print name_node[0].text
        writer.writerow(team_data)
    
def get_detail(attr, soup):
  attr_node = soup.find('dt', text=attr)
  detail = attr_node.findNextSibling('dd').text if attr_node else ''
  return detail.encode('utf-8')

def get_venue_id(team_id):
  r = requests.get(BASE_URL % team_id + 'venue/')  
  venue_id = re.findall(r'/venues/.*/v(\d+)', r.text)
  return int(venue_id[0]) if venue_id else ''




if __name__ == '__main__':
  main()
