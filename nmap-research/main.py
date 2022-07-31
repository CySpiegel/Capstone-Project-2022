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
        servicesDict['hostname'] = results[IPAddress]["hostname"][0]["name"]
        servicesDict["services"] =  currentDict
        targetList[IPAddress] = servicesDict

    return targetList


def parseNmapOSScan(results):
    results.pop("stats")
    results.pop("runtime")
    listOfIPAddr = []
    for key, value in results.items():
        listOfIPAddr.append(key)


if __name__ == "__main__":
    nmap = nmap3.Nmap()
    results = {}
    results = nmap.scan_top_ports("192.168.1.124/24", args="-sS")
    targets = parseNmapNetworkServices(results)
    #os_results = nmap.nmap_os_detection("192.168.1.124")



    for key, value in targets.items():
        if key == "192.168.1.124":
            print("ip address: ", key, value)
        # results = nmap.scan_top_ports(key, args="-sP")
        # parseHostName(results)
        # print(info)