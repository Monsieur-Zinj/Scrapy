import scrapy
import re
import time
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from utils import get_func_calls
import ast





class GetPySpider(CrawlSpider):
    name = "get_py_2"
    allowed_domains = ["github.com", "raw.githubusercontent.com"]
    start_urls = []



    # rules : crawl links froms strart_urls containing "tree/main/examples" and not containing "blob"
    # and url termination is ".py"


    rules = [Rule(LinkExtractor(allow=r'/tree/(main|master).*'), follow=True),              
             Rule(LinkExtractor(allow=r'/blob.*.py'), follow=False, callback='parse_py')
            ]
    
    # overwrite __init__ to add start_urls
    def __init__(self, start_urls=['http://github.com/Monsieur-Zinj/blog'], *args, **kwargs):
        super(GetPySpider, self).__init__(*args, **kwargs)
        if start_urls is not None:
            self.start_urls = start_urls



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
            #lib = self.get_lib(response)
            py_file_str=re.findall("<p>(.*)</p>",str(response.css("p").get()),re.DOTALL)[0]
            tree = ast.parse(py_file_str)
            func_call=get_func_calls(tree)
            if func_call!=[]:
                yield {#'title': response.css("title::text").get(),
                    "URL:": response.request.url,
                    #"py_file": re.findall("<p>(.*)</p>",str(response.css("p").get()),re.DOTALL)[0],
                    "func_call": func_call
                    #"py_lib": lib
                    #"lib": response.css("body").re(r"import.*?\n")




                }
    
    def get_lib(self, response):
        rep=response.css("p").get()
        
        # case 1 : looking for pattern like "import xyz" 
        case_1=re.findall("^import (.*?)($|\.)(.*)",str(rep), re.MULTILINE)




        # get the lines containing "import" or "from"
        # lib = re.findall("^( *)(?:from (.*?)(\.| |import)|import (.*?)\n)", str(rep), re.MULTILINE )
        
        # get group 2 and 4

        
        lib=case_1

        # remove duplicates
        #lib = list(dict.fromkeys(lib))
        #print(ast.dump(ast.parse('x += 5').body[0]))"
        
        
        
        return lib
 

# run the spider
# should be run from py_lib_scrap directory
# -0 option to erase the previous json file
# scrapy runspider spiders/get_py_2.py -O py_lib_2.json

