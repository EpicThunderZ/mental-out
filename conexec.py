from modules.common import *


class Job:
		def __init__(self, code):
			self.code = code

		def execute(self):
			exec(self.code)


class World:

	def start_connection():
		# global connection
		# scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#	print("Authenticating...")
		# creds = ServiceAccountCredentials.from_json_keyfile_name('service_account_credentials.json', scope)
		# client = gspread.authorize(creds)
		World.client = connection.connect()
		# sheet = client.open('Exterior').worksheet(socket.gethostname())
		World.sheet = connection.opensheet('Exterior',socket.gethostname(),World.client)
		World.data = World.sheet.get_all_records()[0]
		World.DEBUGMODE = World.data["DEBUGMODE"]


	def initialize():

		if World.DEBUGMODE=='True':
			print(World.data)

		for col in range(0,len(World.data)-1):
			# var=sheet.cell(1,col).value 	
			var = list(World.data.keys())[col]
			exec(f"World.{var} = World.data[var]")	
			exec(f'''
if World.{var}=="":
	World.{var}=None
elif World.{var}=="True":
	World.{var}=True
elif World.{var}=="False":
	World.{var}=False
else:
	#World.{var}=str(World.data[{var}])
	pass
		'''
			)
			if World.DEBUGMODE=='True' or World.DEBUGMODE == True:
				print(f"{var}={World.data[var]}")


	def prepare(): 
		# global operations
		World.nodes = deepcopy(operations)
		World.processes = deepcopy(operations)
		for key in list(operations['non-uniform'].keys()):
			exec(f"World.nodes['non-uniform'][key] = World.{key}")
			World.processes['non-uniform'][key] = Job('')
			World.processes['non-uniform'][key].code=operations['non-uniform'][key]


	def non_uniformers():
		for key in list(World.nodes['non-uniform'].keys()):
			if World.nodes['non-uniform'][key] is True:
				World.processes['non-uniform'][key].execute()


def main():
	World.start_connection()
	World.initialize()
	World.prepare()
	World.non_uniformers()


if __name__ == '__main__':
	World.start_connection()
	World.initialize()
	World.prepare()
	if World.SWITCH == True:
		World.non_uniformers()	
