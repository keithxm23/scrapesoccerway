#!/usr/bin/env python
__author__ = "Keith Mascarenhas"
__email__ = "keithxm23@gmail.com"

import requests, json, re, pdb
from bs4 import BeautifulSoup as BS

BASE_URL = 'http://us.soccerway.com/a/block_competition_matches_summary?block_id=page_competition_1_block_competition_matches_summary_6&callback_params={"page":"%d","bookmaker_urls":[],"block_service_id":"competition_summary_block_competitionmatchessummary","round_id":"%s","outgroup":"","view":"2"}&action=changePage&params={"page":%d}'
#view -> 1=going forward, 2=going reverse
BASE_SOCCERWAY_URL = "http://us.soccerway.com"
MAX_ATTEMPTS = 10
EPL_ID = 8
EPL_NAME = "Premier League"

def main():
	#First get IDs for all seasons in EPL
	EPL_URL = "http://us.soccerway.com/national/england/premier-league/c%d/" % EPL_ID
	season_soup = BS(requests.get(EPL_URL).text, 'html.parser')
	season_ids = [x for x in season_soup.select("#season_id_selector")[0].contents if x != '\n'] 
	#print season_ids
	seasons = []
#	pdb.set_trace()
	for s in season_ids[::]:
		rs = requests.get(BASE_SOCCERWAY_URL + s['value'])
		#print s['value'], rs.url
		tmp_season = {}
		tmp_season['id'] = re.findall(r'/r(\d+)', rs.url)[0]
		tmp_season['season'] = s.text
		
		print tmp_season
		matches = []
		for p in range(-37, 1):
			r = requests.get(BASE_URL % (p+1, tmp_season['id'], p))
			#print r.url
			soup = BS(json.loads(r.text)['commands'][0]['parameters']['content'], 'html.parser')
			for g in soup.find('tbody').children:
				if ' - ' not in g.contents[4].text.encode('utf-8'):
					print "Reached most recent match; break;"
					break
				tmp = {}
				tmp['season_id'] = int(tmp_season['id'])
				tmp['season'] = tmp_season['season']	
				tmp['comp_id'], tmp['comp_name'] = EPL_ID, EPL_NAME
				tmp['day'] = g.contents[0].text.encode('utf-8') 
				tmp['date'] = g.contents[1].text.encode('utf-8') 
				tmp['home_team'] = g.contents[2].text.encode('utf-8') 
				tmp['home_team_id'] = int(re.findall(r'/(\d+)/$', g.contents[2].a['href'])[0])
				tmp['away_team'] = g.contents[5].text.encode('utf-8') 
				tmp['away_team_id'] = int(re.findall(r'/(\d+)/$', g.contents[5].a['href'])[0])
				tmp['match_id'] = int(re.findall(r'/(\d+)/$', g.contents[7].a['href'])[0]) 
				tmp['home_goals'] = int(g.contents[4].text.encode('utf-8').split(' - ')[0])
				tmp['away_goals'] = int(g.contents[4].text.encode('utf-8').split(' - ')[1])
				if tmp['home_goals'] == tmp['away_goals']:
					tmp['home_points'] = tmp['away_points'] = 1
				else:
					tmp['home_points'], tmp['away_points'] = (3,0) if tmp['home_goals'] > tmp['away_goals'] else (0,3)
				matches.append(tmp)
				print tmp
		print "_________________________________________________________________"*2
		print len(matches)
		seasons.append(matches)

if __name__ == '__main__':
	main()
