import mysql.connector
import threading
import json
import datetime

class PackageValue:

	def package_decoder(self, dict_param):
		# Declare a container list
		arr = []
		# Loop through the dictionary parameter
		for i in range(len(dict_param)):
			# Split every 'package' element into n array of strings
			split = dict_param[i]['packages'].split(',')

			if len(split) < 17:
				obj = {}
				obj['mac'] = dict_param[i]['mac']
				obj['wallet'] = int(dict_param[i]['wallet'])
				obj['xxxMinutes'] = -1
				obj['iHour'] = -1
				obj['iiHours'] = -1
				obj['iiiHours'] = -1
				obj['vHours'] = -1
				obj['iDay'] = -1
				obj['iiDays'] = -1
				obj['ivDays'] = -1
				obj['iWeek'] = -1

				obj['iiiDays'] = -1
				obj['viiDays'] = -1
				obj['xvDays'] = -1
				obj['xxxDays'] = -1

				obj['dateCreated'] = dict_param[i]['dateCreated']
				
				arr.append(obj)

			elif len(split) == 17:	
				split[19:] = ['iiiHours', 0, 'iiiDays', 0, 'viiDays', 0, 'xvDays', 0, 'xxxDays', 0]

				# sample: ,30Minutes,4,1Hour,20,2Hours,1,5Hours,2,1Day,1,2Days,0,3days,0,1Week,1
				obj = {}
				obj['mac'] = dict_param[i]['mac']
				obj['wallet'] = int(dict_param[i]['wallet'])
				obj['xxxMinutes'] = int(split[2])
				obj['iHour'] = int(split[4])
				obj['iiHours'] = int(split[6])
				obj['vHours'] = int(split[8])
				obj['iDay'] = int(split[10])
				obj['iiDays'] = int(split[12])

				if split[13] == '3days':	
					obj['iiiDays'] = int(split[14])
					obj['ivDays'] = 0
				else:
					obj['iiiDays'] = 0	
					obj['ivDays'] = int(split[14])

				obj['iWeek'] = int(split[16])

				obj['iiiHours'] = int(split[18])
				obj['viiDays'] = int(split[22])
				obj['xvDays'] = int(split[24])
				obj['xxxDays'] = int(split[26])

				obj['dateCreated'] = dict_param[i]['dateCreated']
				
				arr.append(obj)

			elif len(split) == 19:
				split[19:] = ['iiiDays', 0, 'viiDays', 0, 'xvDays', 0, 'xxxDays', 0]

				# sample: ,30Minutes,5,1Hour,157,2Hours,106,3Hours,35,5Hours,48,1Day,3,2Days,2,4days,1,1Week,1
				obj = {}
				obj['mac'] = dict_param[i]['mac']
				obj['wallet'] = int(dict_param[i]['wallet'])
				obj['xxxMinutes'] = int(split[2])
				obj['iHour'] = int(split[4])
				obj['iiHours'] = int(split[6])
				obj['iiiHours'] = int(split[8])
				obj['vHours'] = int(split[10])
				obj['iDay'] = int(split[12])
				obj['iiDays'] = int(split[14])
				obj['ivDays'] = int(split[16])
				obj['iWeek'] = int(split[18])

				obj['iiiDays'] = int(split[20])
				obj['viiDays'] = int(split[22])
				obj['xvDays'] = int(split[24])
				obj['xxxDays'] = int(split[26])

				obj['dateCreated'] = dict_param[i]['dateCreated']
				
				arr.append(obj)


			elif len(split) == 27:
				# sample: ,30Minutes, 0, 1Hour, 1, 2Hours, 0, 5Hours, 0, 1Day, 1, 2Days, 0, 3days, 0, 1Week, 0, 3Hours, 0, 3Days, 0, 7Days, 0, 15Days, 1, 30Days, 0
				obj = {}
				obj['mac'] = dict_param[i]['mac']
				obj['wallet'] = int(dict_param[i]['wallet'])
				obj['xxxMinutes'] = int(split[2])
				obj['iHour'] = int(split[4])
				obj['iiHours'] = int(split[6])
				obj['vHours'] = int(split[8])
				obj['iDay'] = int(split[10])
				obj['iiDays'] = int(split[12])
				obj['ivDays'] = 0 # There is no 4Days to any split which length is 27
				obj['iWeek'] = int(split[16])

				obj['iiiHours'] = int(split[18])
				obj['iiiDays'] = int(split[20])
				obj['viiDays'] = int(split[22])
				obj['xvDays'] = int(split[24])
				obj['xxxDays'] = int(split[26])
				
				obj['dateCreated'] = dict_param[i]['dateCreated']
				
				arr.append(obj)
				


			

		# print(arr)

		return arr


	def compute_packages(self, dict_param):

		def subtractor(param1, param2):
			if param1 == -1:
				return param2 - param2
			elif param2 == -1:
				return param1 - param1
			else:
				return param1 - param2

		# Declare  container list
		arr = []
		# Specify the length of dictionary
		length = len(dict_param)

		# Loop through it
		for i in range(length):
			# The value of z is decreasing as per loop
			z = length - i - 2
			# If the value of z is less than 0 initialize it to z = 0
			if z < 0:	z = 0

			xxxMinutes = subtractor(dict_param[length-i-1]['xxxMinutes'], dict_param[z]['xxxMinutes'])
			iHour = subtractor(dict_param[length-i-1]['iHour'], dict_param[z]['iHour'])
			iiHours = subtractor(dict_param[length-i-1]['iiHours'], dict_param[z]['iiHours'])
			iiiHours = subtractor(dict_param[length-i-1]['iiiHours'], dict_param[z]['iiiHours'])
			vHours = subtractor(dict_param[length-i-1]['vHours'], dict_param[z]['vHours'])
			iDay = subtractor(dict_param[length-i-1]['iDay'], dict_param[z]['iDay'])
			iiDays = subtractor(dict_param[length-i-1]['iiDays'], dict_param[z]['iiDays'])
			ivDays = subtractor(dict_param[length-i-1]['ivDays'], dict_param[z]['ivDays'])
			iWeek = subtractor(dict_param[length-i-1]['iWeek'], dict_param[z]['iWeek'])

			iiiDays = subtractor(dict_param[length-i-1]['iiiDays'], dict_param[z]['iiiDays'])
			viiDays = subtractor(dict_param[length-i-1]['viiDays'], dict_param[z]['viiDays'])
			xvDays = subtractor(dict_param[length-i-1]['xvDays'], dict_param[z]['xvDays'])
			xxxDays = subtractor(dict_param[length-i-1]['xxxDays'], dict_param[z]['xxxDays'])

			wallet = dict_param[length-i-1]['wallet']

			if xxxMinutes < 0:	xxxMinutes = 0
			if iHour < 0:	iHour = 0
			if iiHours < 0:	iiHours = 0
			if iiiHours < 0:	iiiHours = 0
			if vHours < 0:	vHours = 0
			if iDay < 0:	iDay = 0
			if iiDays < 0:	iiDays = 0
			if ivDays < 0:	ivDays = 0
			if iWeek < 0:	iWeek = 0

			if iiiDays < 0: iiiDays = 0
			if viiDays < 0: viiDays = 0
			if xvDays < 0: xvDays = 0
			if xxxDays < 0: xxxDays = 0

			if wallet < 0:	wallet = 0


			# Declare new dictionary and input every subtraction results, mac, and dateCreated attribute into it.
			obj = {}
			obj['mac'] = dict_param[i]['mac']
			obj['wallet'] = wallet
			obj['xxxMinutes'] = xxxMinutes
			obj['iHour'] = iHour
			obj['iiHours'] = iiHours
			obj['iiiHours'] = iiiHours
			obj['vHours'] = vHours
			obj['iDay'] = iDay
			obj['iiDays'] = iiDays
			obj['ivDays'] = ivDays
			obj['iWeek'] = iWeek

			obj['iiiDays'] = iiiDays
			obj['viiDays'] = viiDays
			obj['xvDays'] = xvDays
			obj['xxxDays'] = xxxDays

			obj['dateCreated'] = dict_param[length-i-1]['dateCreated']

			arr.append(obj)

		# print(arr)

		return arr


	def dict_converter(self, tup_param):
		arr = []
		for i in range(len(tup_param)):
			obj = {}
			obj['id'] = tup_param[i][0]
			obj['mac'] = tup_param[i][1]
			obj['wallet'] = tup_param[i][2]
			obj['packages'] = tup_param[i][3]
			obj['dateCreated'] = tup_param[i][4]

			arr.append(obj)

		return arr


	def init_package_values(self, cursor):
		# Establish mysql connection & cursor
		#conn = self.conn
		#cursor = conn.cursor()

		# Get tha mac actives per month
		cursor.callproc('GET_ACTIVE_MACS', ['countActivePM', 'getMac', ''])
		for result in cursor.stored_results():
			get_macs = result.fetchall()
		
		get_macs = [i[0] for i in get_macs]

		# Declare array containers
		arr = []
		arr2 = []

		# Loop through get_macs list where each element will be used as parameter to call the procedure
		for i in range(len(get_macs)):
			mac_param = get_macs[i]

			cursor.callproc('packages_to_decode', [get_macs[i]])
			for result in cursor.stored_results():
				packages_to_decode = result.fetchall()

			# Convert the tuples result into dictionary
			packages_to_decode = self.dict_converter(packages_to_decode)
			# Call the 'package_decoder' function
			decoded_packages = self.package_decoder(packages_to_decode)
			# Conpute for package_value by calling 'compute_packages' function
			raw_package_values = self.compute_packages(decoded_packages)

			arr.append(raw_package_values)

		# Convert the mulltidimensional list into single dimensional list
		for i in range(len(arr)):
			for j in range(len(arr[i])):
				arr2.append(arr[i][j])

		with open('mydata.json', 'w') as f:
			json.dump('Insertion Complete', f, ensure_ascii = False)


		return arr2



	def fill_computed_packages(self):
		# Establish mysql connection & cursor
		try:
			conn = mysql.connector.connect(user='root', password='r3m0teSec', database='mac')
		except Error as err:
			print('Connection Unavailble Needs reconnect')

		cursor = conn.cursor()

		values = self.init_package_values(cursor)
		cursor.callproc('package_results', ['truncate', ''])		

		for i in range(len(values)):
			mac = values[i]['mac']
			wallet = values[i]['wallet']
			xxxMinutes = values[i]['xxxMinutes']
			iHour = values[i]['iHour']
			iiHours = values[i]['iiHours']
			iiiHours = values[i]['iiiHours']
			vHours = values[i]['vHours']
			iDay = values[i]['iDay']
			iiDays = values[i]['iiDays']
			ivDays = values[i]['ivDays']
			iWeek = values[i]['iWeek']

			iiiDays = values[i]['iiiDays']
			viiDays = values[i]['viiDays']
			xvDays = values[i]['xvDays']
			xxxDays = values[i]['xxxDays']

			dateCreated = values[i]['dateCreated']

			cursor.callproc('fill_computed_packages', [
				mac, 
				wallet, 
				xxxMinutes, 
				iHour, 
				iiHours, 
				iiiHours, 
				vHours, 
				iDay, 
				iiDays, 
				ivDays, 
				iWeek, 
				iiiDays, 
				viiDays, 
				xvDays, 
				xxxDays, 
				dateCreated])
			
			conn.commit()

		# Check for time when insertion is finished
		print("Process Complete at " + str(datetime.datetime.now()))
		cursor.close()

		# Run in backgound
		interv = 1000	# 60secs * 30mins
		x = threading.Timer(interv, self.fill_computed_packages)
		x.start()
		
		










	# TEST DUMMY FUNCTIONS
	def xxx(self):
		conn = self.conn
		cursor = conn.cursor()
		cursor.callproc('proc1')
		for result in cursor.stored_results():
			x = result.fetchall()

		y = [i[0] for i in x]
		print(y)

	def diction(self):
		conn = self.conn
		cursor = conn.cursor()

		cursor.execute("INSERT INTO testing SET testing.name = 'Dexter', testing.age = 22, testing.email = 'email.com' ")
		conn.commit()

		print('Inserted Successfully')

		x = threading.Timer(3.0, self.diction)
		x.start()

	def zzz(self):
		x = int(-1)
		print(x)





