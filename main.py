import requests
import json
import telebot
import time

winning_urls = ['https://api.sofascore.com/api/v1/odds/1/winning/football','https://api.sofascore.com/api/v1/odds/1/winning/ice-hockey','https://api.sofascore.com/api/v1/odds/1/winning/volleyball','https://api.sofascore.com/api/v1/odds/1/winning/tennis','https://api.sofascore.com/api/v1/odds/1/winning/basketball']
bot = telebot.TeleBot('1600740144:AAFpFngQxwH528CPMaZXPG_X-qmvvCgHjM4')
cash = set()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.sofascore.com/',
    'Origin': 'https://www.sofascore.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers',
}
while True:
    for winning_url in winning_urls:
        response = requests.get(f'{winning_url}', headers=headers).text
        try:
            error = json.loads(response)['error']
            print('тут нет игр')
        except:
            list_event = json.loads(response)['events']
            list_of_events = dict()
            for event in list_event:
                custom_id = str(event['customId'])
                slug = event['slug']
                event_id = str(event['id'])
                url = f'https://www.sofascore.com/{slug}/{custom_id}'
                event_dict = {event_id:url}
                list_of_events.update(event_dict)

            winning_odd_map = json.loads(response)['winningOddsMap']
            for odd in winning_odd_map:
                odd_2 = winning_odd_map[f'{odd}']
                expected = int(odd_2['expected'])
                actual = int(odd_2['actual'])
                if odd in cash:
                    pass
                else:
                    if actual-expected >= 40:
                        value = list_of_events[f'{odd}']
                        bot.send_message(-1001627146030,f'{value}')
                        cash.add(odd)
                    else:
                        pass
        time.sleep(30)
    time.sleep(1800)
