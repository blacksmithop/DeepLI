from urllib import request
from re import findall


def Tag_To_Url(base: str, tag: str, page: int):
    base = f'https://{base}.com/'
    URL = '{base}questions/tagged/{tag}?tab=votes&page={i}&pagesize=15'
    with request.urlopen(URL.format(base=base, tag=tag, i=page)) as response:
        content = response.read()
    tag_url = findall(r'<h3><a href="(.*?)" class', str(content))[1:]
    tag_url = [f'{base}{link}' for link in tag_url]
    #return list of urls for that tag
    yield tag_url


def Link_To_JSON(urls: list):
    url = urls[0]
    with request.urlopen(url) as response:
        content = response.read()
    title = findall(r'hyperlink">(.*?)</a>', str(content))[0]
    code = findall(r'<pre><code>(.*?)</code>', str(content))
    code = [c.replace('\\n','') for c in code]
    is_verified = findall(r'"answer accepted-answer"', str(content))
    if is_verified:
        is_verified = True
    else:
        is_verified = False
    result = {
        'title': title,
        'code': code,
        'verfied': is_verified
    }
    return result


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

for platform in platform_to_tag:
    tags = platform_to_tag[platform]
    for tag in tags:
        tag_urls[tag] = []
        for i in range(1, PAGE_MAX): #PAGE_MAX number of list of urls per iteration

            for url in Tag_To_Url(base=platform, tag=tag, page=i):
                tag_urls[tag].extend(url)
        print(f"Found {len(tag_urls[tag])} urls for tag {tag} in {platform} searching {PAGE_MAX} pages")