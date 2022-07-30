import genotype
from genotype import *
from primitive import *
from primitiveFunctions import *
import sys
import os


class SimpleAgent:
    def __init__(self, name, context, species, rootNode):
        self.name = name
        self.Tree = self.buildTree(species, rootNode)
        self.context = context
        self.context["localIP"] = extract_ip()

        if context == 0:
            self.context = self.standardTree()

    # Executes the current context on 
    # the tree currently stored
    def actionsToTake(self, context):
        self.Tree.execute(context)

    def buildTree(self, species, rootNode):
        Tree = GeneticTree(species, rootNode)
        Tree.initialize(4, full=True)

    # Exucutes the currently stored context the 
    # agent has available on the current tree
    # in memmory
    def run(self):
        self.actionsToTake(self.context)
    
    # Replace the current context dictionary with
    # a new context dictionary
    def replaceContext(self, context):
        self.context = context
    
    # Adds to the existing context
    def updateContext(self, key, action):
        if key in self.context:
            self.context[key] =  action
            return True
        else:
            print("key not in context. Use addToContext")
            return False
    
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

    def filterForService(self, service):
        if SCANNETWORKSERVICES in self.context:
            scanResults = self.context[SCANNETWORKSERVICES]
            targetList = list()
            IPAddressList = list()
            # Build list of IP Addresses from scan results
            for key in scanResults:
                IPAddressList.append(key)
            
            for adress in IPAddressList:
                services = scanResults[adress]["services"]

                if service in services:
                    targetedService = services[service]
                    state = targetedService["state"]
                    if state == "open":
                        targetList.append(adress)
            targetList.remove(self.hostIP())
            storeAs = service + "Targets"
            self.context[storeAs] = targetList
            return targetList
        else:
            throwError(2)
            return []


    def recon(self, cidr):
        # Create Recon Tree
        Tree = GeneticTree(ATTACKER, RECON)
        Tree.initialize(3, full=True)
        # Assign Recon Tree to Agent
        self.Tree = Tree
        localIP = self.context["localIP"]
        ipRange = localIP + "/" + cidr
        self.context["ipRange"] = ipRange
        # Running the above Recon Tree
        self.run()


    def getContextValue(self, key):
        storedVaule = ""
        if key in self.context:
            storedVaule = self.context[key]
        else:
            storedVaule = throwError(3)
        return storedVaule

    def attackTargets(self, targetList):
        for target in targetList:
            self.updateContext("ip address", target)
            self.run()

    def generateTree(self, side, treeType, depth):
        # Create Recon Tree
        Tree = GeneticTree(side, treeType)
        Tree.initialize(depth, full=True)
        self.Tree = Tree

    def smithWasHere():
        pass
