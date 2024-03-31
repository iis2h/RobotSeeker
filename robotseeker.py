#!/bin/python3

import aiohttp
import asyncio
import argparse
import re
import os

# Argumetns
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, metavar='File', help='Path to the input file')
parser.add_argument('-m', action='store_true', help='Map the content of "robots.txt" to its corresponding URL')
parser.add_argument('-g', action='store_true', help="Generate a wordlist")
parser.add_argument('-r', type=int, metavar='Rate Limit', default=3, help='Requests per second (Default is 3)')
parser.add_argument('-v', action='store_true', help="Verbose - Display all status codes")
parser.add_argument('-q', action='store_false', help='Don\'t display banner')
parser.add_argument('--version', action='store_true', help="Version")

# ANSI Colors
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BLUE = '\033[34m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Banner
def banner():
    banner = r'''
  ___  ___  ___  ___ _____ ___ ___ ___ _  _____ ___ 
 | _ \/ _ \| _ )/ _ |_   _/ __| __| __| |/ | __| _ \
 |   | (_) | _ | (_) || | \__ | _|| _|| ' <| _||   /
 |_|_\\___/|___/\___/ |_| |___|___|___|_|\_|___|_|_\
'''
    print(banner)
    print(f" Crafted with Passion by iis2h aka {BLUE}Frenzy{RESET}\n")

