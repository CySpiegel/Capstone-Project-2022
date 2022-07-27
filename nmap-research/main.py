import os
import nmap3


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
    #results = nmap.scan_top_ports("192.168.1.124/24", args="-sV")
    #targets = parseNmapResults(results)
    os_results = nmap.nmap_os_detection("192.168.1.124")



    for key, value in os_results.items():
        print("ip address: ", key)
        print(os_results[key])