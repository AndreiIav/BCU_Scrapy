# Overview
This is a Python Scrapy project to crawl and scrape data from [https://documente.bcucluj.ro/periodice.html](https://documente.bcucluj.ro/periodice.html).
Besides the Scrapy spider, it also contains scripts to generate the database and other required
files. 


# Extracted Data
This project extracts all the relevant data of the digitized magazines by traversing the magazine links found on the [starting page](https://documente.bcucluj.ro/periodice.html) (and also present in _wanted_magazines.txt_ file).
All the magazines names, years, numbers and their PDF content are saved in a SQLite database. 


# Installation
Pull down the source code from GitHub:\
`git clone https://github.com/AndreiIav/BCU_Scrapy.git`

Change the current working directory to the 'BCU_Scrapy' directory. 

Create and activate a virtual environment:\
On Linux:\
Create the virtual environment:\
`python3 -m venv venv`\
Activate the virtual environment:\
`source venv/bin/activate`

On Windows:\
Create the virtual environment:\
`python -m venv venv`\
Activate the virtual environment:\
`venv\Scripts\activate`

Install the python packages specified in requirements.txt:\
`(venv) $ pip install -r requirements.txt`


# Configuration
In order for the scripts and spider to run, the following environment variables need to be set:
- **BASE_PATH** - the absolute path of the 'BCU_Scrapy' directory (e.g.: BASE_PATH='absolute_path/to/BCU_Scrapy')
- **DATABASE_NAME** - the desired name of the SQLite database file (this needs to have the '.db' extension )(e.g. : DATABASE_NAME='app.db')

These can be set in an _.env_ file that needs to be present in 'BCU_Scrapy' directory.

# Database
In order for the _BCU_Scrapy_ to run, a SQLite database needs to exist in 'BCU_Scrapy' directory.
A new database with the correct schema can be created by running the **create_database.py** script:\
`(venv) $ python -m src.scripts.create_database`


# Other Required Files
In order for the _BCU_Scrapy_ to run, a *wanted_magazines.txt* file needs to exist in BCU_Scrapy/extra directory.
The file and the names of magazines needed for scrapping can be added manually (every magazine name
on a new line).\
Or, by running the **create_wanted_magazines_file.py** script a new *wanted_magazines.txt* file will be
created in the correct location:\
`(venv) $ python -m src.scripts.create_wanted_magazines_file`\
The file is created by checking what magazine names exists at [https://documente.bcucluj.ro/periodice.html](https://documente.bcucluj.ro/periodice.html)
but not in the database in _magazines_ table.\
Also, the **create_wanted_magazines_file.py** script checks if a *list_of_magazines_not_to_be_scrapped.txt*
exists in BCU_Scrapy/extra directory. This file is optional and can be removed if desired, or other magazine names can be added to it (every magazine name on a new line).

# Running the Spider
In order to run the spider change the current working directory to  BCU_Scrapy/src/BcuSpider and run the following command:\
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
Make sure the current working directory is set to BCU_Scrapy.

To run all the tests:\
`(venv) $ pytest`

To check the code coverage of the tests:\
`(venv) $ pytest --cov-report term-missing --cov=src`