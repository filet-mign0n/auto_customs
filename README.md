Autofill Customs
========

Hong Kong customs decleration website does not allow upload of list of items to declare. The process in which to declare them one by one is painfully manual. This app automates it.

###How it works

The Python app will take a csv file as input, map the column names to form inputs, and enter them on the website with the Selenium API. 

###Install

```sh
$ git clone https://github.com/filet-mign0n/autofill_customs && cd autofill_customs && pip install requirements.txt
```
###Configure

Username, password, etc. should be documented in config.json before launching app. 

###Launch

```sh
$ python autofill.py --csv /path/to/csv --config /path/to/config #optional
```

###Requirements

* Python 2.7
* ChromeDriver executable http://chromedriver.storage.googleapis.com/index.html
 
