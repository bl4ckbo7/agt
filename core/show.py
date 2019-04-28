#!/usr/bin/env python3

"""
Title: Search Module for Advanced Git Tool
Author: bl4ckbo7
Twitter: @0x616e6479
Date: Mon April 22, 2019
Dependency: sudo apt-get install python3-texttable	Install python3 texttable package

--------------------------------------------------------------------

    Objectives:
    -----------
	1) Shows Details of a particular repository.
    2) Lists the contents of a repository.
    3) Renders README.md markdown file.

---------------------------------------------------------------------
"""

import os
import time
import requests
import consolemd
import texttable as tt
from core.conf import Conf


showtable = tt.Texttable()

headers = [
			'ID',
			'File Name',
			'HTML File URL',
			'File Size',
            'Raw File URL'
		   ]

showtable.header(headers)

class Show:

    def __init__(self, full_name):
        self.full_name = full_name


    def getRepositoryDetails(self):
        
        r = requests.get(Conf.URLS['GITHUB_API_URL'] + "repos/" + self.full_name)

        if r.status_code != 200:
            print("[x] Unable to fetch '{}'. (NOT FOUND)".format(self.full_name) + "\n")
            exit(1)
        else:
            pass

        langs = requests.get(Conf.URLS['GITHUB_API_URL'] + "repos/" + self.full_name + "/languages")
        langs = langs.json()

        repositoryDetails = r.json()

        repositoryDetails.update({'languages': langs})

        return repositoryDetails


    def getRepositoryContents(self):
        print("\n[~] Fetching repository contents...\n")

        r = requests.get(Conf.URLS['GITHUB_API_URL'] + "repos/" + self.full_name + "/contents/")

        if r.status_code != 200:
            print("[x] Unable to fetch '{}'. (NOT FOUND)".format(self.full_name) + "\n")
            exit(1)
        else:
            pass

        repositoryContents = r.json()

        time.sleep(2)

        print("[!] Done...\n\n")

        time.sleep(3)

        return repositoryContents


    def printRepositoryContents(self, response):
        contents = response
        contents_total = len(contents)
        count = 0	

        for position in range(contents_total):

            count = count + 1

            if len(str(contents[position]['name'])) > 117:
                showtable.add_row([str(count) , contents[position]['name'] , contents[position]['html_url'] , str(format((contents[position]['size'] / 1024), '.2f') + " KB"), contents[position]['download_url']])

            else:
                showtable.add_row([str(count) , contents[position]['name'] , contents[position]['html_url'] , str(format((contents[position]['size'] / 1024), '.2f') + " KB"), contents[position]['download_url']])

        print("[!] " + str(contents_total) + " repository contents. \n\n" + showtable.draw())


    def getREADME(self):
        url = Conf.URLS['RAW_FILE_URL'] + self.full_name + "/master/README.md"
        r = requests.get(url)

        if r.status_code != 200:
            url = Conf.URLS['RAW_FILE_URL'] + self.full_name + "/master/README.rst"
            r = requests.get(url)

            if r.status_code != 200:
                print("\n[x] README File NOT Found.\n")
                exit(1)

        open(os.path.expanduser(Conf.DEFAULTS['TEMP_DIR'] + 'README'), 'wb').write(r.content)


    def parseREADME(self):
        with open(os.path.expanduser(Conf.DEFAULTS['TEMP_DIR'] + 'README'), 'r') as file:
            file_content = file.read()

        renderer = consolemd.Renderer()
        renderer.render(file_content)

        os.remove(os.path.expanduser(Conf.DEFAULTS['TEMP_DIR'] + 'README'))