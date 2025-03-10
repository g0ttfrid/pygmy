#!/usr/bin/python3
import argparse
import re
import urllib3
import time
from requests import get

urllib3.disable_warnings()

regex = {
"aws_client_id": r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
"aws_mws_key": r"amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
"aws_secret_key": r"(?i)(secret|aws)(.{0,21})?['\"][0-9a-zA-Z\/+]{40}['\"]",
"aws_bucket": r"s3\.amazonaws.com[/][A-Za-z0-9_-]+|[a-zA-Z0-9_-]*\.s3.amazonaws.com",
"google_api_key": r"AIza[0-9A-Za-z\\-_]{35}",
"google_oauth_2.0": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
"google_cloud_plataform": r"(?i)(google|gcp|youtube|drive|yt)(.{0,20})?['\"][AIza[0-9a-z\\-_]{35}]['\"]",
"slack_token": r"xox[baprs]-([0-9a-zA-Z]{10,48})?",
"postman": r"\bPMAK-[a-zA-Z0-9]{32}-[a-zA-Z0-9]{32}\b",
"basic_auth": r"(?<=:\/\/)[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+",
"github": r"(?:ghp|gho|ghu|ghs|ghr)_[0-9a-zA-Z]{42}",
"ip address": r"\b((?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))\b",
"generic api": r"(?i)(?:key|api|token|secret|client|passwd|password|auth|access)(?:[0-9a-z\\-_\\t .]{0,20})(?:[\\s|']|[\\s|\"]){0,3}(?:=|>|:{1,3}=|\\|\\|:|<=|=>|:|\\?=)(?:'|\"|\\s|=|\\x60){0,5}([0-9a-z\\-_.=]{10,150})(?:['|\"|\\n|\\r|\\s|\\x60|;]|$)",
"terraform": r"(typeform)([0-9a-z\\-_\\s.]{0,20})([\\s|']|[\\s|\"]){0,3}(=|>|:{1,3}=|\\|\\|:|<=|=>|:|\\?=)('|\"|\\s|=|\\x60){0,5}(tfp_[a-z0-9\\-_\\.=]{59})(['|\"|\\n|\\r|\\s|\\x60|;]|$)"}

def parse_args():
    parser = argparse.ArgumentParser(usage='pygmy.py -f url_list.txt')
    parser.add_argument('-f', '--file', type=argparse.FileType('r', encoding='utf-8'), required=True)
    return parser.parse_args()

def search(list):
    data = set()
    urls = list.readlines()
    print(f'[>] File with {len(urls)} lines')
    for url in urls:
        try:
            r = get(url.rstrip(), timeout=(3), verify=False)
            for k,v in regex.items():
                try:
                    x = re.findall(v, r.text)
                    if x:
                        #print(f'[+] {k}: {x} >> {url.rstrip()}')
                        data.add(f'[+] {k}: {x} >> {url.rstrip()}') 
                except:
                    #print(f'[!] error regex pattern {k} ({e})')
                    pass
        except Exception as e:
            data.add(f'[!] error request {url.rstrip()} ({e})')
            #print(f'[!] error request {url.rstrip()} ({e})')
    return data

def logger(list):
    filename = f"output_{time.time()}.txt"
    print(f"[>] Save output {filename}")
    with open(filename, 'w', encoding='utf-8') as f:
        for line in list:
            f.write(f'{line}\n')

if __name__ == '__main__':
    try:
        args = parse_args()
        logger(search(args.file))
    except KeyboardInterrupt:
        print('[!] Stopping')
