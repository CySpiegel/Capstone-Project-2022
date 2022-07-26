from genotype import *
from primitiveFunctions import *
from protocol_ssh import *

import random
import socket 
import os.path
import time

# defining types of agents as constant strings
ATTACKER = 'attacker'

# defining data types of primitives as constant strings
SERVICE = 'service'

# SSH
SSH = 'ssh'
SSHACTIONS = 'sshactions'
SSHACTIONSGET = 'sshactionsget'
SSHACTIONSPUT = 'sshactionsput'

# SFTP
SFTP ='sftp'
SFTPACTIONS = 'sftpactions'
SFTPACTIONSGET = 'sshactions'


######################################################################################
#									SERVICE Declerations							 #
######################################################################################

# This is the root primitive of the Services node. 
@GeneticTree.declarePrimitive(ATTACKER, SERVICE, (SFTP, SSH))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	service = context['service']		# parameter is a Dict with 'ip address'

	# Perform action from services context
	# this will allow for expansion of child nodes for more services
	services = {}
	services = dictActions(input_nodes, context)
	return performAction(services, service, context)




######################################################################################
#									SSH Declerations								 #
######################################################################################

# SSH Login Node. This will loginto the supplied address "ip address" found in context
@GeneticTree.declarePrimitive(ATTACKER, SSH, (SSHACTIONS, SSHACTIONS,SSHACTIONS,SSHACTIONS))
def determinSSHActions(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# get the current action from context
	
	# Informant clause to inform parrent node on what this node is
	inform = context['inform']
	if inform == "unknown":
		return SSH

	# getting SSH parameters from context
	port = context['port']
	username = context['username']
	password = context['password']

	# Creating SSH Connection object and store it in context
	# To pass through to SSH Action leafs
	ssh = connect(ip_address, port, username, password)
	# Storing SSH Object in context
	context['ssh'] = ssh

	# List of SSHACTIONS leaf nodes for possible execution
	# 'action' in context must be set and possibly 'subaction' depending on leaf used
	actions = {}
	actions = dictActions(input_nodes, context)
	return performAction(actions, action, context)

######################################################################################
# 		SSH remote command that can be run using the active ssh connection			 #
######################################################################################
@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def scpTransferFile(self, input_nodes, context):
	# Inform the parrent node of what leaf action i am
	inform = context['inform']
	if inform == "unknown":
		return "scpTransferFile"

	# What kind of tranfer
	subaction = context['subaction']
	fileName = context['file']
	remoteDirectory = context['remoteDir']
	downloadDirectory = context['downloadDir']
	localDirectory = context['localDir']
	# Getting SSH object from context
	ssh = context['ssh']
	# Creating SCP object for file transfer
	scp = SCPClient(ssh.get_transport())

	if subaction == 'downloadFile':
		scp.get(fileName, local_path=downloadDirectory)

	if subaction == 'downloadDirectory':
		scp.get(remoteDirectory, local_path=downloadDirectory, recursive=True)

	if subaction == 'uploadFile':
		scp.put(localDirectory+"/"+fileName, remoteDirectory)

	if subaction == "uploadDirectory":
		scp.put("/home/spiegel/Capstone-Project-2022/scenarios", remoteDirectory, recursive=True)

	print('Chose SCP File Transfer through SSH Connection')



# Replicate and launch agend on remote system
@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def replicateAgent(self, input_nodes, context):
	pass






######################################################################################
#									SFTP Declerations								 #
######################################################################################
# Root SFTP Node to create SFTP Object 
@GeneticTree.declarePrimitive(ATTACKER, SFTP, (SFTPACTIONS, SFTPACTIONS))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'

	inform = context['inform']
	if inform == "unknown":
		return "sftp"

	actions = {}
	actions = dictActions(input_nodes, context)
	return performAction(actions, action, context)




# SFTP File Transfer
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

















