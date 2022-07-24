from genotype import *
from examplePrimitives import *

def main():
	# example of manually defining a tree
	manualTree = GeneticTree(ATTACKER, IP_ACTION)
	manualTree.root.func = hard_coded_range_if # basically a function pointer
	manualTree.root.children = [Node(IP_ACTION), Node(IP_ACTION)]
	manualTree.root.children[0].func = action0
	manualTree.root.children[1].func = action1

	context = {'ip address': '111.111.111.111'}
	testReturn = manualTree.execute(context)
	print("test return value", testReturn)

	# # example of randomly generating a tree where all branches go to some depth limit
	# fullTree = GeneticTree(ATTACKER, IP_ACTION)
	# fullTree.initialize(4, full=True)

	# fullTree.execute(context)

	# # example of randomly generating a tree where one branch goes to the depth
	# # limit and all other branches may or may not reach the depth limit
	# growTree = GeneticTree(ATTACKER, IP_ACTION)
	# growTree.initialize(4, grow=True)

	# growTree.execute(context)




if __name__ == '__main__':
	main()