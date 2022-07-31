from fileinput import filename
from genotype import *
from primitiveFunctions import *
from protocol_ssh import *
from ftplib import FTP
from scp import SCPClient
import scp
import nmap3

import random
import socket 
import os.path
import time

# Needed Information for Agents to function
USERNAME = "spiegel"
PASSWD = "1226"
REMOTEDIR = "/home/spiegel"
LOCALDIR = "/home/spiegel/Capstone-Project-2022/src"


# Actions
TRANSFREFILE = "transferFile"
SUBACTION = "downloadFile"
FILENAME = "user.txt"

# defining types of agents as constant strings
ATTACKER = 'attacker'

# Decision Tree Declerations
BOB = "bob"

# defining data types of primitives as constant strings
SERVICE = 'service'

# SSH
SSH = 'ssh'
SSHACTIONS = 'sshactions'
SSHACTIONDTRANSFERFILE = "sshactionstransferfile"

# SFTP
SFTP ='sftp'
SFTPACTIONS = 'sftpactions'

# RECON
RECON = 'recon'

NMAP = "nmap"
SCANNETWORKSERVICES = 'scannetworkservices'
SCANNETWORKOPERATINGSYSTEMS = "scannetworkoperatingsystems"



######################################################################################
#									Decesion Tree Declerations						 #
######################################################################################
@GeneticTree.declarePrimitive(ATTACKER, BOB, (RECON, SERVICE))
def hard_coded_range_if(self, input_nodes, context):
	print("Bob is building context")
	context["username"] = USERNAME
	context["password"] = PASSWD
	context["localDirectory"] = LOCALDIR
	context["remoteDirectory"] = REMOTEDIR
	# Adding target to context
	context['ip address'] = ""


	# Set initial recon
	context["action"] = SCANNETWORKSERVICES
	context['service'] = RECON
	service = context['service']
	# Set the Recon Tool to use
	context["recontool"] =  NMAP
	context["nmapFlags"] = "-sV"
	# Set the IP CIDR to scan with the above tool
	context["ipRange"] = getCIDRrange(context, "24")
	print("ipRange", context["ipRange"] )

	# Perform action from services context
	# this will allow for expansion of child nodes for more services
	services = {}
	services = dictActions(input_nodes, context)
	print("service",service)
	performAction(services, service, context)

	targetList = filterForService(context, SSH)
	print(targetList)









######################################################################################
#									SERVICE Declerations							 #
######################################################################################

# This is the root primitive of the Services node. 
@GeneticTree.declarePrimitive(ATTACKER, SERVICE, (SFTP, SSH))
def hard_coded_range_if(self, input_nodes, context):
	service = context['service']

	

	# Perform action from services context
	# this will allow for expansion of child nodes for more services
	services = {}
	services = dictActions(input_nodes, context)
	return performAction(services, service, context)




######################################################################################
#									SSH Declerations								 #
######################################################################################

# SSH Login Node. This will loginto the supplied address "ip address" found in context
@GeneticTree.declarePrimitive(ATTACKER, SSH, (SSHACTIONS, SSHACTIONS))
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
	ssh = ssh_connect(ip_address, port, username, password)
	# Storing SSH Object in context
	context['ssh'] = ssh

	# List of SSHACTIONS leaf nodes for possible execution
	# 'action' in context must be set and possibly 'subaction' depending on leaf used
	actions = {}
	actions = dictActions(input_nodes, context)
	print("action", action)
	return performAction(actions, action, context)

######################################################################################
# 		SSH remote command that can be run using the active ssh connection			 #
######################################################################################
@GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
def scpTransferFile(self, input_nodes, context):
	# Inform the parrent node of what leaf action i am
	inform = context['inform']
	if inform == "unknown":
		return "transferFile"

	# What kind of tranfer
	subaction = context['subaction']
	fileName = context['fileName']
	remoteDirectory = context['remoteDirectory']
	localDirectory = context['localDirectory']

	remoteFile = buildFilePath(remoteDirectory, fileName)
	localFile = buildFilePath(localDirectory, fileName)

	# Getting SSH object from context
	ssh = context['ssh']
	# Creating SCP object for file transfer
	scp = SCPClient(ssh.get_transport())

	if subaction == 'downloadFile':
		print("Downloading File", fileName, localDirectory)
		scp.get(remoteFile, local_path=localDirectory)

	if subaction == 'downloadDirectory':
		scp.get(remoteDirectory, local_path=localDirectory, recursive=True)

	if subaction == 'uploadFile':
		scp.put(localFile, remoteDirectory)

	if subaction == "uploadDirectory":
		scp.put(localDirectory, remoteDirectory, recursive=True)

	ssh.close()
	print('SCP Files Transfered')



