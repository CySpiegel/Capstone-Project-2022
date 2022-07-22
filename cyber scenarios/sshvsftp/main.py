from genotype import *
from primitive import *



if __name__ == "__main__":
    # # defining types of agents as constant strings
    # ATTACKER = 'attacker'

    # # defining data types of primitives as constant strings
    # IP_ACTION = 'ip action'
    # IP_ADDRESS = 'ip address'

    # # example of manually defining a tree
    # manualTree = GeneticTree(ATTACKER, IP_ACTION)
    # manualTree.root.func = hard_coded_range_if # basically a function pointer
    # manualTree.root.children = [Node(IP_ACTION), Node(IP_ACTION)]
    # manualTree.root.children[0].func = action0
    # manualTree.root.children[1].func = action1

    # context = {'ip address': '192.168.1.200', 'service': 'ssh'}
    # manualTree.execute(context)


    growTree = GeneticTree(ATTACKER, SERVICE)
    growTree.initialize(3, grow=True)
    