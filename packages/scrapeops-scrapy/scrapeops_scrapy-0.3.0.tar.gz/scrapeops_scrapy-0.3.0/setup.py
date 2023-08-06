from setuptools import setup, find_packages


VERSION = '0.3.0'
DESCRIPTION = 'Scrapeops Scrapy SDK, is a monitoring tool for your Scrapy spiders.'

setup(name='scrapeops_scrapy',
      description="This is an extension for Scrapy spiders to enable scraping monitoring, statistics, alerting, scheduling and data validation.",
      long_description="This an extension for your Scrapy spiders that gives you all the scraping monitoring, statistics, alerting, scheduling and data validation you will need straight out of the box.",
      author="ScrapeOps",
      author_email="info@scrapeops.io",
      version="0.3.0",
      license="BSD",
      url="https://github.com/ScrapeOps/scrapeops-scrapy-sdk",
      packages=find_packages(),
      install_requires=[
          "tld==0.12.4",
          "requests==2.24.0",
          "json5==0.9.5",
          "urllib3==1.25.10",
          ],
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
      ],
      python_requires=">=3.6",
      )
