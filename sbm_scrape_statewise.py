from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import urllib
from urllib.request import Request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#constants 
url = "https://sbm.gov.in/sbmgdashboard/statesdashboard.aspx"

def getTableData(selector : str,filepath : str,soup,index : int):
   # dataframe = pd.DataFrame(columns=headers)
   tabledata = []
   tables = soup.find_all("table")
   table = tables[1]
   data = pd.read_html(str(table))
   for row in data[0].iterrows():
      print(row[1])
      tabledata.append(row[1])
   dataframe = pd.DataFrame(tabledata)
   print(dataframe)
   dataframe.to_csv(filepath)

# Driver Code 
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
driver.get(url)
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

table = soup.select_one("table#tblOrders")
data = pd.read_html(str(table))
i=1
for row in data[0].iterrows():
   state = row[1][0]
   anchor = driver.find_element(By.XPATH,"/html/body/form/div[4]/div/div/div/div[3]/div/div[1]/div/div/div[2]/div/div/div/div/table/tbody/tr["+str(i)+"]/th/a")
   driver.execute_script("arguments[0].click();",anchor)
   time.sleep(10)
   htmlState = driver.page_source
   soupState = BeautifulSoup(htmlState,'lxml')
   print("\n\n\n **************************" + state + "*****************************\n\n\n")
   # expand1 = driver.find_element(By.XPATH,"/html/body/form/div[4]/div/div/div/div[3]/div/div/div/div/div[1]/h3/span[1]")
   # driver.execute_script("arguments[0].click();",expand1)
   # time.sleep(2)

   # District Wise ODF Plus Status 
   getTableData("table#user_table ",state+"_districtwise_ODF_Plus_Status.csv",soupState,1)

   # ODF Plus Model verified Villages
   getTableData("table#tblOrders",state+"_ODF_Plus_Model_Verified_Villages.csv",soupState,2)
   
   driver.back()
   i+=1