from genotype import *
import random
import socket 
import grpc
import os.path
import actions_pb2_grpc
import actions_pb2
import time

def PerformRemoteAction(stub, host, port, username, password, command):
    request = actions_pb2.RemoteExecutionRequest()
    request.host = host
    request.port = port
    request.username = username
    request.password = password
    request.command = command
    response = stub.RemoteExecution(request)
    return response

# defining types of agents as constant strings
ATTACKER = 'attacker'

# defining data types of primitives as constant strings
IP_ACTION = 'ip action'
IP_ADDRESS = 'ip address'

# Server address of gRPC server
SERVER_ADDRESS = "localhost:23350"

# only attackers can use this primitive, it's data type is IP_ACTION, and it 
# requires 2 IP_ACTION-type children nodes.
@GeneticTree.declarePrimitive(ATTACKER, IP_ACTION, (IP_ACTION, IP_ACTION))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	service = context['service']		# parameter is a Dict with 'ip address'
	# Validate IP range

	if service == "ssh":
		input_nodes[0].execute(context)
		# sftp
	elif service == "sftp":
		input_nodes[1].execute(context)
	else:
		# send to new tree
		exit(1)

# only attackers can use this primitive, it's data type is IP_ACTION, and it
# does not have any children (so it's a leaf node)
# ssh login attack
@GeneticTree.declarePrimitive(ATTACKER, IP_ACTION, ())
def action0(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'

	with grpc.insecure_channel(SERVER_ADDRESS) as channel:
		# create a stub (client)
		stub = actions_pb2_grpc.ActionsStub(channel)
		#recieved = PerformAction(stub)

		# Remote Action Demo
		targetIP = "192.168.1.200"
		targetPort = 22
		targetUsername = "pi"
		targetPassword = ""
		targetCommand = "ls"
		response = PerformRemoteAction(stub, targetIP, targetPort, 
										targetUsername, targetPassword, targetCommand)
	print('Chose SSH', ip_address)

# only attackers can use this primitive, it's data type is IP_ACTION, and it
# does not have any children (so it's a leaf node)
@GeneticTree.declarePrimitive(ATTACKER, IP_ACTION, ())
def action1(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SFTP', ip_address)