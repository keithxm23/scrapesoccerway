import requests, csv, datetime
from bs4 import BeautifulSoup as BS

BASE_URL = 'http://us.soccerway.com/teams/x/x/%d/'

file_name = 'teams_%si.csv' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(file_name, 'wb') as f:
  writer = csv.writer(f)
  writer.writerow(['club_id', 'name', 'founded', 'address', 'country',
                   'phone', 'fax', 'email', 'website', 'logo'])

for x in range(0,100):
  if requests.head(BASE_URL % x).status_code == requests.codes.ok:
    r = requests.get(BASE_URL % x)
    soup = BS(r.text)
    team_data = []
    team_data.append(x) #club_id
    name_node = soup.select('#subheading > h1')
    team_data.append(name_node[0].text if name_node else '')
    team_data.append(get_detail('Founded', soup))
    team_data.append(get_detail('Address', soup))
    team_data.append(get_detail('Country', soup))
    team_data.append(get_detail('Phone', soup))
    team_data.append(get_detail('Fax', soup))
    team_data.append(get_detail('E-mail', soup))
    website_node = soup.find('a', text='Official website')
    team_data.append(website_node['href'] if website_node else '')
    team_data.append(soup.find('div', 'logo').img['src'])
    print team_data
    writer.writerow(team_data)
    
def get_detail(attr, soup):
  attr_node = soup.find('dt', text=attr)
  detail = attr_node.findNextSibling('dd').text if attr_node else ''
  return detail



