import aiohttp
import asyncio
import argparse
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, metavar='File', help='Path to the file')
parser.add_argument('-m', action='store_true', help='Map the content of "robots.txt" to its corresponding URL')
parser.add_argument('-g', action='store_true', help="Generate a wordlist")
parser.add_argument('-v', action='store_true', help="Enable verbose output")
parser.add_argument('-r', type=int, metavar='Rate Limit', default=3, help='Requests per second "Default is 3"')
parser.add_argument('--version', action='store_true', help="Display version")

GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BOLD = '\033[1m'
RESET = '\033[0m'

print('\nProcessing ... \n')

def UrlFilter(inputData):
    with open(inputData, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        urls = set()
        for url in lines:
            if url.startswith('http'):
                pattern = re.compile(r'(https?://[^/?]+).*')
                urls.add(pattern.sub(r'\1', url) + '/robots.txt')
        return urls

def UniqFilename(base):
    file_number = 1
    file_name = f'{base}_{file_number}.txt'
    while os.path.exists(file_name):
        file_number += 1
        file_name = f'{base}_{file_number}.txt'
    return file_name

def WordlistGenerator(text):
    words_to_remove = ['user-agent','disallow', 'allow', 'user-agentadsbot-google', 
                       'user-agentadsbot-google-mobile', 'user-agentgooglebot-image', 
                       'googlebot-image', 'www.robotstxt.org'] 
    symblos_to_remove = {ord('$') : None,  ord('*') : None, ord('(') : None, ord(')') : None, 
                         ord('#') : None, ord(':') : None, ord('!') : None, ord('"') : None} 
    pattern = r'^-*|-$|\.$'
    lines = [line.replace('/', ' ').replace('&', ' ').replace('=', ' ').replace('?', ' ').replace(',', ' ') for line in text]
    init = [re.sub(pattern , '', item.translate(symblos_to_remove)) for value in lines for item in value.split(' ')]
    cleaned = set(str(word) for word in init if word.lower() not in words_to_remove and word != '')
    return '\n'.join(cleaned)

def DirMapper(url, text):
    pattern = re.compile(r'(https?://[^/?]+).*')
    lower_text = text.lower()
    if lower_text.startswith('sitemap:'):
        return lower_text.split(':', 1)[1].strip()
    elif '/' in text and '#' not in text:
        return  str(pattern.sub(r'\1', str(url))) + str(text.replace('Disallow:', '').replace('Allow:', '').strip())

async def fetch(session, url, semaphore):
    try:
        async with semaphore:
            async with session.get(url, ssl=False) as response:
                return await response.text(), response.url, response.status, response.headers.get('Content-Type', '')
    except Exception as e:
        print(f'[{BOLD}{YELLOW}Error{RESET}] : {e}')

async def main():
    semaphore = asyncio.Semaphore(args.r)
    async with aiohttp.ClientSession() as session:
        basic_urls = UrlFilter(args.f)
        tasks = [fetch(session, url, semaphore) for url in basic_urls]
        valid = set()
        texts = []
        mapped = set()
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            if isinstance(response, tuple) and len(response) == 4:
                text, url, status, header = response
                if status == 200 and 'text/plain' in header:
                    print(f'[{BOLD}{GREEN}{status}{RESET}]: {url}')
                    valid.add(str(url))
                    text_lines = text.splitlines()
                    texts.extend(text_lines)
                    if args.m:
                        for item in text_lines:
                            mapped_url = DirMapper(url, item)
                            if mapped_url:
                                mapped.add(mapped_url)
                elif args.v and status != 200:
                    print(f'[{BOLD}{RED}{status}{RESET}]: {url}')        
        
        return valid, texts, sorted(mapped)

if __name__ == '__main__':
    args = parser.parse_args()
    valid, texts, mapped = asyncio.run(main())
    if args.f:
        filename = UniqFilename('robots_valid')
        with open(filename, 'x') as v:
            v.write('\n'.join(valid))
    if args.g:
        filename = UniqFilename('robots_wordlist')
        with open(filename, 'x') as w:
            w.write(WordlistGenerator(texts))
    if args.m:
        filename = UniqFilename('robots_mapped')
        with open(filename, 'x') as w:
            w.write('\n'.join(mapped))
    if args.version:
        version = '1.0.0'
        print(f'Version : {version}')
