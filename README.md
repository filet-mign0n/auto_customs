Auto-Customs
========

Hong Kong's customs decleration website does not allow bulk upload of list of items to declare. The process in which to declare them one by one is painfully manual. This app automates it.

<img src="https://raw.githubusercontent.com/filet-mign0n/filet-mignon.github.io/master/images/auto_customs0.png">

### How it works

The Python app will take a csv file as input, map the column names to form inputs, and enter them on the website with the Selenium API. 

### Install

```sh
$ git clone https://github.com/filet-mign0n/auto_customs && cd auto_customs && sudo pip install requirements.txt
```
### Configure

Username, password, etc. should be documented in config.json before launching app. 

### Launch

```sh
$ python autofill.py --csv /path/to/csv --config /path/to/config #optional
```
### Requirements

* Python 2.7
* ChromeDriver executable http://chromedriver.storage.googleapis.com/index.html
 
