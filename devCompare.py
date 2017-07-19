import requests
import difflib
import json
import csv
from subprocess import call
import subprocess
from pprint import pprint

def compare():

	with open('sys_upgrade_history_log.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter='\n')
		for row in spamreader:
			#print ', '.join(row)
			row = str(row[0])
			sys_id = row[-32:]
			print sys_id
			table = row.split(sys_id,1)[0]
			table = table[:-1]

			if "_" not in sys_id:
				resp1 = requests.get('https://dev36141.service-now.com/api/now/table/' + table + '/' + sys_id, auth=('admin','*******'))
				resp2 = requests.get('https://dev31798.service-now.com/api/now/table/' + table + '/' + sys_id, auth=('admin','*******'))
				resp3 = requests.get('https://********.service-now.com/api/now/table/' + table + '/' + sys_id, auth=('****','*******'))

				out1 = str(json.dumps(resp1.json(), sort_keys=True, indent=4, separators=(',', ': '))).replace('\\n','\n').replace('\\t',' ').replace('\\r','')
				out2 = str(json.dumps(resp2.json(), sort_keys=True, indent=4, separators=(',', ': '))).replace('\\n','\n').replace('\\t',' ').replace('\\r','')
				out3 = str(json.dumps(resp3.json(), sort_keys=True, indent=4, separators=(',', ': '))).replace('\\n','\n').replace('\\t',' ').replace('\\r','')

				file1 = open("out/hel_" + row + ".txt","w")
				file2 = open("out/jak_" + row + ".txt","w")
				file3 = open("out/test_" + row + ".txt","w")
				
				file1.write(out1)
				file2.write(out2)
				file3.write(out3)

				file1.close()
				file2.close()
				file3.close()

				f1 = open("out/diff_hel_jak" + row + ".txt", "w")
				f2 = open("out/diff_hel_test" + row + ".txt", "w")

				call(["diff", "out/hel_" + row + ".txt", "out/jak_" + row + ".txt"], stdout=f1)
				call(["diff", "out/hel_" + row + ".txt",  "out/test_" + row + ".txt"], stdout=f2)

				f1.close()
				f2.close()



compare()
