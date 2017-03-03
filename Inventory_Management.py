###################################################################################################
# Introduction:	
#				
#				
#
# Usage:		
# Created by:	Allyn Hunt - www.AllynH.com
###################################################################################################

from Header_file import *
import requests
import json

# Uncomment this line to print JSON output to a file:
#f = open('inventoryItem.txt', 'w')

def transferItem(payload, session):
	req_string = base_url + "TransferItem/"
	print "Transferring item from vault to character..."
	res = session.post(req_string, data=payload)
	error_stat = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_stat + "\n"
	return res

def equipItem(payload, session):
	# Send the request to equip the item:
	equip_url = base_url + "EquipItem/"
	print "Equipping item..."
	res = session.post(equip_url, data=payload)
	error_stat = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_stat + "\n"
	return res

def getVault(session):
	getVault_url = base_url + membershipType + "/MyAccount/Vault/"
	res = session.get(getVault_url, params={'accountId': destinyMembershipId})
	print (res.url)
	error_stat = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_stat + "\n"
	#print (res.status_code)
	#print (res.text)
	return res

	
def getCharacterInventory(session, charId):
	req_string = base_url + membershipType + "/Account/" + destinyMembershipId + "/Character/" + charId + "/Inventory/"
	print "Fetching data for: " + req_string + "\n"
	res = session.get(req_string)
	error_stat = res.json()['ErrorStatus']
	print "Error status: " + error_stat + "\n"
	return res

def getCharacterInventorySummary(session, charId):
	req_string = base_url + membershipType + "/Account/" + destinyMembershipId + "/Character/" + charId + "/Inventory/Summary/"
	print "Fetching data for: " + req_string + "\n"
	res = session.get(req_string)
	error_stat = res.json()['ErrorStatus']
	print "Error status: " + error_stat + "\n"
	return res

def parsegetCharacterInventorySummary(session, charInventorySummary, all_data):
	array_size = 0
	vault_list = [{
		'itemName': '',
		'tierTypeName': '',
		'itemTypeName': '',
		'icon': '',
		'bucket': '',
	} for array_size in range(vaultSize)]
	array_size = 0

	for item in charInventorySummary.json()['Response']['data']['items']:
		vault_list[array_size]['itemReferenceHash'] = item['itemHash']
		vault_list[array_size]['itemId'] = item['itemId']
		inventoryItem = all_data['DestinyInventoryItemDefinition'][item['itemHash']]
		#f.write (json.dumps(inventoryItem, indent=4))
		if (inventoryItem['itemName'] != ""):
			bucketHash = all_data['DestinyInventoryBucketDefinition'][item['bucketHash']]
			vault_list[array_size]['itemName'] = inventoryItem['itemName']
			if ((inventoryItem['itemName'] != "Classified") and (inventoryItem['itemHash'] != 1826822442) and (item['bucketHash'] != 1801258597)):
				vault_list[array_size]['itemName'] = inventoryItem['itemName']
				vault_list[array_size]['tierTypeName'] = inventoryItem['tierTypeName']
				vault_list[array_size]['itemTypeName'] = inventoryItem['itemTypeName']
				vault_list[array_size]['icon'] = "http://www.bungie.net/" + inventoryItem['icon']
				vault_list[array_size]['bucket'] = bucketHash['bucketName']
		array_size += 1
		
	return vault_list

def parseVault(session, vaultResult, all_data):
	array_size = 0
	weapon_list = [{
		"membershipType": 2,
		"itemReferenceHash": 0,
		"itemId": 0,
		"characterId": characterId_Warlock,
		"stackSize": 1,
		"transferToVault": False
	} for array_size in range(vaultSize)]
	array_size = 0

	for bucket in vaultResult.json()['Response']['data']['buckets']:
	#f.write (json.dumps(bucket['items'], indent=4))
		for item in bucket['items']:
			#print "Item location: " + item['location']
			#print item['itemInstanceId']
			hashReqString = base_url + "Manifest/6/" + str(item['itemHash'])
			#res2 = requests.get(hashReqString, headers=HEADERS)
			#myItem = item['itemHash']
			weapon_list[array_size]['itemReferenceHash'] = item['itemHash']
			weapon_list[array_size]['itemId'] = item['itemInstanceId']
			#print weapon_list[array_size]['itemReferenceHash']
			#print weapon_list[array_size]['itemId']
			inventoryItem = all_data['DestinyInventoryItemDefinition'][item['itemHash']]
			item_name = inventoryItem['itemName']
			item_tier = inventoryItem['tierTypeName']
			item_type = inventoryItem['itemTypeName']
			item_icon = inventoryItem['icon']
			print "Item name is: " + item_name
			#print "Item type is: " + item_tier + " " + item_type
			#print "Item icon is: http://www.bungie.net" + item_icon
			#print array_size
			array_size += 1
		
	return weapon_list

def parseVaultHtml(session, vaultResult, all_data):
	array_size = 0
	vault_list = [{
		'itemName': '',
		'tierTypeName': '',
		'itemTypeName': '',
		'icon': '',
	} for array_size in range(vaultSize)]
	array_size = 0

	for bucket in vaultResult.json()['Response']['data']['buckets']:
		for item in bucket['items']:
			hashReqString = base_url + "Manifest/6/" + str(item['itemHash'])
			vault_list[array_size]['itemReferenceHash'] = item['itemHash']
			vault_list[array_size]['itemId'] = item['itemInstanceId']
			inventoryItem = all_data['DestinyInventoryItemDefinition'][item['itemHash']]
			if (inventoryItem['itemName'] != ""):
				vault_list[array_size]['itemName'] = inventoryItem['itemName']
				vault_list[array_size]['tierTypeName'] = inventoryItem['tierTypeName']
				vault_list[array_size]['itemTypeName'] = inventoryItem['itemTypeName']
				vault_list[array_size]['icon'] = "http://www.bungie.net/" + inventoryItem['icon']
			#print "Item name is: " + vault_list[array_size]['itemName']
			array_size += 1
		
	return vault_list

def GetCharacterSummary(session):
	req_string = base_url + membershipType + "/Account/" + destinyMembershipId + "/Character/" + characterId + "/"
	res = session.get(req_string)
	print req_string
	error_state = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_state + "\n"
	return res

def GetCurrentBungieUser(session):
	req_string = 'https://www.bungie.net/Platform/User/GetCurrentBungieNetUser/'
	res = session.get(req_string)
	print req_string
	error_state = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_state + "\n"
	return res
	
def GetAdvisorsForCharacter(session):
	req_string = base_url + membershipType + "/Account/" + destinyMembershipId + "/Character/" + characterId + "/Advisors/"
	res = session.get(req_string)
	print req_string
	error_state = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_state + "\n"
	return res
		
def getAccount(session):
	req_string = base_url + membershipType + "/Account/" + destinyMembershipId + "/"
	res = session.get(req_string)
	print req_string
	error_state = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_state + "\n"
	return res

#https://www.bungie.net/Platform/User/GetBungieNetUser/
def GetCurrentUser(session):
	req_string = 'https://www.bungie.net/Platform/User/GetBungieNetUser/'
	res = session.get(req_string)
	print req_string
	error_state = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_state + "\n"
	return res

def GetCurrentBungieAccount(session):
	req_string = 'https://www.bungie.net/Platform/User/GetBungieNetUser/'
	res = session.get(req_string)
	print req_string
	error_state = res.json()['ErrorStatus'].decode('utf-8')
	print "Error status: " + error_state + "\n"

	return res

#TODO: http://destinydevs.github.io/BungieNetPlatform/docs/DestinyService/GetMembershipIdByDisplayName