import nmap3

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def parseNmapResults(results):
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
            targetList[IPAddress] = currentDict

    return targetList


if __name__ == "__main__":
    nmap = nmap3.Nmap()
    results = {}
    results = nmap.scan_top_ports("192.168.1.124/24", args="-sV")
    targets = parseNmapResults(results)


    for key, value in targets.items():
        print(key, value)