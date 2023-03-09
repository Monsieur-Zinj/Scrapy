import os
# print the current working directory
print(os.getcwd())

# import the spider
from spiders import get_py_2
from scrapyscript import Job, Processor
import json

# run the spider and save the result in a json file

from scrapy.crawler import CrawlerProcess
#from scrapy.utils.project import get_project_settings

# process = CrawlerProcess(get_project_settings())
# process.crawl(get_py_2.GetPySpider)
# process.start(stop_after_crawl=True)
processor = Processor(settings=None)

pythonJob = Job(get_py_2.GetPySpider, url=['http://github.com/Monsieur-Zinj/blog'])

#Start the reactor, and block until all spiders complete.
data = processor.run([pythonJob])

# Print the consolidated results

# write data in a json
with open("py_lib_scrap/py_lib_2.json", "w") as f:
    json.dump(data, f)

print(data)













# import result of the spider, py_lib_2.json
# this json file contains the libraries used in the .py files of the github repository
#
# the json file is a list of dictionaries
# each dictionary contains the url of the .py file and the libraries used in it

import json
with open("py_lib_scrap/py_lib_2.json", "r") as f:
    data = json.load(f)

# create a list of all the libraries used in the .py files
# this list is a list of strings


# make a datafram with this
import astpretty
import ast
import pandas as pd
#df = pd.DataFrame(lib, columns=["lib"])
#print(lib[0])

# print the ast 

#astpretty.pprint(ast.parse(lib[0]).body[4])



