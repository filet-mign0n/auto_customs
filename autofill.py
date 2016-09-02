#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Get chromedriver here:
http://chromedriver.storage.googleapis.com/2.23/chromedriver_mac64.zip
unzip chromedriver_linux32_x.x.x.x.zip

For Remote Server:
http://selenium-release.storage.googleapis.com/3.0-beta2/selenium-server
or check this node module: https://github.com/vvo/selenium-standalone
make sure u got JAVA JRE 8 
Run `java -jar selenium-server-stand*jar`
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import json
import sys

import random

print '\n✈ 🚢  🚚  👮  Auto-Dutiable™ session started 👮  🚚  🚢  ✈\n' 

try:
	driver = webdriver.Chrome()
except Exception as e:
	print '⚠️  error loading Google Chrome driver', e
print '✅  successfully loaded Google Chrome Driver'

with open('config.json') as config:
	config = json.load(config)

supplier_num = config['supplier_num']
username = config['username']
password = config['password']

csvfile = 'tyse.csv'

def closewindows(driver, keep=None):
	if keep: # keep only window of interest open
		for window in driver.window_handles:
			if window != keep:
				driver.switch_to_window(window)
				driver.close()
		driver.switch_to_window(keep)
	else: # close all windows
		driver.quit()

# First check and load csv
try:
	tyse = pd.read_csv(csvfile)
except Exception as e:
	print '⚠️  error loading CSV:', e
	closewindows(driver)
	sys.exit(1)

row_len = len(tyse)-1
tyse = tyse.iterrows() 
print '✅  successfully loaded CSV'

driver.get("http://www.tradelink-ebiz.com/eng/index.html")
assert "Tradelink-eBiz.com" in driver.title
print '✅  successfully accessed "Hong Kong Import and Export Trade and Business" webpage'


for handle in driver.window_handles:
	homepage = handle

elem = driver.find_element_by_css_selector(".t3.t3-e")
print '👉  clicking on "Dutiable Commodities Permits" tab'
elem.click()

timeout = time.time() + 30 
while True:
	if len(driver.window_handles) > 1:
		break
	if time.time() > timeout:
		print '⚠️  timeout or error loading popup page'
		closewindows(driver)
		sys.exit(1)


for handle in driver.window_handles:
	if handle != homepage:
		print '🔁  switching to login window'
		main_window = handle
		driver.switch_to_window(handle)

# Wait at least until the username field loads up
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "username")))
except Exception as e:
    print "⚠️  timeout or error loading popup page:", e
    closewindows(driver)
    sys.exit(1)

print "🔐  inserting username"
elem.send_keys(username)

elem = driver.find_element_by_id("password")
print "🔐  inserting password"
elem.send_keys(password)

print "👉  clicking on \"Login\""
elem = driver.find_element_by_id("login").click()

skip = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > p:nth-child(3) > a:nth-child(4)"
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, skip)))
except Exception as e:
	# selenium.common.exceptions.TimeoutException
    print '⚠️  timeout or error loading skip page:', e
    closewindows(driver)
    sys.exit(1)
print "🔓  successfully logged in"
print "👉  clicking on \"Skip\""
elem.click()

draft = "body > div:nth-child(3) > div > table > tbody > tr:nth-child(1) > td > span > form > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(4) > a > table > tbody > tr > td:nth-child(2)"
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, draft)))
except Exception as e:
    print '⚠️  timeout or error loading Gateway page:', e
    closewindows(driver)
    sys.exit(1)

print '✖  closing surrounding windows"
closewindows(driver, main_window)

print "👉  clicking on \"Draft\" tab"
elem.click()

# note tr:nth-child(1) determins the row
message_id = "#FolderList > tbody > tr:nth-child(1) > td:nth-child(4) > a"
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, message_id)))
except Exception as e:
    print '⚠️  timeout or error loading Gateway page:', e
    closewindows(driver)
    sys.exit(1)

print "👉  clicking on first row of \"Drafts\" table"
elem.click()

# Wait at least until the CommodityCode field loads up
try:
    _CommodityCode = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "_CommodityCode")))
except Exception as e:
    print '⚠️  timeout or error loading Draft page:', e
    closewindows(driver)
    sys.exit(1)

# Fetch all input elems
try:
	_Add = driver.find_element_by_name('btnDutiableAdd')
except Exception as e:
    print '⚠️  timeout or error fetching _Add btn:', e
try:
	_Quantity = driver.find_element_by_name('_Quantity')
except Exception as e:
    print '⚠️  timeout or error fetching _Quantity:', e
try:
	_NoOfCase = driver.find_element_by_name('_NoOfCase')
except Exception as e:
    print '⚠️  timeout or error fetching _NoOfCase:', e
try:
	_SupplierNo = driver.find_element_by_name('_SupplierNo')
except Exception as e:
    print '⚠️  timeout or error fetching _SupplierNo:', e
try:
	_DutiableItemCostEfp = driver.find_element_by_name('_DutiableItemCostEfp')
except Exception as e:
    print '⚠️  timeout or error fetching _DutiableItemCostEfp:', e
try:
	_InvoiceNo = driver.find_element_by_name('_InvoiceNo')
except Exception as e:
    print '⚠️  timeout or error fetching _InvoiceNo:', e
try:
	_DutiableItemCostCurrencySel = Select(driver.find_element_by_name('_DutiableItemCostCurrencySel'))
except Exception as e:
    print '⚠️  timeout or error fetching _DutiableItemCostCurrencySel:', e


def clear_and_fill_input(inpt, value):
	inpt.clear()
	try:
		inpt.send_keys(value)
	except Exception as e:
		print '⚠️  error inputing', value, e

# Click ADD once to be on last line
try:
	_Add.click()
except Exception as e:
	print '⚠️  error trying to click Add:', e

print '\n✨✨✨ Time to automagically fill out the form ✨✨✨'
# Loop through CSV
for i in range(5): #range(row_len): 

	# Get values
	# TODO: add more testing for corrupt or missing cells
	row = next(tyse)[1]
	cc = row['Comm. Code']
	qty = row['Packing']
	if pd.isnull(qty):
		qty = 1
	else:
		qty = int(qty)
	cases = random.randint(1,10)
	price = random.randint(1,370)
	inv = 'SGHK2016AUG01'

	# Fill form
	clear_and_fill_input(_CommodityCode, cc)
	clear_and_fill_input(_Quantity, qty)
	clear_and_fill_input(_NoOfCase, cases)
	clear_and_fill_input(_SupplierNo, supplier_num)
	clear_and_fill_input(_DutiableItemCostEfp, price)
	# select currency
	try:
		_DutiableItemCostCurrencySel.select_by_value('SGD')
	except Exception as e:
		print '⚠️ error trying to seelct currency:', e
	clear_and_fill_input(_InvoiceNo, inv)
	


	print '👉  clicking "ADD with the following filled in form:'
	print '📌  [cc: %s, qty: %s, cases: %s, price: %s, invoice: %s, currency: SGD]' % (cc, qty, cases, price, inv)

	try:
		_Add.click()
	except Exception as e:
		print '⚠️  error trying to click Add:', e

print '\n 🙌  FINISHED 🙌\n'
# js_script = '''
# var A = _PermitApplication_DutiableCommodityInfo__PermitApplication_DutiableCommodityInfo_var;
# var CCs = [];
# A.forEach(function(a) { CCs.push(a[1]); });
# return CCs;
# '''
# try:
# 	A = driver.execute_script(js_script)
# except Exception as e:
# 	print 'error executing js script:', e
# 
# print '\n all Commodity Codes found in online table:'
# print A
# 
# driver.save_screenshot('screenshot.png')
