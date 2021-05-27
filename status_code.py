#!/usr/bin/env python3

import requests
import click
import time
from datetime import datetime

# python3 status_code.py 5 3
# will fetch status code of websites in the list 
# after intervals of 5 seconds and this program
# will run for 3 iterations

@click.command()
@click.argument('timer', default=10)
@click.argument('count', default=1)
def main(timer, count):
    # list.txt contains the list of websites to be tracked
    file1 = open('list.txt', 'r')
    lines = file1.readlines()
    file1.close()

    # to store the all the results
    file2 = open('log.txt', 'w')

    # keep running for count iterations
    while count > 0:
        for line in lines:
            addr = "https://" + line.strip()
            print(addr)

            resp = requests.get(addr)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            if resp.status_code == 200:
                str = current_time + " : " + addr + " is working\n"
                file2.write(str)
            else:
                str = current_time + " : " + addr + " has error : " + resp.status_code + "\n"
                file2.write(str)

        # repeat after timer seconds
        time.sleep(timer)
        count -= 1
    
    file2.close()

if __name__ == "__main__":
    main()