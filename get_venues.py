#!/usr/bin/env python
""" Scrapes all venue details from soccerway and dumps to csv"""
__author__ = "Keith Mascarenhas"
__email__ = "keithxm23@gmail.com"

import requests, csv, datetime, re
from bs4 import BeautifulSoup as BS

BASE_URL = "http://us.soccerway.com/venues/x/x/v%d/"
def main():
  venues_file_name = 'venues%s.csv' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  venue_team_file_name = 'venue_team%s.csv' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(file_name, 'wb') as f, open(venue_team_file_name) as f2:
    writer = csv.writer(f)
    writer.writerow(['venue_id', 'name', 'country', 'address', 'zipcode',
                     'city', 'fax', 'email', 'website', 'phone', 'openend',
                     'architect', 'capacity', 'surface', 'facts'])

    writer2 = csv.writer(f2)
    writer2.writerow(['venue_id','team_id'])
    

    for x in range(0,20000):
      print x
      if requests.head(BASE_URL % x).status_code == requests.codes.ok:
        r = requests.get(BASE_URL % x)
        soup = BS(r.text, 'html.parser')
        venue_data = []
        venue_data.append(x) #venue_id
        name_node = soup.select('#subheading > h1')
        venue_data.append(name_node[0].text.encode('utf-8') if name_node else '')
        venue_data.append(get_detail('Founded', soup))
        venue_data.append(get_detail('Address', soup))
        venue_data.append(get_detail('Country', soup))
        venue_data.append(get_detail('Phone', soup))
        venue_data.append(get_detail('Fax', soup))
        venue_data.append(get_detail('E-mail', soup))
        website_node = soup.find('a', text='Official website')
        venue_data.append(website_node['href'].encode('utf-8') if website_node else '')
        venue_data.append(soup.find('div', 'logo').img['src'].encode('utf-8'))
        venue_data.append(get_venue_id(x))
        print name_node[0].text
        writer.writerow(venue_data)
    
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
