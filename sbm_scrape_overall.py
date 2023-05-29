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
odfplusstatusfile = "odfplusstatus.csv"
odfplusstatusfields = ["State/UT","Total Villages","Total ODF Plus Villages 1","Total ODF PLus Villages 2","ODF Plus Aspiring Villages 1","ODF Plus Aspiring Villages 2","ODF Plus Rising Villages 1","ODF Plus Rising Villages 2","ODF Plus Model Villages 1","ODF Plus Model Villages 2"]
odfplusmodelverifiedvillagesfile = "odfplusmodelverifiedvillages.csv"
url = "https://sbm.gov.in/sbmgdashboard/statesdashboard.aspx"

def getTableData(selector : str,filepath : str,soup,index : int):
   # dataframe = pd.DataFrame(columns=headers)
   tabledata = []
   tables = soup.find_all("table")
   table = tables[index]
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

getTableData("table#tblOrders",odfplusstatusfile,soup,0)

getTableData("table#tblOrders",odfplusmodelverifiedvillagesfile,soup,0)
   