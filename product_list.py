from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import csv
import json

class Scraper:
  def __init__(self):
    self.driver = webdriver.Chrome()

  def get_product_detail(self, link):
    self.driver.get(link)
    # for _ in range(0, 500, 500):
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

    return {
      "imgs": imgs_src,
      "name": name,
      "price": price,
      "detail": details,
      "desc": desc,
      "variants": variants,
    }


  def get_data(self, link):
    self.driver.get(link)
    
    counter_page = 0
    datas = []
    product_links = []
    while counter_page < 15:
      for _ in range(0, 4500, 500):
        time.sleep(0.1)
        self.driver.execute_script("window.scrollBy(0,500)")

      
      elements = self.driver.find_elements(by=By.CLASS_NAME, value='css-gfx8z3')
      for element in elements:
        link_product = element.find_element(by=By.TAG_NAME, value='a').get_attribute('href')

        if 'ta.tokopedia.com' in link_product:
          continue
        print("link_product", link_product)
        product_links.append(link_product)

      counter_page += 1
      print(counter_page)
      # next_page = self.driver.find_element(by=By.XPATH, value="//button[@class='css-1eamy6l-unf-pagination-item']")
      next_page = self.driver.find_element(by=By.XPATH, value="//button[@aria-label='Laman berikutnya']")
      next_page.click()
    
    return product_links

  def close(self):
    self.driver.close()


scraper = Scraper()
datas = scraper.get_data('https://www.tokopedia.com/p/audio-kamera-elektronik-lainnya/aksesoris-kamera/kabel-konektor-kamera')
scraper.close()

print(datas)

data_products = []
for data in datas:
  scraper2 = Scraper()
  try:
    data_products.append(scraper2.get_product_detail(data))
  except Exception as e:
    print(e)
  finally:
    scraper2.close()
    

print(data_products)
# Serializing json
json_object = json.dumps(data_products, indent=4)
 
# Writing to sample.json
with open("product_hp.json", "w") as outfile:
    outfile.write(json_object)