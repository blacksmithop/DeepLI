from urllib import request
from re import findall, search
from bs4 import BeautifulSoup


def Tag_To_Url(base: str, tag: str, page: int):
    base = f'https://{base}.com/'
    URL = '{base}questions/tagged/{tag}?tab=votes&page={i}&pagesize=15'
    with request.urlopen(URL.format(base=base, tag=tag, i=page)) as response:
        content = response.read()
    tag_url = findall(r'<h3><a href="(.*?)" class', str(content))[1:]
    tag_url = [f'{base}{link}' for link in tag_url]
    #return list of urls for that tag
    yield tag_url


def Link_To_Data(urls: list):
    url = urls[0] #test
    platform = search('https?://([A-Za-z_0-9.-]+).com*', url).group(1)
    print(f"Platform: {platform}")
    with request.urlopen(url) as response:
        content = response.read()
    soup = BeautifulSoup(str(content), 'html.parser')
    question = soup.find("a", {"class": "question-hyperlink"})
    print(f"Question: {question.text}") #title of the question

    source_verified = False
    verified_question = soup.find("div", {"class": "answer accepted-answer"})
    if verified_question:
        source_verified = True #is an accepted answer
    print(f"Source_Verified: {source_verified}")

    manual_verified = False
    print(f"Manual_Verified: {manual_verified}") #to be done later

    answer = soup.find("div", {"class": "answercell post-layout--right"})
    code_blocks = answer.find_all('code')
    print("Answer: (commands only)")
    code_blocks = [code.text.replace('\\n', '') for code in code_blocks if len(code.text.split())!=1]
    for code in code_blocks:
        print(code)
    if source_verified:
        answer_id = verified_question.get('id')
        answer_id = findall(r'\d+', answer_id)[0]
        url = f"https://{platform}/a/{answer_id}"
    print(f"Url: {url}")
        

platform_to_tag = {
    "askubuntu": [
        "mysql", "command-line", "apt"
    ],
    "stackoverflow": [
        "aiohttp", "python", "django"
    ]
}

PAGE_MAX = 3 #number of pages to consider
tag_urls = {}


def main():
    for platform in platform_to_tag:
        tags = platform_to_tag[platform]
        for tag in tags:
            tag_urls[tag] = []
            for i in range(1, PAGE_MAX+1): #PAGE_MAX number of list of urls per iteration
                for url in Tag_To_Url(base=platform, tag=tag, page=i):
                    tag_urls[tag].extend(url)
            print(f"Found {len(tag_urls[tag])} urls for tag {tag} in {platform} searching {PAGE_MAX} pages")


Link_To_Data(['https://askubuntu.com/questions/17823/how-to-list-all-installed-packages'])

