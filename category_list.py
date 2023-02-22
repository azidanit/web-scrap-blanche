from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import csv
import json

class Scraper:
  def __init__(self):
    self.driver = webdriver.Chrome()
    self.cat_id_global = 99 

  def get_data(self, link):
    self.driver.get(link)
    
    for _ in range(0, 12500, 500):
      time.sleep(0.1)
      self.driver.execute_script("window.scrollBy(0,500)")

    catagories = []
    elements = self.driver.find_elements(by=By.CLASS_NAME, value='css-s7tck8') # card category A,B,C,D
    for element in elements:
      level_1s = element.find_element(by=By.CLASS_NAME, value='css-2wmm3i') # level 1
      level_1s = level_1s.find_elements(by=By.TAG_NAME, value='a') # level 1 A HREF
      for idx, level1 in enumerate(level_1s):
        level_1_name = level1.text
        level_1_href = level1.get_attribute('href')
        level_1_cat_id = self.cat_id_global
        level_data = {"level_1_name" : level_1_name, "level_1_href" : level_1_href, "cat_id": level_1_cat_id, "cat_id_parent": None, "cat_id_grandparent": None, "level_2" : []}
        self.cat_id_global += 1

        level_2_card = element.find_elements(by=By.CLASS_NAME, value='css-16mwuw1')[idx] # level 2 card
        level_2_grid_card = level_2_card.find_element(by=By.CLASS_NAME, value='css-1g1liea') # level 2 grid placeholder
        level_2_grid = level_2_grid_card.find_elements(by=By.CLASS_NAME, value='e13h6i9f2') # level 2 grid
        for level_2 in level_2_grid:
          level_2_name = level_2.find_element(by=By.TAG_NAME, value='a').text
          level_2_href = level_2.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
          level_2_cat_id = self.cat_id_global
          level_2_data = {"level_2_name" : level_2_name, "level_2_href" : level_2_href, "cat_id": level_2_cat_id, "cat_id_parent": level_1_cat_id, "cat_id_grandparent": None, "level_3" : []}
          self.cat_id_global += 1
          
          level_3_card = level_2.find_element(by=By.CLASS_NAME, value='e13h6i9f3') # level 3 card
          level_3_a = level_3_card.find_elements(by=By.TAG_NAME, value='a') # level 3 a
          level_3_cat_id = self.cat_id_global
          if len(level_3_a) <= 0:
            level_2_data['level_3'].append({"level_3_name" : "Lain-Lain", "level_3_href" : level_2_href + "/lain-lain", "cat_id": level_3_cat_id, "cat_id_parent": level_2_cat_id, "cat_id_grandparent": level_1_cat_id})
            self.cat_id_global += 1
          for level_3 in level_3_a:
            level_3_name = level_3.text
            level_3_href = level_3.get_attribute('href')
            level_3_cat_id = self.cat_id_global
            level_3_data = {"level_3_name" : level_3_name, "level_3_href" : level_3_href, "cat_id": level_3_cat_id, "cat_id_parent": level_2_cat_id, "cat_id_grandparent": level_1_cat_id}
            self.cat_id_global += 1
            level_2_data['level_3'].append(level_3_data.copy())
            print(level_3_data)
          level_data['level_2'].append(level_2_data.copy())
        
        catagories.append(level_data.copy())

    return catagories

  def close(self):
    self.driver.close()


scraper = Scraper()
datas = scraper.get_data('https://www.tokopedia.com/p')
scraper.close()

print(datas)
    

# Serializing json
json_object = json.dumps(datas, indent=4)
 
# Writing to sample.json
with open("categories_new_with_id.json", "w") as outfile:
    outfile.write(json_object)

print(json.dumps(
    datas,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
))