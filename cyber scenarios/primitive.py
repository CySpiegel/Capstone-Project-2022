from genotype import *
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

	print("Targeting Service: ", service)
	if service == lAction:
		input_nodes[0].execute(context)
		# sftp
	elif service == rAction:
		input_nodes[1].execute(context)
	else:
		# send to new tree
		exit(1)



######################################################################################
#									SSH Declerations								 #
######################################################################################

# SSH Login Node. This will loginto the supplied address "ip address" found in context
@GeneticTree.declarePrimitive(ATTACKER, SSH, (SSHACTIONS,SSHACTIONS))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'

	inform = context['inform']
	if inform == "unknown":
		return "ssh"

	if action == "getFile":
		input_nodes[0].execute(context)
		# sftp
	elif action == "putFile":
		input_nodes[1].execute(context)
	else:
		# send to new tree
		exit(1)

# SSH remote command that can be run using the active ssh connection
@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def getfile(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "ssh"
	
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH', ip_address)

@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def putFile(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "ssh"
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH', ip_address)




######################################################################################
#									SFTP Declerations								 #
######################################################################################

@GeneticTree.declarePrimitive(ATTACKER, SFTP, (SFTPACTIONS,SFTPACTIONS))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'

	inform = context['inform']
	if inform == "inform":
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
		return "sftp"
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SFTP', ip_address)

@GeneticTree.declarePrimitive(ATTACKER, SFTPACTIONS, ())
def action1(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "sftp"
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SFTP', ip_address)

















