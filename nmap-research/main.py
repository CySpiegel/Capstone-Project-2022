import os
import nmap3


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
        servicesDict["services"] =  currentDict
        targetList[IPAddress] = servicesDict

    return targetList


def parseNmapOSScan(results):
    results.pop("stats")
    results.pop("runtime")
    listOfIPAddr = []
    for key, value in results.items():
        listOfIPAddr.append(key)

SCANNETWORKSERVICES = 'scannetworkservices'

def filterForService(context, service):
    if SCANNETWORKSERVICES in context:
        scanResults = context[SCANNETWORKSERVICES]
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
                portID = targetedService["portid"]
                print("PortID", portID)
                if state == "open":
                    targetList.append(adress)
        targetList.remove(context["localIP"])
        storeAs = service + "Targets"
        context[storeAs] = targetList
        return targetList
    else:
        throwError(2)
        return []


if __name__ == "__main__":
    nmap = nmap3.Nmap()
    results = {}
    results = nmap.scan_top_ports("192.168.1.124/24", args="-sV")
    targets = parseNmapNetworkServices(results)
    #os_results = nmap.nmap_os_detection("192.168.1.124")



    for key, value in targets.items():
        print("ip address: ", key)
        #print(value)