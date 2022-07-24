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
	# Validate IP range

	if service == "sftp":
		input_nodes[0].execute(context)
		# sftp
	elif service == "ssh":
		input_nodes[1].execute(context)
	else:
		# send to new tree
		exit(1)



######################################################################################
#									SSH Declerations								 #
######################################################################################


# only attackers can use this primitive, it's data type is IP_ACTION, and it
# does not have any children (so it's a leaf node)
# ssh login attack
@GeneticTree.declarePrimitive(ATTACKER, SSH, (SSHACTIONS,))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'
	# Validate IP range

	if action == "getFile":
		input_nodes[0].execute(context)
		# sftp
	elif action == "putFile":
		input_nodes[1].execute(context)
	else:
		# send to new tree
		exit(1)

@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def action0(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH', ip_address)

@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def action1(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH', ip_address)




######################################################################################
#									SFTP Declerations								 #
######################################################################################

@GeneticTree.declarePrimitive(ATTACKER, SFTP, (SFTPACTIONS,))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'
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
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH', ip_address)

@GeneticTree.declarePrimitive(ATTACKER, SFTPACTIONS, ())
def action1(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH', ip_address)



































# SFTP Actions
@GeneticTree.declarePrimitive(ATTACKER, SFTP, ())
def action0(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SFTP', ip_address)