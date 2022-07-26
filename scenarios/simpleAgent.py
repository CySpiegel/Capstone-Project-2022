import genotype
from genotype import *
from primitive import *
from primitiveFunctions import *
import sys
import os


class SimpleAgent:
    def __init__(self, name, context = 0, decisionTree = 0):
        self.name = name
        self.Tree = decisionTree
        self.context = context
        self.context["localIP"] = extract_ip()

        if context == 0:
            self.context = self.standardTree()

    # Executes the current context on 
    # the tree currently stored
    def actionsToTake(self, context):
        self.Tree.execute(context)

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

    # Will create a generic tree 
    def standardTree(self):
        context = {"ip address": "192.168.1.124",
                    "service": "ssh",
                    "port": 22,
                    "action": "transferFile",
                    "subaction":"uploadDirectory",
                    "file": "user.txt",
                    "localDir": "",
                    "remoteDir": "/home/spiegel/flags",
                    "downloadDir": "/home/spiegel/Capstone-Project-2022/downloads",
                    "username": "spiegel",
                    "password": "1226"
                    }
        return context
    def smithWasHere():
        pass

