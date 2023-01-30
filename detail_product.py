from selenium.webdriver.common.by import By
from selenium import webdriver
import time

class Scraper:
  def __init__(self):
    self.driver = webdriver.Firefox()

  def get_data(self):
    self.driver.get('https://www.tokopedia.com/apasaja16/axioo-slimbook-14-r-series-ryzen-3-3200u-8gb-256ssd-w10pro-14-fhd?extParam=ivf%3Dfalse&src=topads')
    
    counter_page = 0
    datas = []

    for _ in range(0, 2500, 500):
      time.sleep(0.1)
      self.driver.execute_script("window.scrollBy(0,500)")

    imgs = self.driver.find_elements(by=By.CLASS_NAME, value='css-1c345mg')
    imgs_src = []
    for img in imgs:
      imgs_src.append(img.get_attribute('src'))

    detail_upper = self.driver.find_elements(by=By.CLASS_NAME, value='css-1dmo88g')
    details = []
    for i in range (2):
      details.append(detail_upper[i].find_elements(by=By.TAG_NAME, value='span')[-1].text)
    for i in range(2, 4):
      details.append(detail_upper[i].find_elements(by=By.TAG_NAME, value='b')[-1].text)

    name = self.driver.find_element(by=By.CLASS_NAME, value='css-1320e6c').text
    price = self.driver.find_element(by=By.CLASS_NAME, value='price').text
    desc = self.driver.find_element(by=By.CLASS_NAME, value='eytdjj01')
    desc = desc.find_element(by=By.TAG_NAME, value='div').text

    datas.append({
      'imgs': imgs_src,
      'name': name,
      'price': price,
      'detail': details,
      'desc': desc,
    })

    
    return datas

  def close(self):
    self.driver.close()


scraper = Scraper()
datas = scraper.get_data()
print(datas)
scraper.close()