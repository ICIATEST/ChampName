import requests
from bs4 import BeautifulSoup as bs
from model.riot import *
from database import *
import boto3
from tqdm import tqdm

ssm = boto3.client(
    'ssm',
    region_name='ap-northeast-2',
    aws_access_key_id='AKIAZQEYKFPQOPOC4RH5',
    aws_secret_access_key='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'
)
parameter = ssm.get_parameter(Name='B2C_API_KEY', WithDecryption=False)
B2C_API_KEY = parameter['Parameter']['Value']

# B2C_API_KEY='RGAPI-63242056-ba20-4c7c-9203-349129698589'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}

response = requests.get('https://www.op.gg/spectate/list/pro-gamer?region=kr', headers=headers)

html = response.text

if response.status_code == 200:
    html = response.text
    soup = bs(html, 'html.parser')
    lst = soup.select('#content-container > ul > li > ul > li')
    op_gg_lst = []
    for i in tqdm(lst):
        try:
            op_gg_dic = {}
            op_gg_dic['stats'] = 'pro'
            op_gg_dic['pro_name'] = i.select('div > div > div > div > span.name')[0].get_text()
            summoner_name = i.select('div > div > div > div')[0].get_text()
            op_gg_dic['summoner_name'] = summoner_name
            riot = get_json(RiotV4Summoner(platform_id='KR', api_key=B2C_API_KEY).get_url(summoner_name=summoner_name))
            op_gg_dic['b2c_summoner_id'] = riot['id']
            op_gg_dic['b2c_account_id'] = riot['accountId']
            op_gg_dic['puuid'] = riot['puuid']
            op_gg_lst.append(op_gg_dic)
        except:
            print(summoner_name)
    # for i in op_gg_dic:
    db = connect_sql()


else:
    print(response.status_code)
