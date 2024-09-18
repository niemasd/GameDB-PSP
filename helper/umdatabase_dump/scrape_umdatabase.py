#! /usr/bin/env python3
'''
Scrape data from UMDatabase
'''
from bs4 import BeautifulSoup
from os import makedirs
from os.path import abspath, expanduser, isfile
from sys import argv

# regions
REGION = {
    'eu': 'PAL',
    'jp': 'NTSC-J',
    'kr': 'NTSC-J',
    'us': 'NTSC-U',
}

# main program
if __name__ == "__main__":
    assert len(argv) == 2, "USAGE: %s <umdatabase.net HTML>" % argv[0]
    games_path = '%s/games' % '/'.join(abspath(expanduser(argv[0])).split('/')[:-3])
    raw_data = open(argv[1]).read().strip()
    soup = BeautifulSoup(raw_data, 'html.parser')
    for row_num, row in enumerate(soup.find_all('table', {'id':'UMDTable'})[0].find_all('tr')):
        if row_num == 0:
            continue # skip header row
        game_data = {
            'serial': row.find_all('td', {'id':'DISCID'})[0].text.strip(),
            'title': '\n'.join([v.text.strip() for v in row.find_all('td', {'id':'TITLE'})[0] if v.text.strip() != ''][::-1]),
            'release_date': row.find_all('td', {'id':'DATE'})[0].text.strip(),
            'region': '',
            'version': row.find_all('td', {'id':'VERSION'})[0].text.strip(),
            'publisher': row.find_all('td', {'id':'PUBLISHER'})[0].text.strip(),
        }
        try:
            game_data['region'] = REGION[row.find_all('td', {'id':'FLAG'})[0].find_all('img')[0]['src'].split('/')[-1].split('.')[0].strip()]
        except IndexError:
            pass
        game_path = '%s/%s' % (games_path, game_data['serial'])
        makedirs(game_path, exist_ok=True)
        for k in ['title', 'release_date', 'region', 'version', 'publisher']:
            k_path = '%s/%s.txt' % (game_path, k)
            if game_data[k].strip() != '' and not isfile(k_path):
                f = open('%s/%s.txt' % (game_path, k), 'w'); f.write(game_data[k].strip()); f.write('\n'); f.close()
