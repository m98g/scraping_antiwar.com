# scraping_antiwar.com
A simple web scraper to scrape the articles from antiwar.com


## Spider usage

Define a starting Url (an article by Antiwar) and the spider will terminate by the defined data in the last for loop in the antiwarSpider.
The spider will download the page get the Tile, Author, Date and the paragraphs from the main content body of the page.

## Data pipeline

After each page beeing processed the item containing Title, Author, Date and Text will be processed cleaned and put into the dataframe within the pipelineobject. If the dataframe surpasses 250mb it will be written to the "feather" file.

When the spider closes the remaining data or the dataframe, depending on how much data was processes is written to the fether file.

The feather file format was chosen, because it is small in footprint and can be quickly passed between Python and R.

The dataframe has the fixed column names of "Title", "Author", "Date", "Text".

## Shutting down the spider

Either the spider will be shut down if it reaches the target date or manually kill it just use Control + C in the terminal. The data will not be lost by Control + C.

## Performance

This spider is slow and more a prove of concept. It is easy to run and easy on the website. The structure of antiwar.com made it easy to download every article in a chronological fashion. Under each articel is a link to the previously published article, which the spider follows.

The primary goal is ony to obtain the text data for sentiment analysis and hence I was satisfied with the issue that I will just have to invest some time. I will only load everything once and hence dont really care about the performance.
