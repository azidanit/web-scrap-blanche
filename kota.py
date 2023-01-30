import requests
from bs4 import BeautifulSoup

# Make a GET request to the website
url = 'https://kodepos.nomor.net/_kodepos.php?_i=desa-kodepos&daerah=Provinsi&jobs=&urut=&asc=000101&sby=000000&no1=2&prov=Aceh+%28NAD%29'
response = requests.get(url)

print(response.text)

# Parse the HTML content
# soup = BeautifulSoup(response.text, 'html.parser')

# prov_select = soup.find_all('select')
# print(prov_select)
# options = prov_select.find_all('option')

# for option in options:
#     value = option['value']
#     text = option.text
#     print(f'{text} : {value}')

# Extract data from the drop-down list
# dropdown_list = soup.select('select[name="prov"]')[0]
# options = dropdown_list.find_all('option')
# dropdown_data = []
# for option in options:
#     dropdown_data.append({'text': option.text, 'value': option['value']})

# # Extract data from the table
# table = soup.select('table')[11]
# # print(table[11])
# rows = table.find_all('tr')
# table_data = []
# for row in rows:
#     cells = row.find_all('td')
#     table_data.append([cell.text for cell in cells])

# # Print the data
# print('Dropdown data:')
# print(dropdown_data)
# print('\n')
# print('Table data:')
# print(table_data)