if __name__ == '__main__':
	x = PackageValue()
	xx = x.fill_computed_packages()
	

















	'''
	arr_17 = [
		{
			'mac' : 'aaa',
			'wallet' : 1000,
			'packages' : ',30Minutes,146,1Hour,178,2Hours,17,5Hours,11,1Day,5,2Days,0,3days,0,1Week,0',
			'dateCreated' : '2018-11-20'
		},
		{
			'mac' : 'aaa',
			'wallet' : 2000,
			'packages' : ',30Minutes,115,1Hour,189,2Hours,123,5Hours,111,1Day,21,2Days,21,3days,21,1Week,65',
			'dateCreated' : '2018-11-21'
		}
	]

	arr_19 = [
		{
			'mac' : 'aaa',
			'wallet' : 1000,
			'packages' : ',30Minutes,146,1Hour,178,2Hours,17,3Hours,6,5Hours,11,1Day,5,2Days,0,4days,0,1Week,0',
			'dateCreated' : '2018-11-20'
		},
		{
			'mac' : 'aaa',
			'wallet' : 2000,
			'packages' : ',30Minutes,115,1Hour,189,2Hours,123,5Hours,111,1Day,21,2Days,21,4days,21,1Week,65',
			'dateCreated' : '2018-11-21'
		}
	]

	arr_27 = [
		{
			'mac' : 'aaa',
			'wallet' : 1000,
			'packages' : ',30Minutes,146,1Hour,178,2Hours,17,5Hours,11,1Day,5,2Days,0,3days,0,1Week,0,3Hours,9,3Days,9,7Days,9,15Days,9,30Days,9',
			'dateCreated' : '2018-11-20'
		},
		{
			'mac' : 'aaa',
			'wallet' : 2000,
			'packages' : ',30Minutes,115,1Hour,189,2Hours,123,5Hours,111,1Day,21,2Days,21,3days,21,1Week,65,3Hours,12,3Days,12,7Days,12,15Days,12,30Days,12',
			'dateCreated' : '2018-11-21'
		}
	]

	arr_mix = [
		{
			'mac' : 'aaa',
			'wallet' : 1000,
			'packages' : ',30Minutes,146,1Hour,178,2Hours,17,5Hours,11,1Day,5,2Days,0,3days,0,1Week,0,3Hours,9,3Days,9,7Days,9,15Days,9,30Days,9',
			'dateCreated' : '2018-11-20'
		},
		{
			'mac' : 'aaa',
			'wallet' : 2000,
			'packages' : ',30Minutes,115,1Hour,189,2Hours,123,5Hours,111,1Day,21,2Days,21,3days,21,1Week,65,3Hours,12,3Days,12,7Days,12,15Days,12,30Days,12',
			'dateCreated' : '2018-11-21'
		},
		{
			'mac' : 'aaa',
			'wallet' : 2000,
			'packages' : ',30Minutes,115,1Hour,189,2Hours,123,5Hours,111,1Day,21,2Days,21,3days,21,1Week,65',
			'dateCreated' : '2018-11-22'
		},
		{
			'mac' : 'aaa',
			'wallet' : 2000,
			'packages' : ',30Minutes,115,1Hour,189,2Hours,123,5Hours,111,1Day,21,2Days,21,4days,21,1Week,65',
			'dateCreated' : '2018-11-23'
		},
		{
			'mac' : 'aaa',
			'wallet' : 2000,
			'packages' : '0',
			'dateCreated' : '2018-11-24'
		}
	]

	xx = x.package_decoder(arr_mix)
	yy = x.compute_packages(xx)

	with open('test.json', 'w') as f:
		json.dump(yy, f, ensure_ascii = False)
	
	'''









'''		A FUNCTION THAT EXECUTES EVERY n SECONDS 
def test1(self):
	cursor.callproc('proc1')
	for result in cursor.stored_results():
		x = result.fetchall()

	print(x)

	x = threading.Timer(3.0, test1, [''])
	x.start()


if __name__  == "__main__":
	test1('')

'''
