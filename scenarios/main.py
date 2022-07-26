from os import lseek
from genotype import *
from primitive import *
from simpleAgent import *
from primitiveFunctions import *



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

    # Randomly Grow tree to a depth of 3 if possible
    Tree = GeneticTree(ATTACKER, SERVICE)
    Tree.initialize(4, full=True)
    Tree.printTree()

    context = {"ip address": "192.168.1.124",
                "service": "ssh",
                "port": 22,
                "action": "scpTransferFile",
                "subaction":"uploadDirectory",
                "file": "user.txt",
                "localDir": "",
                "remoteDir": "/home/spiegel/flags",
                "downloadDir": "/home/spiegel/Capstone-Project-2022/downloads",
                "username": "spiegel",
                "password": "1226"
                }
    
    print("\n\nAgent Bob on the job")
    AgentBob = SimpleAgent("BoB", context, Tree)
    AgentBob.hostIP()
    AgentBob.run()

    print("\n\nAgent Smith on the job")

    # Agent Smith
    # Main goal: Replicate itself across the
    # context['service'] = 'sftp'
    # AgentSmith = SimpleAgent("Smith", context)
    # AgentSmith.randomTree()
    # AgentSmith.run()
