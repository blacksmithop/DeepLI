from urllib import request
from re import findall, search
from bs4 import BeautifulSoup
from csv import DictWriter


class DataSetGen:
    def __init__(self):
        self.PAGE_MAX = 3
        self.platform_to_tag = {  # tags and platforms to consider
            "askubuntu": [
                "mysql", "command-line", "apt"
            ],
            "stackoverflow": [
                "aiohttp", "python", "django"
            ]
        }
        self.URL = '{base}questions/tagged/{tag}?tab=votes&page={i}&pagesize=15'
        self.tag_urls = {}
        self.soup = None
        self.platform = None
        self.data_set = []

    def tag_to_url(self, base: str, tag: str, page: int):
        base = f'https://{base}.com/'
        with request.urlopen(self.URL.format(base=base, tag=tag, i=page)) as response:
            content = response.read()
        tag_url = findall(r'<h3><a href="(.*?)" class', str(content))[1:]
        tag_url = [f'{base}{link}' for link in tag_url]
        # return list of urls for that tag
        yield tag_url

    def collect_urls(self):
        for platform in self.platform_to_tag:
            tags = self.platform_to_tag[platform]
            for tag in tags:
                self.tag_urls[tag] = []
                for i in range(1, self.PAGE_MAX + 1):  # PAGE_MAX number of list of urls per iteration
                    for url in self.tag_to_url(base=platform, tag=tag, page=i):
                        self.tag_urls[tag].extend(url)
                print(
                    f"Found {len(self.tag_urls[tag])} urls for tag {tag} in {platform} searching {self.PAGE_MAX} pages")
        return self.tag_urls

    def url_to_data(self, url: str):
        self.platform = search(r'https?://([A-Za-z_0-9.-]+).com*', url).group(1)
        with request.urlopen(url) as response:
            content = response.read()

        self.soup = BeautifulSoup(str(content), 'html.parser')

        question = self.get_question()
        source_verified, url = self.is_verified()
        manual_verified = False
        if not source_verified:  # skip over ones without accepted answers
            return None
        answer = self.get_answer()
        final_answer = False

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

    def get_question(self):
        question = self.soup.find("a", {"class": "question-hyperlink"}).text
        return question

    def is_verified(self):
        verified = self.soup.find("div", {"class": "answer accepted-answer"})
        url = None
        try:
            answer_id = verified.get('id')
            answer_id = findall(r'\d+', answer_id)[0]
            url = f"https://{self.platform}.com/a/{answer_id}"  # answer share link
            verified = True

        except Exception:
            verified = False

        return verified, url

    def get_answer(self):
        answer = self.soup.find("div", {"class": "answercell post-layout--right"})
        code_blocks = answer.find_all('code')
        code_blocks = [code.text.replace('\\n', '') for code in code_blocks if len(code.text.split()) != 1]
        answer = '\n'.join(code_blocks)  # concatenated list of commands (code) as the answer
        return answer

    def data_from_url(self):
        _dataset = []
        for tag in self.tag_urls:
            _urls = self.tag_urls[tag]
            for url in _urls:
                data = self.url_to_data(url=url)
                if data is None:
                    continue
                _dataset.append(data)
            print(f"Collected data from {len(_urls)} urls with tag {tag}")
        self.data_set = _dataset

    def write_to_csv(self):
        with open('dataset.csv', 'w') as data:
            fields = list(self.data_set[0].keys())
            data_writer = DictWriter(data, fieldnames=fields, delimiter=';')
            data_writer.writeheader()
            for item in self.data_set:
                data_writer.writerow(item)


    def sanitize_output(self):
        with open('dataset.csv', 'r+') as data:
            content = data.read()
            content.replace('"', '')
            data.write(content)

if __name__ == '__main__':
    data_gen = DataSetGen()
    data_gen.PAGE_MAX = 1
    data_gen.platform_to_tag = {
        "askubuntu": [
            "apt"
        ]
    }
    data_gen.collect_urls()
    data_gen.data_from_url()
    data_gen.write_to_csv()
    data_gen.sanitize_output()


