from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import csv
import json
import threading

class Scraper:
  def __init__(self):
    self.driver = webdriver.Chrome()
    # self.driver.set_window_position(1024, 0, windowHandle='current')

    # self.driver.minimize_window()

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
    while counter_page < 2:
      time.sleep(2)
      self.driver.execute_script("window.scrollBy(0,-4000)")
      time.sleep(0.1)
      self.driver.execute_script("window.scrollBy(0,-500)")
      for _ in range(0, 4000, 500):
        time.sleep(0.1)
        self.driver.execute_script("window.scrollBy(0,500)")

      
      elements = self.driver.find_elements(by=By.CLASS_NAME, value='e1nlzfl2')
      for element in elements:
        link_product = element.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        print("link product", link_product)
        if 'ta.tokopedia.com' in link_product:
          continue

        product_links.append(link_product)

        # if len(product_links) >= 1:
        #   break

      counter_page += 1
      print(counter_page)
      # next_page = self.driver.find_element(by=By.XPATH, value="//button[@class='css-1eamy6l-unf-pagination-item']")
      next_page = self.driver.find_element(by=By.XPATH, value="//button[@aria-label='Laman berikutnya']")
      next_page.click()
    
    return product_links

  def close(self):
    self.driver.close()


def dict_to_jsonfile(data, filename):
    # Serializing json
  json_object = json.dumps(data, indent = 4)

  with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=4)

def scrap_cat(from_idx, to_idx):
  # Opening JSON file
  f = open('categories_new.json')
    
  # returns JSON object as 
  # a dictionary
  data_json = json.load(f)
  counter_file = from_idx

  cat_id_global = 99
  is_skipping_level_1 = True
  iter_level_1 = 0
  for data_row_json in data_json[from_idx:to_idx]:
    if iter_level_1 < 3:
      iter_level_1 += 1
    else:
      is_skipping_level_1 = False
    new_data_json = []

    cat_id_global += 1
    level_data = {"level_1_name" : data_row_json["level_1_name"], "level_1_href" : data_row_json["level_1_href"], "cat_id": cat_id_global, "level_2" : []}
    for data_2 in data_row_json["level_2"]:
      cat_id_global += 1
      level_2_data = {"level_2_name" : data_2["level_2_name"], "level_2_href" : data_2["level_2_href"], "cat_id": cat_id_global,"level_3" : []}

      for data_3 in data_2["level_3"]:
        cat_id_global += 1

        level_3_name = data_3["level_3_name"]
        level_3_href = data_3["level_3_href"]
        level_3_data = {"level_3_name" : level_3_name, "level_3_href" : level_3_href,
        "cat_id": cat_id_global,
        "products": None}

        if is_skipping_level_1:
          continue

        datas = []
        try:
          scraper = Scraper()
          print("OPENING PRODUCT LIST=====", level_3_href)
          datas = scraper.get_data(level_3_href)
          scraper.close()
        except Exception as e:
          print(e)
          continue

        print("DONE GET PRODUCT LIST===== GOT ", len(datas), "PRODUCTS")

        json_temp_prods_level3 = {}
        data_products = []

        # for data in datas:
        #   scraper2 = Scraper()
        #   try:
        #     print("OPENING PRODUCT DETAIL=====", data)
        #     data_products.append(scraper2.get_product_detail(data))
        #   except Exception as e:
        #     print(e)
        #     scraper2.close()
        #     continue

        level_3_data["products"] = data_products.copy()
        
        json_temp_prods_level3 = level_3_data.copy()
        json_temp_prods_level3["cat_id"] = cat_id_global
        dict_to_jsonfile(json_temp_prods_level3, "product_category_populate_chunk_n" + str(cat_id_global) + ".json")

        level_2_data["level_3"].append(level_3_data.copy())
        print(level_3_data)

        level_data["level_2"].append(level_2_data.copy())

        new_data_json.append(level_data.copy())
        
    if is_skipping_level_1:
      continue

    # Serializing json
    json_object = json.dumps(new_data_json[-1], indent=4)

    # Writing to sample.json
    with open("product_category_populate_n" + str(counter_file) + ".json", "w") as outfile:
      counter_file += 1
      outfile.write(json_object)

thread_list = []
# for i in range(3):
#   thread = threading.Thread(target=scrap_cat, args=(i*1, (i+1)*1))
#   thread_list.append(thread)
#   thread.start()
#
# for i in range(2):
#   thread_list[i].join()

  # thread = threading.Thread(target=scrap_cat, args=(i*1, (i+1)*1))
  # thread_list.append(thread)
  # thread.start()

scrap_cat(1, 2)