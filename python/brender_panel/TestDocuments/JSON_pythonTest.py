import json

exDict = {'Objects':[]}
# print(exDict)

val1 = {}
val1['Name'] = "Test2"
# print(val1)
val1['Parent'] = None
# print(val1)

exDict['Objects'].append(val1)

# print(exDict)

val2 = {"Name" : "Test3"}
# print(val2)
val2['Parent'] = 'Test1'
# print(val2)

exDict['Objects'].append(val2)

# print(exDict)

new_string = json.dumps(exDict, indent=2)

# print(new_string)

for obj in exDict['Objects']:
	if 'Test2' in obj['Name']:
		print("it exists")


# exDict['Objects'].append({"Name":"Test1"})
# print(exDict)
# exDict['Objects']['Name']
#------------------------------------------------------------------
# obj_string = '''
# {
# 	"Objects" : [
# 		{
# 			"Name" : "000000_Cloth2D",
# 			"Parent" : null,
# 			"Type" : "MESH",
# 			"Material" : {
# 				"id" : 0,
# 				"Name" : "Clear2DMaterial"
# 			} 

# 		},

# 		{
# 			"Name" : "000000_Cloth2D.wireframe",
# 			"Parent" : "000000_Cloth2D",
# 			"Type" : "CURVE",
# 			"Depth" : 0.001,
# 			"Res" : 2.000,
# 			"Material" : {
# 				"id" : 0,
# 				"Name" : "Clear2DMaterial"
# 			}
# 		}

# 	]
	
# }
# '''

# data = json.loads(obj_string)

# # for obj in data['Objects']:
# # 	# print(obj)
# # 	print(obj['Name'])
# # 	print('\n')

# # for obj in data['Objects']:
# # 	del obj['Type']
	
# new_string = json.dumps(data, indent=2)

# print(new_string)
# # print(type(data['Objects']))