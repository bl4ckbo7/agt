#!/usr/bin/env python3

"""
Title: Advanced Git Tool Search Module
Author: bl4ckbo7
Twitter: @0x616e6479
Date: Mon April 22, 2019
Dependency: sudo apt-get install python3-texttable	Install python3 texttable package

--------------------------------------------------------------------

	Objectives:
	-----------
		1) Search a topic or repository.
		2) Render the results.
		3) Sort &/or Order and Paginate the search results.
	
	Sort Options:
	-------------
		1)Best Match (&s=)
		2)Most Stars (&s=stars)
		3)Fewest Stars (&s=stars)
		4)Most Forks (&s=forks)
		5)Fewest Forks (&s=forks)
		6)Recently Updated (&s=updated)
		7)Least recently updated (&s=updated)

	Order Options:
	--------------
		1)Ascending (?o=asc)
		2)Descending (?o=desc)

---------------------------------------------------------------------
"""

import requests
import texttable as tt
from core.conf import Conf

searchtable = tt.Texttable()

headers = [
			'ID',
			'User/Repository',
			'Repository URL',
			'Repository Description',
			'Stars', 
			'Forks'
		   ]

searchtable.header(headers)

class Search:

		def __init__(self, query, page, per_page, sort, order):
			self.query = query
			self.page = page
			self.per_page = per_page
			self.sort = sort
			self.order = order

		
		def getAllRepositories(self, response):

			repositories = response['items']

			return repositories


		def printRepositoryResults(self, response):

			git_items_total = response['total_count']
			git_items = response['items']
			count = 0	

			for position in range(len(git_items)):

				count = count + 1

				if len(str(git_items[position]['description'])) > 117:
					searchtable.add_row([str(count) , git_items[position]['full_name'] , git_items[position]['html_url'] , str(git_items[position]['description'])[:117]+"...", git_items[position]['stargazers_count'], git_items[position]['forks_count']])

				else:
					searchtable.add_row([str(count) , git_items[position]['full_name'] , git_items[position]['html_url'] , str(git_items[position]['description']), git_items[position]['stargazers_count'], git_items[position]['forks_count']])

			if int(self.per_page) < git_items_total:
				print("\n[!] " + str(git_items_total) + " repository results. \n" + "[!] Displaying Only " + self.per_page + " results.\n\n" + searchtable.draw())
			else:
				print("\n[!] " + str(git_items_total) + " repository results. \n" + "[!] Displaying Only " + str(git_items_total) + " results.\n\n" + searchtable.draw())


		def search(self, qtype):

			"""

			Query Types:
			------------
			
				1) Default Query
					-Only Search 'Repository Name'.
				2) Topic Query 
					-Only Search 'Topic Name' (Takes only a single argument value i.e only one topic).

			"""

			if qtype == "DEFAULT":
				
				r = requests.get(Conf.URLS['GITHUB_API_URL'] + "search/repositories?order=" + self.order + "&sort=" + self.sort + "&q=" + self.query + "&page=" + self.page + "&per_page=" + self.per_page)
				response = r.json()

			elif qtype == "TOPIC":
				
				r = requests.get(Conf.URLS['GITHUB_API_URL'] + "search/repositories?order=" + self.order + "&sort=" + self.sort + "&q=topic:" + self.query + "&page=" + self.page + "&per_page=" + self.per_page)
				response = r.json()

			return response			