# Filter input data
def urls_filter(input_data):
    with open(input_data, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        urls = []
        for url in lines:
            if url.startswith('http') and '*' not in url:
                pattern = re.compile(r'(https?://[^/?]+).*')
                urls.append(pattern.sub(r'\1', url) + '/robots.txt')
        return sorted(set(urls))

# Create unique output file names
def unique_filename(base):
    file_number = 1
    file_name = f'{base}_{file_number}.txt'
    while os.path.exists(file_name):
        file_number += 1
        file_name = f'{base}_{file_number}.txt'
    return file_name

# Generate a wordlist
def wordlist_generator(content):
    words_to_remove = ['user-ano_domainst','disallow', 'allow', 'crawl-delay' , 'googlebot', 
                       'user-ano_domainstadsbot-google', 'user-ano_domainstadsbot-google-mobile', 
                       'user-ano_domainstgooglebot-image', 'googlebot-image', 'www.robotstxt.org', 
                       'googlebot-news', 'robotstxt', 'robotstxt.html']
    symbols_to_remove = {ord('$') : None,  ord('*') : None, ord('(') : None, ord(')') : None, 
                         ord('#') : None, ord(':') : None, ord('!') : None, ord('"') : None,
                         ord('%') : None}   
    # Regex Patterns
    pattern = r'^-*|-$|\.$|^\.\w+$'
    domain_pattern = re.compile(r'(\w+)\.(\w+)\.(\w+)')    
    # Replace symbols with spaces
    lines = [line.replace('/', ' ').replace('&', ' ').replace('=', ' ')
             .replace('?', ' ').replace(',', ' ') 
             for line in content]   
    # Translate over {symbols_to_remove}
    no_symbols = [re.sub(pattern , '', item.translate(symbols_to_remove)) 
            for value in lines 
            for item in value.split(' ')]   
    # Seperate 'www.example.com' into three words (www , example , com)
    no_domains = [item for word in no_symbols 
           for item in (domain_pattern.match(word).groups() 
            if domain_pattern.match(word) else [word])]  
    # Final Pure Wordlist
    wordlist = {str(word).replace('\n', '').replace('\t', '').replace('\r','').strip() 
                for word in no_domains 
                if word.lower() not in words_to_remove and word}  
    return '\n'.join(sorted(set(wordlist)))

# Mapping URLs to the endpoints specified in its robots.txt file
def mapper(url, content):
    # Regex Patterns
    url_pattern = re.compile(r'(https?://[^/?]+).*')
    content_pattern = re.compile(r'(?mi)^(.*)(Disallow|Allow)[:]?\s*')
    symbol_pattern = re.compile(r'\*|\$')   
    lower_text = content.lower()
    # Remove words "Sitemap:", "Host:" and return their value
    if lower_text.startswith(('sitemap:', 'host:')):
        return content.split(':', 1)[1].strip()
    # Discard "Crawl-Delay:" and its value
    elif lower_text.startswith('crawl-delay:'):
        return None
    # Discard Comments
    elif lower_text.startswith('#'):
        return None
    # Dealing with endpoints
    elif '/' in lower_text:
        endpoint = re.sub(content_pattern, '', str(content))
        endpoint = re.sub(symbol_pattern, '', str(endpoint))
        # If the value is a complete URL, add it directly
        if endpoint.startswith(('http://', 'https://')):
            return endpoint.strip()
        else:
            # Append endpoints to the base domain
            base_domain = str(url_pattern.sub(r'\1', str(url)))
            return base_domain + endpoint.strip()

async def fetch(session, url, semaphore):
    try:
        async with semaphore:
            # Requesting method and SSL check is disabled
            async with session.get(url, ssl=False) as response:
                # Check for 'text/plain' in the 'Content-Type' header to identify robots.txt only and discard Soft 404 pages or Blank Pages
                if response.status == 200 and 'text/plain' in response.headers.get('Content-Type', ''):
                    print(f'[{GREEN}{response.status}{RESET}]: {url}')
                    # Return a tuple containing the response body and URL
                    return await response.text(), response.url
                elif args.v and response.status != 200:
                    if response.status == 404:
                        print(f'[{RED}{response.status}{RESET}]: {url}')
                    else:
                        print(f'[{YELLOW}{response.status}{RESET}]: {url}')
                elif args.v:
                    print(f'[{BOLD}BLANK{RESET}]: {url}')
                # Don't return either Body or URL
                return None, None
    except Exception as e:
        if args.v:
            print(f'[{BOLD}{YELLOW}ERROR{RESET}]: {e}')
            # Don't return either Body or URL
            return None, None

async def main():
    # If quiet mode is enabled don't display banner
    if args.q:
        banner()
    else:
        print('\n')
    # Rate Limit function using Semaphore
    semaphore = asyncio.Semaphore(args.r)
    async with aiohttp.ClientSession() as session:
        base_urls = urls_filter(args.f)
        tasks = [fetch(session, url, semaphore) for url in base_urls]
        # List contains valid URLs
        valid = []
        # List contains everything inside robots.txt files
        content = []
        # List contins URLs mapped to the endpoints
        mapped = []
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            # Check if the response exists and it's a tuple with two elements
            if response and len(response) == 2:
                text, url = response
                # Check if the text is not 'None' or Empty
                if text:
                    # If text is there that's mean the url status code is [200 OK], not Soft 404 or Empty Page
                    valid.append(str(url))
                    text_lines = text.splitlines()
                    content.extend(text_lines)
                    # If mapping is enabled
                    if args.m:
                        # Take every item in 'text_lines' list
                        for item in text_lines:
                            # And apply mapper function to it
                            mapped_url = mapper(url, item)
                            # Ensure the result not Empty and then add it to 'mapped' list
                            if mapped_url:
                                mapped.append(mapped_url)                    
        return sorted(set(valid)), content, sorted(set(mapped))

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        if not args.f:
            print(f'\n Please add an input file using -f flag\n')
        else:
            valid, content, mapped = asyncio.run(main())
        if args.f:
            filename = unique_filename('valid')
            with open(filename, 'x') as v:
                v.write('\n'.join(valid))
        if args.g:
            filename = unique_filename('wordlist')
            with open(filename, 'x') as w:
                w.write(wordlist_generator(content))
        if args.m:
            filename = unique_filename('mapped')
            with open(filename, 'x') as w:
                w.write('\n'.join(mapped))
        if args.version:
            version = '2.0.0'
            print(f'Version : {version}')
    except KeyboardInterrupt:
        print(f' \nKeyboard Interrupt\n')