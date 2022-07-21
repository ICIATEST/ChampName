import requests


url = 'http://ddragon.leagueoflegends.com/cdn/12.13.1/data/ko_KR/champion/Aatrox.json'
url2 = 'http://ddragon.leagueoflegends.com/cdn/12.13.1/data/ko_KR/champion/Ahri.json'

res = requests.get(url).json()
res2 = requests.get(url2).json()

champ_lst = (res['data']['Aatrox']['key'], res['data']['Aatrox']['name'])
champ_lst2 = (res2['data']['Aatrox']['key'], res2['data']['Aatrox']['name'])
