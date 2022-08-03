import socket
import nmap3
import os

SCANNETWORKSERVICES = 'scannetworkservices'

def mkdir(localDir, address):
    newDir = localDir + "/" + address
    os.mkdir(newDir)
    return newDir

#return a dictionary of actions available
def dictActions(input_nodes, context):
    context['inform'] = 'unknown'
    actions = {}
    for node in input_nodes:
        nodeAction = node.execute(context)
        actions[nodeAction] = node
    context['inform'] = 'known'
    return actions

# Perform the nodes action based on context
def performAction(actions, action, context):
    print("From PerformAction")
    print("Actions", actions)
    print("Attempting Action", action)
    print("Context Action", context["action"])
    if action in actions:
        return actions[action].execute(context)
    else:
        print("Action Missing: ", action)
        return throwError(1)


def buildFilePath(path, fileName):
    return path + "/" + fileName

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

# Only used in leaf node
def parseNmapNetworkServices(results):
    results.pop("stats")
    results.pop("runtime")
    listOfIPAddr = []
    for key, value in results.items():
        listOfIPAddr.append(key)

    # Build Target List by IP address and information
    targetList = {}
    for IPAddress in listOfIPAddr:
        targetList[IPAddress] = {}
        for targetPorts in results[IPAddress]["ports"]:
            portName = targetPorts["service"]["name"]
            portNumber = targetPorts["portid"]
            portState = targetPorts["state"]
            portInfo = {"name": portName, "portid": portNumber, "state": portState}
            currentDict = targetList[IPAddress]
            currentDict[portName] = portInfo
        servicesDict = {}
        if results[IPAddress]["hostname"] != []:
            servicesDict['hostname'] = results[IPAddress]["hostname"][0]["name"]
        servicesDict["services"] =  currentDict
        targetList[IPAddress] = servicesDict

    return targetList

def getCIDRrange(ipAddress, range):
    ipRange = ipAddress + "/" + str(range)
    return ipRange


def filterForService(context, service):
    if SCANNETWORKSERVICES in context:
        scanResults = context[SCANNETWORKSERVICES]
        targetList = {}
        IPAddressList = list()
        # Build list of IP Addresses from scan results
        for key in scanResults:
            IPAddressList.append(key)
        
        for address in IPAddressList:
            if address == context["localIP"]:
                continue
            services = scanResults[address]["services"]

            if service in services:
                targetedService = services[service]
                state = targetedService["state"]
                if state == "open":
                    portid = targetedService["portid"]
                    targetList[address] = portid
        storeAs = service + "Targets"
        context[storeAs] = targetList
        return targetList
    else:
        throwError(2)
        return []

def dictToList(dict):
    itemList = list()
    print("Dict To list")
    for key, value in dict.items():
        print(key, value)
        itemList.append([key, value])
    return itemList

def filterByMachineName(context, targetDict, substringName):
    if SCANNETWORKSERVICES in context:
        scanResults = context[SCANNETWORKSERVICES]
        IPAddresses=list()
        for ip, value in targetDict.items():
            IPAddresses.append(ip)

        for ip in IPAddresses:
            if "hostname" in scanResults[ip]:
                print("hostname",scanResults[ip]["hostname"])
                if substringName in scanResults[ip]["hostname"]:
                    print("Found machine: ", scanResults[ip]["hostname"])
                    continue
                else:
                    targetDict.pop(ip)
            else:
                targetDict.pop(ip)

        print("Target With matching Names", targetDict)
        return targetDict



def throwError(error):
    errorTable = {}
    errorTable[1] = "The current action from context is not found in the dictionary of actions provided.\nPlease check that leaf nodes are being generatted correctly. Most common issue is the leaf was not generated." 
    errorTable[2] = "scannetworkservices is missing from context. did you run the recon tree leaf scannetworkservices?"
    errorTable[3] = "key not in context"
    
    print(errorTable[error])
    return errorTable[error]

