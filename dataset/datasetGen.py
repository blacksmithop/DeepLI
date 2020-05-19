import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

questions = []

# each page take 50 questions, range is the page count
for i in range(100):
    response = requests.get('https://askubuntu.com/questions/tagged/command-line?tab=newest&page='+str(i)+'&pagesize=15')
    response.status_code
    soup = bs(response.content, 'html.parser')
    body = soup.find('body')
    q_tags = body.find_all('div', class_='question-summary') # each  QUESTION
    print(len(q_tags))
    for quest in q_tags:
        text = quest.find_all('div', class_='excerpt') # quesstion text
        if "How" in text[0].text:
            print(text[0].text)
            # questions = questions.append(text[0].text)
