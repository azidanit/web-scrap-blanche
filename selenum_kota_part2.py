from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import urllib.parse
import csv

class Scraper:
  def __init__(self):
    self.driver = webdriver.Firefox()

  def get_data(self):
    return self.get_data_kelurahan(self.get_provinsi())

  def get_provinsi(self):
    self.driver.get('https://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&sby=010000')
    datas = []

    elements = self.driver.find_elements(by=By.NAME, value='prov')[0]
    options = elements.find_elements(by=By.TAG_NAME, value='option')
    print(elements)
    for option in options:
      print(option.get_attribute('value'))
      datas.append(option.get_attribute('value'))
    
    return datas

  def get_data_kelurahan(self, provinsi):
    # self.driver.get('https://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&sby=010000')

    # https://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=&urut=&asc=000101&sby=010000&no1=2&prov=Aceh+%28NAD%29
    # https://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=&urut=&asc=000101&sby=010000&no1=2&prov=Aceh+%28NAD%29
    # https://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=Aceh+%28NAD%29&perhal=1000&urut=&asc=000101&sby=010000&no1=1001&no2=2000&kk=3

    # datas = {
    #   'no': [], 
    #   'kodepos': [],
    #   'kelurahan': [],
    #   'kecamatan': [],
    #   'jenis': [],
    #   'kabupaten': [],
    #   'provinsi': 'Aceh (NAD)',
    #   }

    datas_csv = []
    counter_page = 0
    
    # with open('aceh.csv', 'w', encoding='UTF8', newline='') as f:
    #   header = ['no', 'kodepos', 'kelurahan', 'kecamatan', 'jenis', 'kabupaten', 'provinsi']
    #   writer = csv.writer(f)
    #   # write the header
    #   writer.writerow(header)
    params = {
    'jobs': provinsi, 
    'no1':'2', 
    'no2': '', 
    'kk': ''
    }
    while counter_page < 40:
        url = 'https://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&perhal=1000&urut=&asc=000101&sby=010000&'
        q_params = urllib.parse.urlencode(params)
        self.driver.get(url + q_params)
        print(url + q_params)

        tables = self.driver.find_elements(by=By.TAG_NAME, value='table')
    
        rows = tables[12].find_elements(by=By.TAG_NAME, value='tr')

        print(len(rows)-9)

        if (len(rows)-9) <= 0:
          break
        # iterate through the rows
        for i in range(len(rows)-9):
          # extract all td elements from the row
          cells = rows[i+9].find_elements(by=By.TAG_NAME, value='td')
          # iterate through the cells and print their text
          # for cell in cells:
          #     print(cell.text)
          row_csv = []

          # datas['no'].append(cells[0].text)
          # datas['kodepos'].append(cells[1].text)
          # datas['kelurahan'].append(cells[2].text)
          # datas['kecamatan'].append(cells[4].text)
          # datas['jenis'].append(cells[4].text)
          # datas['kabupaten'].append(cells[5].text)

          row_csv.append(int(cells[0].text))
          row_csv.append(cells[1].text.split(' ')[2])
          row_csv.append(cells[2].text)
          row_csv.append(cells[4].text)
          row_csv.append(cells[5].text)
          row_csv.append(cells[6].text)
          row_csv.append(provinsi)

          # writer.writerow(row_csv)
          print(row_csv)
          datas_csv.append(row_csv)
      #   img = element.find_element(by=By.CLASS_NAME, value='css-1c345mg').get_attribute('src')
      #   name = element.find_element(by=By.CLASS_NAME, value='css-1b6t4dn').text
      #   price = element.find_element(by=By.CLASS_NAME, value='css-1ksb19c').text
      #   city = element.find_element(by=By.CLASS_NAME, value='css-1kdc32b').text
        counter_page += 1
        params['kk'] = str(counter_page+1)
        params['no1'] = str(counter_page + (1000 * (counter_page - 1)))
        params['no2'] = str(counter_page * 1000)

      # next_page = self.driver.find_element(by=By.XPATH, value="//button[@class='css-1ix4b60-unf-pagination-item' and text()='" + str(counter_page + 1) + "']")
      # next_page.click()
    
    return datas_csv

  def close(self):
    self.driver.close()

scraper = Scraper()
provinsi = scraper.get_provinsi()
print(provinsi[16:])

for prov in provinsi[16:]:
  datas = scraper.get_data_kelurahan(prov)

  header = ['no', 'kodepos', 'kelurahan', 'kecamatan', 'jenis', 'kabupaten', 'provinsi']

  with open(prov + 'final.csv', 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)

      # write the header
      writer.writerow(header)

      # write multiple rows
      writer.writerows(datas)

scraper.close()

# # print(datas)
# print("GOT " + str(len(datas)) + " DATA")
# print("GOT " + str(len(datas['no'][-1])) + " DATA")
# print(datas['no'])


# params = {
#   'jobs': 'ACEH (NAD)', 
#   'no1':'1001', 
#   'no2': '2000', 
#   'kk': '3'}

# params['no1'] = "asddasd"
# print(params['no1'])
# urllib.parse.urlencode(params)

# print(urllib.parse.urlencode(params))