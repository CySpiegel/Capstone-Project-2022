import genotype
from genotype import *
from primitive import *
from primitiveFunctions import *

class SimpleAgent:
    def __init__(self, name, context, decisionTree = 0):
        self.name = name
        self.Tree = decisionTree
        self.context = context
        self.context["localIP"] = extract_ip()


    def actionsToTake(self, context):
        self.Tree.execute(context)

    def run(self):
        self.actionsToTake(self.context)
    
    def updateContext(self, context):
        self.context = context
    
    def addToContext(self, key, action):
        self.context[key] =  action

    def randomTree(self):
        # Randomly Grow tree to a depth of 3 if possible
        self.Tree = GeneticTree(ATTACKER, SERVICE)
        self.Tree.initialize(3, full=True)

    # Returns the IP of what this agent is running on
    def hostIP(self):
        hostIP = self.context['localIP']
        return hostIP
