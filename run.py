import requests
from bs4 import BeautifulSoup
import os

GIST_ID = os.getenv('GIST_ID')
GH_TOKEN = os.getenv('GH_TOKEN')
BGM_USER = os.getenv('BGM_USER')
COOKIE = os.getenv('COOKIE')

HEADERS = {
    'User-Agent': 'Coin-233/bgm-box (https://github.com/Coin-233/bgm-box)',
    'Cookie': f"chii_auth={COOKIE}"
}

def fetch_bgm_info(username):
    api_url = f'https://api.bgm.tv/v0/users/{username}'
    api_response = requests.get(api_url, headers=HEADERS)
    user_data = api_response.json()
    nickname = user_data.get('nickname', username)

    user_url = f'https://bgm.tv/user/{username}'
    response = requests.get(user_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    info = {
        'fav': soup.find('div', class_='item').find('span', class_='num').text,
        'pc': soup.find('div', class_='item green').find('span', class_='num').text,
        'pcr': soup.find('div', class_='item blue').find('span', class_='num').text,
        'gp': soup.find('div', class_='item orange').find('span', class_='num').text,
        'sd': soup.find('div', class_='item purple').find('span', class_='num').text,
        'rat': soup.find('div', class_='item sky').find('span', class_='num').text
    }

    return info, nickname

def update_gist(info, nickname):
    gist_url = f'https://api.github.com/gists/{GIST_ID}'
    headers = {
        'Authorization': f'token {GH_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    content = f"""
{info['fav']} 收藏           {info['pc']} 完成
{info['pcr']} 完成率       {info['gp']} 平均分
{info['sd']} 标准差        {info['rat']} 评分数

https://bgm.tv/user/{BGM_USER}
"""
    data = {
        "files": {
            f"📺{nickname}'s bangumi stats": {
                "content": content.strip()
            }
        }
    }
    response = requests.patch(gist_url, json=data, headers=headers)

if __name__ == '__main__':
    user_info, nickname = fetch_bgm_info(BGM_USER)
    update_gist(user_info, nickname)
