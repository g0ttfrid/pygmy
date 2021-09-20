#!/usr/bin/python3
import argparse, requests, re, urllib3
urllib3.disable_warnings()

regex = {
"aws_client_id": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
"aws_mws_key": r"amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
"aws_secret_key": r"(?i)(secret|aws)(.{0,21})?['\"][0-9a-zA-Z\/+]{40}['\"]",
"aws_bucket": r"s3\.amazonaws.com[/][A-Za-z0-9_-]+|[a-zA-Z0-9_-]*\.s3.amazonaws.com",
"google_api_key": r"[A-Za-z0-9_]{21}--[A-Za-z0-9_]{8}",
"google_oauth_2.0": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
"google_cloud_plataform": r"(?i)(google|gcp|youtube|drive|yt)(.{0,20})?['\"][AIza[0-9a-z\\-_]{35}]['\"]",
"slack_token": r"xox[baprs]-([0-9a-zA-Z]{10,48})?",
"basic_auth": r"(?<=:\/\/)[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+",
"github": r"(?i)github(.{0,20})?['\"][0-9a-zA-Z]{35,40}"}

def parse_args():
    parser = argparse.ArgumentParser(usage='pygmy.py -f urls.txt')
    parser.add_argument('-f', '--file', type=open, required=True)
    return parser.parse_args()

def search(urls):
    for url in urls:
        try:
            r = requests.get(url.rstrip(), timeout=(3), verify=False)
            for k,v in regex.items():
                x = re.search(v, str(r.content))
                if x:
                    print(f"[+] Possible {k}: {x.group(0)} >> {url.rstrip()}")
        except:
            print(f"[-] Error in {url.rstrip()}")

try:
    args = parse_args()
    search(args.file)
except KeyboardInterrupt:
    print('Stopping')