# Replicate and launch agent on remote system
# @GeneticTree.declarePrimitive(ATTACKER, SSHACTIONS, ())
# def replicateAgent(self, input_nodes, context):
# 	pass






######################################################################################
#									SFTP Declerations								 #
######################################################################################
# Root SFTP Node to create SFTP Object 
@GeneticTree.declarePrimitive(ATTACKER, SFTP, (SFTPACTIONS, SFTPACTIONS))
def sftp(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	action = context['action']		# parameter is a Dict with 'ip address'

	inform = context['inform']
	if inform == "unknown":
		return SFTP

	# getting SSH parameters from context
	port = context['port']
	username = context['username']
	password = context['password']
	# Creating SSH Connection object and store it in context
	# To pass through to SSH Action leafs
	ssh = ssh_connect(ip_address, port, username, password)
	# Storing SSH Object in context
	context['ssh'] = ssh


	actions = {}
	actions = dictActions(input_nodes, context)
	return performAction(actions, action, context)




# SFTP File Transfer
# directory knowledge is a must know because
# SFTP works from the root source of where the environment is run from
# It tends to start local directory from project root folder
# remote directory is root from whereever SFTP configureation is set
# this is generally the users home directory
@GeneticTree.declarePrimitive(ATTACKER, SFTPACTIONS, ())
def transferFiles(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return "transferFile"
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'

	# What kind of tranfer
	subaction = context['subaction']
	fileName = context['file']
	remoteDirectory = context['remoteDirectory']
	localDirectory = context['localDirectory']
	# Getting SSH object from context
	ssh = context['ssh']
	# getting transport object
	transport = ssh.get_transport()
	#establishing sftp connection from ssh trannsport object session
	sftp = paramiko.SFTPClient.from_transport(transport)




	if subaction == "downloadFile":
		# Download File
		source = buildFilePath(remoteDirectory, fileName)
		destination = buildFilePath(localDirectory, fileName)
		sftp.get(source, destination)

	if subaction == "uploadFile":
		source = "testing.txt"

		source = buildFilePath(localDirectory, fileName)
		destination = buildFilePath(remoteDirectory, fileName)
		sftp.put(source, destination)

	sftp.close()
	print('Chose SFTP File Transfer', ip_address)















######################################################################################
#									Recon Declerations								 #
######################################################################################
# Root SFTP Node to create SFTP Object 
@GeneticTree.declarePrimitive(ATTACKER, RECON, (NMAP, ))
def hard_coded_range_if(self, input_nodes, context):
		# Informant clause to inform parrent node on what this node is
	inform = context['inform']
	if inform == "unknown":
		return RECON
	
	service = context['recontool']
	
	# Perform action from services context
	# this will allow for expansion of child nodes for more services
	services = {}
	services = dictActions(input_nodes, context)
	return performAction(services, service, context)


@GeneticTree.declarePrimitive(ATTACKER, NMAP, (SCANNETWORKSERVICES, SCANNETWORKSERVICES))
def nmapscan(self, input_nodes, context):
	action = context['action']		# what action is stored in context
	inform = context['inform']
	if inform == "unknown":
		return NMAP

	# Actions available definer
	actions = {}
	actions = dictActions(input_nodes, context)
	return performAction(actions, action, context)

# SNetwork Wide Services scan
@GeneticTree.declarePrimitive(ATTACKER, SCANNETWORKSERVICES, ())
def scanNetworkServices(self, input_nodes, context):
	inform = context['inform']
	if inform == "unknown":
		return SCANNETWORKSERVICES

	print("Scanning Network")
	ipRange = context["ipRange"]
	nmapFlags = context["nmapFlags"]
	nmap = nmap3.Nmap()
	results = {}
	results = nmap.scan_top_ports(ipRange, args=nmapFlags)
	targets = parseNmapNetworkServices(results)
	context[SCANNETWORKSERVICES] = targets
	print('Scan Network Services')
	return context



