import socket

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
    if action in actions:
        return actions[action].execute(context)
    else:
        return throwError(1)

def buildContext(context):
    # initial context
    context = {"ip address": "192.168.1.124", "service": "ssh", "action": "getFile", "file": "user.txt", "filepath": "/home/spiegel/", "username": "spiegel", "password": "1226"}
    return context


def buildGetFileFromRemoteSystem(context):
    remotecommand = ""
    command = "scp "
    at = "@"
    colan = ":"
    space = " "
    targetIP = context['ip address']
    username = context['username']
    fileName = context['file']
    remoteFilePath = context['remoteFilePath']
    destinationFilePath = context['destinationFilePath']

    remotecommand = command + username + at + targetIP + colan + remoteFilePath + fileName + space + destinationFilePath
    return remotecommand

def sendToRemoteSystem(context, targetAddress):
    remotecommand = ""
    command = "scp "
    at = "@"
    colan = ":"
    space = " "
    targetIP = targetAddress
    username = context['username']
    fileName = context['file']
    destinationFilePath = context['destinationFilePath']
    extra = ";1226\n"

    remotecommand = command + fileName + space + username + at + targetIP + colan + destinationFilePath

    return remotecommand

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

def throwError(error):
    errorTable = {}
    errorTable[1] = "The current action from context is not found in the dictionary of actions provided.\nPlease check that leaf nodes are being generatted correctly. Most common issue is the leaf was not generated." 
    
    print(errorTable[error])
    return errorTable[error]