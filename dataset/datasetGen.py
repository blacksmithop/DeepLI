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
    # return list of urls for that tag
    yield tag_url


def Url_To_Data(url: str):
    platform = search('https?://([A-Za-z_0-9.-]+).com*', url).group(1)
    with request.urlopen(url) as response:
        content = response.read()
    soup = BeautifulSoup(str(content), 'html.parser')
    question = soup.find("a", {"class": "question-hyperlink"}).text

    source_verified = False
    verified_question = soup.find("div", {"class": "answer accepted-answer"})
    if verified_question:
        source_verified = True  # is an accepted answer

    manual_verified = False

    answer = soup.find("div", {"class": "answercell post-layout--right"})
    code_blocks = answer.find_all('code')

    code_blocks = [code.text.replace('\\n', '') for code in code_blocks if len(code.text.split()) != 1]
    answer = '\n'.join(code_blocks)  # concatenated list of commands (code) as the answer

    if source_verified:  # getting answer from verified answers (only)
        answer_id = verified_question.get('id')
        answer_id = findall(r'\d+', answer_id)[0]
        url = f"https://{platform}/a/{answer_id}"  # answer share link

    final_answer = None  # defaults to None

    # answer schema as a dict - to be changed to csv
    post = {
        'question': question,
        'answer': answer,
        'source_verified': source_verified,
        'manual_verified': manual_verified,
        'url': url,
        'final_answer': final_answer
    }
    return post


# Parameters

platform_to_tag = {  # tags and platforms to consider
    "askubuntu": [
        "mysql", "command-line", "apt"
    ],
    "stackoverflow": [
        "aiohttp", "python", "django"
    ]
}

PAGE_MAX = 3  # number of pages to consider


def collect_urls():
    tag_urls = {}
    for platform in platform_to_tag:
        tags = platform_to_tag[platform]
        for tag in tags:
            tag_urls[tag] = []
            for i in range(1, PAGE_MAX + 1):  # PAGE_MAX number of list of urls per iteration
                for url in Tag_To_Url(base=platform, tag=tag, page=i):
                    tag_urls[tag].extend(url)
            print(f"Found {len(tag_urls[tag])} urls for tag {tag} in {platform} searching {PAGE_MAX} pages")
    return tag_urls


def data_from_url(tag_urls: dict):
    _dataset = []
    for tag in tag_urls:
        _urls = tag_urls[tag]
        for url in _urls:
            _dataset.append(Url_To_Data(url=url))
        print(f"Collected data from {len(urls)} urls with tag {tag}")
    return _dataset


if __name__ == '__main__':
    urls = collect_urls()
    dataset = data_from_url(tag_urls=urls)
