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


SSHACTIONS = 'sshactions'
SSHACTIONSGET = 'sshactionsget'
SSHACTIONSPUT = 'sshactionsput'

SFTP ='sftp'
SFTPACTIONS = 'sftpactions'
SFTPACTIONSGET = 'sshactions'


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
		print("Choosing left Action")
		input_nodes[0].execute(context)
		# sftp
	elif service == rAction:
		print("Choosing right Action")
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
@GeneticTree.declarePrimitive(ATTACKER, SSH, (SSHACTIONS, SSHACTIONS,SSHACTIONS,SSHACTIONS))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'

	inform = context['inform']
	if inform == "unknown":
		return "ssh"
	
	context['inform'] = "unknown"
	print('SSH Input Node 0', input_nodes[0].execute(context))
	print('SSH Input Node 1', input_nodes[1].execute(context))
	print('SSH Input Node 2', input_nodes[1].execute(context))
	print('SSH Input Node 3', input_nodes[1].execute(context))

	print("Input Nodes ", input_nodes)
	context['inform'] = 'known'

	actions = {}
	actions = dictActions(input_nodes, context)
	context['inform'] = 'known'
	print("Actions list",actions)
	#actions[action].execute(context)
	return performAction(actions, action, context)

# SSH remote command that can be run using the active ssh connection
@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def downloadFile(self, input_nodes, context):
	# Inform the parrent node of what leaf i am
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

















