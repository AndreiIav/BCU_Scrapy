# Overview
This is a Scrapy project to crawl and scrape data from [https://documente.bcucluj.ro/periodice.html](https://documente.bcucluj.ro/periodice.html).
Besides the Scrapy spider, it also contains scripts to generate the database and other required
files. 


# Extracted Data
This project extracts all the relevant data of the magazines by traversing the magazine links found on the starting page.
All the magazines names, years, numbers and the pdf content are saved in a sqlite database. 


# Installation
Pull down the source code from GitHub:\
`git clone https://github.com/AndreiIav/BCU_Scrapy_Scrapper.git`

Create a new virtual environment

Activate the virtual environment

Install the python packages specified in requirements.txt:\
`(venv) $ pip install -r requirements.txt`


# Configuration
In order for the scripts and spider to run, the following environment variables
need to be set:
- BASE_PATH - pointing to the project root folder
- DATABASE_NAME - the name of the sqlite database file

These can be set in an .env file that needs to be present in root_folder.

# Database
In order for the scrapper to run, a sqlite database needs to exist in root folder.
A new database with the correct schema can be created by running the **create_database.py** script
(the script is located in root_folder\src\scripts).


# Other Required Files
In order for the scrapper to run, a *wanted_magazines.txt* file needs to exist in root_folder\extra.
The file and the names of magazines needed for scrapping can be added manually (every magazine name
on a new line).\
Or, by running the **create_wanted_magazines_file.py** script a new *wanted_magazines.txt* file will be
created in the correct location. The file is created by checking what magazine names exists at [https://documente.bcucluj.ro/periodice.html](https://documente.bcucluj.ro/periodice.html)
but not in the database in magazines table (the script is located in root_folder\src\scripts).\
Also, the **create_wanted_magazines_file.py** script checks if a *list_of_magazines_not_to_be_scrapped.txt*
exists in root_folder\extra. This file is optional and can be removed if desired, or other magazine names can be added to it (every magazine name on a new line).

# Running the Spider
Go to root_folder\src\BcuSpider and run:\
`(venv) $ scrapy crawl bcu`


# Key Python Modules Used
- **Scrapy**: a web crawling and web scraping framework
- **requests**: Python library for HTTP requests
- **beautifulsoup4**: Python library for pulling data out of HTML and XML files
- **pypdf**: Python library for working with PDF files
- **pytest**: framework for testing Python projects
- **pytest-cov**: pytest extension for running coverage\.py to check code coverage of tests
- **python-dotenv**: Python library for reading .env files


# Testing
To run all the tests:\
`(venv) $ pytest`

To check the code coverage of the tests:\
`(venv) $ pytest --cov-report term-missing --cov=src`