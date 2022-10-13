# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pyarrow import feather
import os
import pandas as pd
from bs4 import BeautifulSoup

from datetime import datetime
import re

def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
  
    # return data by retrieving the tag content
    return '|'.join(soup.stripped_strings)

def format_time(string):

    d = datetime.strptime(string, "%B %d, %Y")
    formated =  datetime.strftime(d, "%d-%m-%Y")
    return formated 


class MiningWebPipeline:
    
    def open_spider(self, spider):
        wcd = os.getcwd()
        feather_path = wcd + '/feather'
        if os.path.isfile(feather_path):
            try:
                self.df = feather.read_feather(feather_path)

            except Exception as e:
                print({"File format not corrrect": e})
            
        else:
            # create empty dataframe
            self.df = pd.DataFrame(columns=["Title", "Author", "Date", "Text"])

    def close_spider(self, spider):
        # no need to close the file as the contents are read into self.df
        # but read the results into the file

        # The feather format does not permit lists as a value.
        # Have to split the text into multiple rows and then have duplicate data in title, Author, Date
        wcd = os.getcwd()
        feather_path = wcd + '/feather'
        # Have to implement that the data is not just dumped but written to the file 
        # lets test it first
        # x = feather.read_feather(feather_path)
        self.df.to_feather(feather_path)

    def process_item(self, item, spider):
        # i think process item is called everytime the crawler yields an item.
        # This is the reason why I had the same thing multipletimes in my end dataframe.

        # turn the item into a pandas data frame and then put it into the feather file 
        # The above comment means that the ItemAdapter is also called everytime.
        # This is very inefficient. This means that the dict conversion as well as everything else is
        # done multiple times for one site. 
        # But we want only one do prossess the item one time.
        adapter = ItemAdapter(item).asdict()
        # convert the adapter dict to a series of only the vlaues and then add it to the df
        
        # actually we want to split the text sections and put date etc into a seperate column
        clean_dict = dict()
        for x,y in adapter.items():
            clean_vals = list()
            for i in y:
                clean_vals.append(remove_tags(i))
            clean_dict[x] = clean_vals

        # cleaning Author and Date
        # from author we have to clean the "by" and In the website we have two dates.
        # The first, which we keep, is the publishing date and the second is the last changed date, which we wont keep
        # Date clean did not work at all
        # First strip the second non imporatnt date and then take the string and reformat the time
        clean_dict.update({'Author': clean_dict['Author'][0][2:].lstrip(), 'Date': format_time(re.sub('\\|(.*)$','',clean_dict['Date'][0]))})
                
        # converts all the key value pairs of the dict into a Series containing the values
        cur_df = pd.DataFrame({ key:pd.Series(value) for key, value in clean_dict.items() })

        # get rid of the NaN in Title, Author, Date using forwardfill
        cur_df = cur_df.fillna(method='ffill')
        # I think i first have to split the Text column and do not append a list
        # This does not work at all
        print(cur_df)
        self.df = pd.concat([self.df, cur_df], ignore_index=True)

        # write the data to the feather if the file exceeds 250mb
        if (self.df.memory_usage(deep=True).sum() / 1000000) > 250:
            wcd = os.getcwd()
            feather_path = wcd + '/feather'
            self.df.to_feather(feather_path)
            self.df.drop(self.df.index, inplace=True)

        return item
