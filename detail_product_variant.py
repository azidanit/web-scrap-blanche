from selenium.webdriver.common.by import By
from selenium import webdriver
import time

class Scraper:
  def __init__(self):
    self.driver = webdriver.Chrome()

  def get_data(self):
    # self.driver.get('https://www.tokopedia.com/studioponsel/macbook-air-2022-m2-chip-13-inch-512gb-256gb-ram-8gb-apple-ibox-inter-256gb-midnight?extParam=ivf%3Dfalse%26src%3Dsearch')
    # self.driver.get('https://www.tokopedia.com/distrilapid/laptop-xiaomi-redmibook-15-intel-i3-1115g4-ram-8gb-ssd-256gb-w10-bundle-mouse?extParam=ivf%3Dfalse%26src%3Dsearch')
    self.driver.get('https://www.tokopedia.com/yanguangkomputer/laptop-second-fujitsu-core-i5-gen-2-i5-gen-3-lifebook-p771-d-ram-4gb-core-i3-gen-3?extParam=ivf%3Dfalse%26src%3Dsearch')
    # self.driver.get('https://www.tokopedia.com/hp/laptop-hp-14s-dq0510tu-celeron-4-gb-ssd-256gb-w11-ohs-gratis-tas?extParam=ivf%3Dfalse%26whid%3D5931369&src=topads')
    
    datas = []

    # for _ in range(0, 2500, 500):
    #   time.sleep(0.1)
    #   self.driver.execute_script("window.scrollBy(0,500)")

    driver = self.driver

    variants = None
  
    variant_elems = driver.find_elements(by=By.CLASS_NAME, value='css-1b2d3hk')
    if len(variant_elems) == 2:
      group_name1 = variant_elems[1].find_element(by=By.CLASS_NAME, value='e1qvo2ff8').text
      variant_data = {"group_name1": group_name1, "group_name2": None, "options": []}

      variant_option_elems = variant_elems[1].find_elements(by=By.CLASS_NAME, value='css-1y1bj62')
      for variant_option in variant_option_elems:
        option = {"option_name1": variant_option.text, "option_name2": "", "price": "rp.21323"}
        option["option_name2"] = None
        
        variant_option_btn = variant_option.find_element(by=By.TAG_NAME, value='button')
        variant_option_btn.click()     

        price_item = driver.find_element(by=By.CLASS_NAME, value='price').text
        option["price"] = price_item
        variant_data["options"].append(option.copy())

      variants= variant_data.copy()

    if len(variant_elems) == 3:
      group_name1 = variant_elems[1].find_element(by=By.CLASS_NAME, value='e1qvo2ff8').text
      group_name2 = variant_elems[2].find_element(by=By.CLASS_NAME, value='e1qvo2ff8').text
      variant_data = {"group_name1": group_name1, "group_name2": group_name2, "options": []}

      variant_option_elems = variant_elems[1].find_elements(by=By.CLASS_NAME, value='css-1y1bj62')
      for variant_option in variant_option_elems:
        option = {"option_name1": variant_option.text, "option_name2": "", "price": "rp.21323"}
        
        variant_option_btn = variant_option.find_element(by=By.TAG_NAME, value='button')
        variant_option_btn.click()

        variant_option2_elems = variant_elems[2].find_elements(by=By.CLASS_NAME, value='css-1y1bj62')
        for variant_option_2 in variant_option2_elems:
          option["option_name2"] = variant_option_2.text

          variant_option2_btn = variant_option_2.find_element(by=By.TAG_NAME, value='button')
          variant_option2_btn.click()

          price_item = driver.find_element(by=By.CLASS_NAME, value='price').text
          option["price"] = price_item
          variant_data["options"].append(option.copy())

      variants= variant_data.copy()

    imgs = driver.find_elements(by=By.CLASS_NAME, value='css-1c345mg')
    imgs_src = []
    for img in imgs:
      if img.get_attribute('src') == "https://assets.tokopedia.net/assets-tokopedia-lite/v2/zeus/kratos/85cc883d.svg":
        continue
      imgs_src.append(img.get_attribute('src'))

    detail_upper = driver.find_elements(by=By.CLASS_NAME, value='css-1dmo88g')
    details = []
    try:
      for i in range (2):
        details.append(detail_upper[i].find_elements(by=By.TAG_NAME, value='span')[-1].text)
      for i in range(2, 4):
        details.append(detail_upper[i].find_elements(by=By.TAG_NAME, value='b')[-1].text)
        details.append(detail_upper[i].find_element(by=By.TAG_NAME, value='a').get_attribute('href'))
        print(detail_upper[i].find_element(by=By.TAG_NAME, value='a').text)
    except:
      pass

    name = driver.find_element(by=By.CLASS_NAME, value='css-1320e6c').text
    price = driver.find_element(by=By.CLASS_NAME, value='price').text
    desc = driver.find_element(by=By.CLASS_NAME, value='eytdjj01')
    desc = desc.find_element(by=By.TAG_NAME, value='div').text

    driver.back()

    return {
      "imgs": imgs_src,
      "name": name,
      "price": price,
      "detail": details,
      "desc": desc,
      "variants": variants,
    }

  def close(self):
    self.driver.close()


scraper = Scraper()
datas = scraper.get_data()
scraper.close()

import json
print(json.dumps(
    datas,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
))