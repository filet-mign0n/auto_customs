'''
get selenim server from:
http://selenium-release.storage.googleapis.com/3.0-beta2/selenium-server -standalone-3.0.0-beta2.jar

get chromedriver from:
http://chromedriver.storage.googleapis.com/2.23/chromedriver_mac64.zip
unzip chromedriver_linux32_x.x.x.x.zip

check this npm later https://github.com/vvo/selenium-standalone

make sure u got JAVA JRE 8

Run 
`java -jar selenium-server-stand*jar -port 1029`
before launching

'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import sys

import random

supplier_num = 28608
csvfile = 'tyse.csv'

# First check and load csv
try:
	tyse = pd.read_csv(csvfile)
except Exception as e:
	print e
	closewindows(driver, driver.window_handles)
	sys.exit(1)

tyse = tyse.iterrows() 

driver = webdriver.Chrome()
driver.get("http://www.tradelink-ebiz.com/eng/index.html")
assert "Tradelink-eBiz.com" in driver.title
print '############## AutoDutiableAdd session started ##############' 
print 'accessing webpage:', driver.title

def closewindows(driver, windows):
	for window in windows:
		driver.switch_to_window(window)
		driver.close()

for handle in driver.window_handles:
	homepage = handle

elem = driver.find_element_by_css_selector(".t3.t3-e")
print 'clicking on Dutiable Commodities Permits tab'
elem.click()

timeout = time.time() + 30 
while True:
	if len(driver.window_handles) > 1:
		break
	if time.time() > timeout:
		print 'timeout or error loading popup page'
		closewindows(driver, driver.window_handles)
		sys.exit(1)


for handle in driver.window_handles:
	if handle != homepage:
		driver.switch_to_window(handle)

# Wait at least until the username field loads up
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "username")))
except Exception as e:
    print "timeout or error loading popup page:", e
    closewindows(driver, driver.window_handles)
    sys.exit(1)

print "inserting username"
elem.send_keys("mjp98280")

elem = driver.find_element_by_id("password")
print "inserting password"
elem.send_keys("France1980")

print "clicking on \"Login\""
elem = driver.find_element_by_id("login").click()

skip = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > p:nth-child(3) > a:nth-child(4)"
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, skip)))
except Exception as e:
	# selenium.common.exceptions.TimeoutException
    print 'timeout or error loading skip page:', e
    closewindows(driver, driver.window_handles)
    sys.exit(1)

print "clicking on \"Skip\""
elem.click()

draft = "body > div:nth-child(3) > div > table > tbody > tr:nth-child(1) > td > span > form > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(4) > a > table > tbody > tr > td:nth-child(2)"
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, draft)))
except Exception as e:
    print 'timeout or error loading Gateway page:', e
    closewindows(driver, driver.window_handles)
    sys.exit(1)

print "clicking on \"Draft\" tab"
elem.click()

# note tr:nth-child(1) determins the row
message_id = "#FolderList > tbody > tr:nth-child(1) > td:nth-child(4) > a"
try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, message_id)))
except Exception as e:
    print 'timeout or error loading Gateway page:', e
    closewindows(driver, driver.window_handles)
    sys.exit(1)

print "clicking on first row of \"Drafts\" table"
elem.click()




# Wait at least until the CommodityCode field loads up
try:
    _CommodityCode = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "_CommodityCode")))
except Exception as e:
    print 'timeout or error loading Draft page:', e
    closewindows(driver, driver.window_handles)
    sys.exit(1)

def fecth_input_elem(name):
	try:
		_Add = driver.find_element_by_name(name)
	except Exception as e:
	    print 'error fetching elem:', name, e


# Fetch all input elems
try:
	_Add = driver.find_element_by_name('btnDutiableAdd')
except Exception as e:
    print 'timeout or error fetching _Add btn:', e
try:
	_Quantity = driver.find_element_by_name('_Quantity')
except Exception as e:
    print 'timeout or error fetching _Quantity:', e
try:
	_NoOfCase = driver.find_element_by_name('_NoOfCase')
except Exception as e:
    print 'timeout or error lfetching _NoOfCase:', e
try:
	_SupplierNo = driver.find_element_by_name('_SupplierNo')
except Exception as e:
    print 'timeout or error fetching _SupplierNo:', e
try:
	_DutiableItemCostEfp = driver.find_element_by_name('_DutiableItemCostEfp')
except Exception as e:
    print 'timeout or error fetching _DutiableItemCostEfp:', e
try:
	_DutiableItemCostCurrencySel = Select(driver.find_element_by_name('_DutiableItemCostCurrencySel'))
except Exception as e:
    print 'timeout or error fetching _DutiableItemCostCurrencySel:', e
try:
	_InvoiceNo = driver.find_element_by_name('_InvoiceNo')
except Exception as e:
    print 'timeout or error fetching _InvoiceNo:', e


def clear_and_fill_input(inpt, value):
	inpt.clear()
	try:
		inpt.send_keys(value)
	except Exception as e:
		print 'error inputing', value, e

# Loop through CSV
for i in range(5):

	# Get values
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
	clear_and_fill_input(_InvoiceNo, inv)

	print 'about to click ADD with cc: %s, qty: %s, supplier_num: %s' % (cc, qty, supplier_num)
	try:
		_Add.click()
	except Exception as e:
		print 'error trying to click Add:', e




js_script = '''
var A = _PermitApplication_DutiableCommodityInfo__PermitApplication_DutiableCommodityInfo_var;
var CCs = []
A.forEach(function(a) { 
	CCs.push(a[1]);
  }); //logs all Commodity Codes
return CCs;
'''
try:
	A = driver.execute_script(js_script)
except Exception as e:
	print 'error executing js script:', e

print '\n all Commodity Codes found in online table:'
print A


'''
select = Select(driver.find_element_by_name('name'))
select.select_by_index(index)
select.select_by_visible_text("text")
select.select_by_value(value)

driver.execute_script('alert("payday");') !!!!
driver.save_screenshot('screenshot.png') !!!!
'''