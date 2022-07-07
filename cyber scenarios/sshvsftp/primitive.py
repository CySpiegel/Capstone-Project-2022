from genotype import *
import random


# defining types of agents as constant strings
ATTACKER = 'attacker'

# defining data types of primitives as constant strings
IP_ACTION = 'ip action'
IP_ADDRESS = 'ip address'

# only attackers can use this primitive, it's data type is IP_ACTION, and it 
# requires 2 IP_ACTION-type children nodes.
@GeneticTree.declarePrimitive(ATTACKER, IP_ACTION, (IP_ACTION, IP_ACTION))
def hard_coded_range_if(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
	service = context['service']		# parameter is a Dict with 'ip address'
	# Validate IP range

	if service == "ssh":
		input_nodes[0].execute(context)
	else:
		input_nodes[1].execute(context)


# only attackers can use this primitive, it's data type is IP_ACTION, and it
# does not have any children (so it's a leaf node)
@GeneticTree.declarePrimitive(ATTACKER, IP_ACTION, ())
def action0(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SSH', ip_address)

# only attackers can use this primitive, it's data type is IP_ACTION, and it
# does not have any children (so it's a leaf node)
@GeneticTree.declarePrimitive(ATTACKER, IP_ACTION, ())
def action1(self, input_nodes, context):
	ip_address = context['ip address'] 	# we assume the provided context
										# parameter is a Dict with 'ip address'
	print('Chose SFTP', ip_address)