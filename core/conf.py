#!/usr/bin/env python3

"""
Title: Advanced GIT Tool Initial Configs
Author: bl4ckbo7
Twitter: @0x616e6479
Date: Sat April 27, 2019
"""


class Conf:

        URLS = {
                'RAW_FILE_URL' : 'https://raw.githubusercontent.com/',
                'GITHUB_API_URL' : 'https://api.github.com/',
                'GITHUB_HTML_URL' : 'https://github.com/'
        }

        DEFAULTS = {
                'OUTPUT_DIR' : '~/.agt/clones/', #Default clones output directory.
                'TEMP_DIR' : '~/.agt/temp/', #Default temporary storage direactory
                'RESULTS_PER_PAGE' : '32',
                'DEFAULT_PAGE_NUMBER' : '1',
                'QUERY_TYPE' : 'DEFAULT',
                'SORT_FILTER' : '',        #|---Best match,
                'ORDER_FILTER' : 'desc'    #|---when combined together.
        }

        MISC = {
                'VERSION' : '1.0.1',
                'STAGE' : 'stable'
        }