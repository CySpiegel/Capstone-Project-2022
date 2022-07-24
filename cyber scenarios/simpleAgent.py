import genotype

class SimpleAgent:
    def __init__(self, name, decisionTree, context):
        self.name = name
        self.Tree = decisionTree
        self.context = context

    def actionsToTake(self, context):
        self.Tree.execute(context)

    def runAgent(self):
        self.actionsToTake(self.context)
    
    def updateContext(self, context):
        self.context = context
    
    def addToContext(self, key, action):
        self.context[key] =  action
    