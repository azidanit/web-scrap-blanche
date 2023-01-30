import os

sql_res_dir = 'final_kodepos.sql'
directory = 'kodepos_data_sql'
with open(sql_res_dir, mode='w') as sql_file:
  for filename in sorted( filter( lambda x: os.path.isfile(os.path.join(directory, x)),
                          os.listdir(directory) ) ):
      f = os.path.join(directory, filename)
      # checking if it is a file
      if not os.path.isfile(f):
        print("not file", f)
        continue
      
      print("opening", f)

      with open(f, mode='r') as sql_chunk_file:
        sql_file.write(sql_chunk_file.read().upper())
        sql_file.write("\n\n")
