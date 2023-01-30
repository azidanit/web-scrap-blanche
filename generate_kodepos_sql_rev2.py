import csv
import os
# assign directory
directory = 'kodepos_data_raw_fix'
sql_res_dir = 'kodepos_data_sql'
# iterate over files in
# that directory
province_id = 0
city_id = 0
district_id = 0
subdistrict_id = 0

list_kabupaten = []
list_city_id = []
list_kecamatan = []
list_district_id = []

for filename in sorted( filter( lambda x: os.path.isfile(os.path.join(directory, x)),
                        os.listdir(directory) ) ):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if not os.path.isfile(f):
      print("not file", f)
      continue
    
    print("opening", f)
    fsql = os.path.join(sql_res_dir, filename.replace('.csv', '.sql'))
    with open(fsql, mode='w') as sql_file:
      with open(f, mode='r') as csv_file:
          csv_reader = csv.DictReader(csv_file)
          line_count = 0
          for row in csv_reader:
              if line_count == 0:
                  print(f'Column names are {", ".join(row)}')
                  line_count += 1
                  continue
              if line_count == 1:
                  province_id += 1
                  sql_file.write("INSERT INTO provinces(id, name) VALUES({}, '{}');\n".format(province_id, row["provinsi"]))


              print(f'\t{row["no"]} {row["kodepos"]} {row["kelurahan"]} {row["kecamatan"]} {row["kabupaten"]}')
              
              kab_temp = [row['jenis'], row['kabupaten'], row["provinsi"]]
              if not kab_temp in list_kabupaten:
                  city_id += 1
                  list_city_id.append(city_id)
                  list_kabupaten.append(kab_temp)
                  if "'" in row["kabupaten"]:
                    row["kabupaten"] = row["kabupaten"].replace("'", "''")
                  sql_file.write("INSERT INTO cities(id, province_id ,name) VALUES({}, {}, '{}');\n".format(city_id, province_id, row["jenis"] + " " + row["kabupaten"]))
                  print(f'Kota {kab_temp} {province_id}')
              
              kec_temp = [row["kecamatan"], row['jenis'], row['kabupaten'], row["provinsi"]]
              if not kec_temp in list_kecamatan:
                district_id += 1
                list_district_id.append(district_id)
                list_kecamatan.append(kec_temp)
                if "'" in row["kecamatan"]:
                  row["kecamatan"] = row["kecamatan"].replace("'", "''")

                city_to_insert = list_city_id[list_kabupaten.index(kab_temp)]
                sql_file.write("INSERT INTO districts(id, city_id, name) VALUES({}, {}, '{}');\n".format(district_id, city_to_insert, row["kecamatan"]))
              
              subdistrict_id += 1
              if "'" in row["kelurahan"]:
                  row["kelurahan"] = row["kelurahan"].replace("'", "''")
              district_to_insert = list_district_id[list_kecamatan.index(kec_temp)]
              sql_file.write("INSERT INTO subdistricts(id, district_id, name, zip_code) VALUES({}, {}, '{}', '{}');\n".format(subdistrict_id, district_to_insert, row["kelurahan"], row["kodepos"]))
              line_count += 1
          print(f'Processed {line_count} lines.')

    # break

    
