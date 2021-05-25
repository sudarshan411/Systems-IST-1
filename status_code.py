#!/usr/bin/env python3

import requests
import click
import time

# python3 status_code.py youtube.com 5
# will fetch status code of website after every timer seconds

@click.command()
@click.argument('website')
@click.argument('timer', default=60)
def main(website, timer):
    addr = "https://" + website
    print(addr)
    while True:
        resp = requests.get(addr)
        if resp.status_code == 200:
            print("The website is working")
        else:
            print("Website has error : " + resp.status_code)
        time.sleep(timer)

if __name__ == "__main__":
    main()