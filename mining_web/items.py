# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#import scrapy
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MiningWebItem:
    Title: Optional[str] = field(default=None)
    Author: Optional[str] = field(default=None)
    Date: Optional[str] = field(default=None)
    Text: Optional[str] = field(default=None)


# class MiningWebItem(scrapy.Item):
# Title = scrapy.Field()
#By = scrapy.Field()
#Date = scrapy.Field()
# Text = scrapy.Field()
