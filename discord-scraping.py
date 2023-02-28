import pandas as pd
import requests
import json
import re

def scrape_messages(channel_id):
    headers = {'authorization': 'NjQ0NTE2NDYyNzY1Mjc3MTg5.G-_0SO.hAM_YxG5wscBO6HZCB2KSOCAHXVNeSsvaVOfdw'}
    
    # Get all messages in the channel based on the request URL
    request_url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    r = requests.get(request_url, headers = headers)
    all_messages_info = json.loads(r.text)
    
    # Get all messages without link and sort from the earliest
    all_messages = [value['content'] for value in all_messages_info if value['content'].find('http') == -1][::-1]
    all_cleaned_messages = []
    for msg in all_messages:
        emoji_pattern = re.compile('['
            u'\U0001F600-\U0001F64F'  # emoticons
            u'\U0001F300-\U0001F5FF'  # symbols & pictographs
            u'\U0001F680-\U0001F6FF'  # transport & map symbols
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
            ']+', flags = re.UNICODE)
        all_cleaned_messages.append(emoji_pattern.sub(r'', msg))
    df = pd.DataFrame({'kalimat': all_cleaned_messages})
    df.to_csv('discord-chat.csv', index = False)

def main():
    channel_link = 'https://discord.com/channels/932467866236751902/944230785936920586'
    reversed_channel_link = channel_link[::-1]
    channel_id = reversed_channel_link[:reversed_channel_link.find('/')][::-1]
    scrape_messages(channel_id)

if __name__ == '__main__':
    main()