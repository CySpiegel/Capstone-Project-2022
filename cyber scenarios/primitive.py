from genotype import *
from primitiveFunctions import *
from protocol_ssh import *
import paramiko
from scp import SCPClient
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
def hard_coded_range_if(self, input_nodes, context):
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



	timeout=5
	remotecommand = "ls"

	# TODO
	# Create SSH connection object and pass it down through context
	# Paramiko establish SSH connection and object here
	# ssh = paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# ssh.connect(ip_address, port, username, password)
	# context['ssh'] = ssh
	ssh = connect(ip_address, port, username, password)
	context['ssh'] = ssh
	actions = {}
	actions = dictActions(input_nodes, context)
	return performAction(actions, action, context)

######################################################################################
# 		SSH remote command that can be run using the active ssh connection			 #
######################################################################################
@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def downloadFile(self, input_nodes, context):
	# Inform the parrent node of what leaf action i am
	inform = context['inform']
	if inform == "unknown":
		return "getFile"

	# TODO
	# Use Paramiko SSH Object to run remote commands to download the targetFile
	ssh = context['ssh']
	scp = SCPClient(ssh.get_transport())
	scp.get("user.txt")


	print('Chose SSH download file from')

@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def uploadFile(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "putFile"
	ip_address = context['ip address']

	# TODO
	# Use paramiko object to upload a file to the targegted ip address
	print('Chose SSH upload file to', ip_address)


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

















