#!/usr/bin/python3
import argparse
import re
import urllib3
from requests import get
from tqdm import tqdm

urllib3.disable_warnings()

regex = {
"aws_client_id": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
"aws_mws_key": r"amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
"aws_secret_key": r"(?i)(secret|aws)(.{0,21})?['\"][0-9a-zA-Z\/+]{40}['\"]",
"aws_bucket": r"s3\.amazonaws.com[/][A-Za-z0-9_-]+|[a-zA-Z0-9_-]*\.s3.amazonaws.com",
"google_api_key": r"AIza[0-9A-Za-z\\-_]{35}",
"google_oauth_2.0": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
"google_cloud_plataform": r"(?i)(google|gcp|youtube|drive|yt)(.{0,20})?['\"][AIza[0-9a-z\\-_]{35}]['\"]",
"slack_token": r"xox[baprs]-([0-9a-zA-Z]{10,48})?",
"basic_auth": r"(?<=:\/\/)[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+",
"github": r"(?i)github(.{0,20})?['\"][0-9a-zA-Z]{35,40}"}

def parse_args():
    parser = argparse.ArgumentParser(usage='pygmy.py -f url_list.txt')
    parser.add_argument('-f', '--file', type=open, required=True)
    return parser.parse_args()

def search(list):
    data = set()
    urls = list.readlines()
    print(f'[!] File with {len(urls)} lines')
    for url in tqdm(urls):
        try:
            r = get(url.rstrip(), timeout=(3), verify=False)
            for k,v in regex.items():
                x = re.search(v, r.text)
                if x:
                    data.add(f'[+] {k}: {x.group(0)} >> {url.rstrip()}')
        except Exception:
            data.add(f'[-] Error in {url.rstrip()}')
    return data

def logger(list):
    with open('output.txt', 'a+', encoding='utf-8') as f:
        for line in list:
            f.write(f'{line}\n')

if __name__ == '__main__':
    try:
        args = parse_args()
        logger(search(args.file))
    except KeyboardInterrupt:
        print('[!] Stopping')
