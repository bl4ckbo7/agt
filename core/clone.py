#!/usr/bin/env python3

"""
Title: Advanced Git Tool Clone Module
Author: bl4ckbo7
Twitter: @0x616e6479
Date: Mon April 24, 2019

--------------------------------------------------------------------

    Objectives:
    -----------
	1) Clones respositories into specified output directory. Default: ~/.clones
    2) Supports multiple repositories cloning. (Multi-cloning)

---------------------------------------------------------------------
"""

import os
import git
import copy
import requests
import consolemd
from core.conf import Conf
import multiprocessing


class Clone(object):

    def __init__(self, *args, **kwargs):
        #Actually, nothing much to construct here.
        pass
    
    def parseListFile(self, path):

        #check if path to file exists
        if os.path.exists(os.path.expanduser(path)):
            lines = [line.rstrip('\n') for line in open(path)]
            return lines
        else:
            print("[x] Can't access '{}': No such file or directory.".format(path))
            exit(1)

    def cloner(self, full_name):
        
        git_url = Conf.URLS['GITHUB_HTML_URL'] + "{}.git".format(full_name)

        #check if path to dir exists
        if os.path.exists(os.path.expanduser(Conf.DEFAULTS['OUTPUT_DIR']+full_name.split("/")[1])) == True:
            print("[x] {} directory already exists!".format(full_name.split("/")[1]))
        else:
            git.Git(os.path.expanduser(Conf.DEFAULTS['OUTPUT_DIR'])).clone(git_url)
            print("[!] {} successfully cloned.".format(full_name))

    def cpu(self, lists):
        
        processes = []
        invalid_urls = []
        repolist = lists
        
        repos_copy = copy.deepcopy(repolist)
        
        print("\n[~] Parsing repositories list...\n")

        for full_name in repos_copy:

            #check full name if it's valid
            names = full_name.split("/")
            
            if len(names) < 2:
                print("[x] '{}' incorrect full name syntax. SYNTAX: <user>/<repository name>".format(full_name))
                invalid_urls.append(full_name)
                repolist.remove(full_name)

        if len(repolist) != 0:
            for full_name in repos_copy:
                if full_name in repolist:
                    #check if the url path to repository is OK
                    git_url = Conf.URLS['GITHUB_HTML_URL'] + "{}".format(full_name)
                    r = requests.get(git_url)

                    if r.status_code != 200:
                        invalid_urls.append(full_name)
                        repolist.remove(full_name)
                    
            total_urls = len(repolist)

            print("\n[~] Preparing to clone " + str(total_urls) + " repository(s)...\n")

            for x in repolist:
                print("[+] {}, ".format(x))

            print("\n")

            for i in range(total_urls):
                p = multiprocessing.Process(target=self.cloner, args=(repolist[i],))
                processes.append(p)

            for p in processes:
                p.start()
                p.join()

            if len(invalid_urls) != 0:
                print("\n[!] NOT FOUND Repository(s):")
                for x in invalid_urls:
                    print("     [-] %s" %x)
                print("\n")
            else:
                pass