Vietnam Stock Financial Statement crawling

This repository is made for financial statement crawling of Viet Name stocks exchange. Financial statements include: Balance Sheet, Income Statement, Cashflow Statement and Ratios. 
I finished this code within an afternoon so little optimization efforts were put in. It would be great if you can help me improve the code.

Requirements:
- Python (3+)
- Pandas (0.25+)
- Selenium (3.14+)

Installations:
- Download the repository
- Install the required libraries
- Download the webdriver, preferrably Chrome, at https://chromedriver.chromium.org/downloads
- Rename the driver_path variable in each files with the location of the webdriver you downloaded
- Create 4 folders for saving data, Balance, Cashflow, Income and Ratios. Inside of each folder you need to create additional 4 folders, which are Bank, Securities, Insurance and Others. The crawled data will be located in those folders respectively of their statement type
- Run the code and wait for the crawling process

The download data will be stored as csv file, in each Folder of their names. Bank for banking data, securities for securities company, insurance for insurance company and others for the rest.

This code will crawl the data of the stock listed in the Code.csv file, including all stocks listed on HOSE. You can modify the stocks to be crawled in that file.


