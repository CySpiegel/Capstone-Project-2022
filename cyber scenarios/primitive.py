from genotype import *
from primitiveFunctions import *
import random
import socket 
import os.path
import time

# defining types of agents as constant strings
ATTACKER = 'attacker'

# defining data types of primitives as constant strings
IP_ACTION = 'ip action'
IP_ADDRESS = 'ip address'

SERVICE = 'service'
SSH = 'ssh'
SFTP ='sftp'


SSHACTIONS = 'sshactions'
SFTPACTIONS = 'sftpactions'


######################################################################################
#									SERVICE Declerations								 #
######################################################################################
@GeneticTree.declarePrimitive(ATTACKER, SERVICE, (SFTP, SSH))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	service = context['service']		# parameter is a Dict with 'ip address'

	context['inform'] = "unknown"
	#inform left vs right
	lAction = input_nodes[0].execute(context)
	rAction = input_nodes[1].execute(context)
	context['inform'] = "known"

	
	print("L Action: ",lAction)
	print("r Action: ", rAction)

	print("Targeting Service: ", service)
	if service == lAction:
		input_nodes[0].execute(context)
		# sftp
	elif service == rAction:
		input_nodes[1].execute(context)
	else:
		# send to new tree
		print("L Action: ",lAction)
		print("r Action: ", rAction)


		exit(1)



######################################################################################
#									SSH Declerations								 #
######################################################################################

# SSH Login Node. This will loginto the supplied address "ip address" found in context
@GeneticTree.declarePrimitive(ATTACKER, SSH, (SSHACTIONS,SSHACTIONS))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']

	inform = context['inform']
	if inform == "unknown":
		return "ssh"

	context['inform'] = "unknown"
	actions = {}

	for node in input_nodes:
		nodeAction = node.execute(context)
		actions[nodeAction] = node

	#if check needed to see is action is in dict
	if action in actions:
		actions[action].execute(context)
	else:
		print("The current action from context is dictionary of actions")

	

	# if action == "getFile":
	# 	input_nodes[0].execute(context)
	# 	# sftp
	# elif action == "putFile":
	# 	input_nodes[1].execute(context)
	# else:
	# 	# send to new tree
	# 	exit(1)

# SSH remote command that can be run using the active ssh connection
@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def downloadFile(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "getFile"
	
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH download file from', ip_address)

@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def uploadFile(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "putFile"
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH upload file to', ip_address)





######################################################################################
#									SFTP Declerations								 #
######################################################################################

@GeneticTree.declarePrimitive(ATTACKER, SFTP, (SFTPACTIONS, SFTPACTIONS))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'

	inform = context['inform']
	if inform == "unknown":
		return "sftp"



	context['inform'] = "unknown"
	actions = {}

	for node in input_nodes:
		nodeAction = node.execute(context)
		actions[nodeAction] = node

	#if check needed to see is action is in dict
	if action in actions:
		actions[action].execute(context)
	else:
		print("The current action from context is dictionary of actions")
	if action == "getFile":
		input_nodes[0].execute(context)
		# sftp
	elif action == "putFile":
		input_nodes[1].execute(context)
	else:
		# send to new tree
		exit(1)

@GeneticTree.declarePrimitive(ATTACKER, SFTPACTIONS, ())
def action0(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "getFile"
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SFTP getFile', ip_address)

@GeneticTree.declarePrimitive(ATTACKER, SFTPACTIONS, ())
def action1(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "putFile"
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SFTP putFile', ip_address)

















