import genotype
from genotype import *
from primitive import *

class SimpleAgent:
    def __init__(self, name, context, decisionTree = 0):
        self.name = name
        self.Tree = decisionTree
        self.context = context

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
        self.Tree.initialize(3, grow=True)
    