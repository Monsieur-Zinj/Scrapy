import scrapy
import re
import time
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class GetPySpider(CrawlSpider):
    name = "get_py_2"
    allowed_domains = ["github.com", "raw.githubusercontent.com"]
    start_urls = ["https://github.com/Monsieur-Zinj/blog", "https://github.com/boilercodes/python"]



    # rules : crawl links froms strart_urls containing "tree/main/examples" and not containing "blob"
    # and url termination is ".py"

    rules = [Rule(LinkExtractor(allow=r'/tree/(main|master).*'), follow=True),              
             Rule(LinkExtractor(allow=r'/blob.*.py'), follow=False, callback='parse_py')
            ]
    
    def parse_py(self, response):
        


        # searching for next page, exist if we currently are on a .py page
        next_page = response.xpath('//*[@class="BtnGroup"]/a/@href').extract_first()

        # if we are on a .py page, we reach the raw py file
        if next_page!=None:
            next_page=next_page.replace("/raw","")
            next_page="https://raw.githubusercontent.com"+next_page
            yield response.follow(next_page, callback=self.parse_py)

        # if not, we are already on the raw py file
        # so we can extract the libraries
        else:
            lib = self.get_lib(response)
            if lib!=[]:
                yield {#'title': response.css("title::text").get(),
                    "URL:": response.request.url,
                    "py_file": lib
                    #"lib": response.css("body").re(r"import.*?\n")




                }
    
    def get_lib(self, response):
        rep=response.css("p").get()
        # in rep, match the lines containing "import" or "from"

        # get the lines containing "import" or "from"
        lib = re.findall("(?:from (.*?)\.|^import (.*?)(?: as |$))", rep, re.MULTILINE )
        # concatenate all elements of lib
        lib = [item for sublist in lib for item in sublist]
        # remove empty strings
        lib = [x for x in lib if x]
        # remove duplicates
        lib = list(dict.fromkeys(lib))
        
        
        
        return lib


# run the spider
# should be run from py_lib_scrap directory
# -0 option to erase the previous json file
# scrapy runspider get_py_2.py -O py_lib_2.json