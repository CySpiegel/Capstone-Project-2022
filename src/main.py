from genotype import *
from primitive import *
from simpleAgent import *
from primitiveFunctions import *



if __name__ == "__main__":

    # # defining types of agents as constant strings
    # ATTACKER = 'attacker'

    # # defining data types of primitives as constant strings
    # IP_ACTION = 'ip action'
    # IP_ADDRESS = 'ip address'

    # # example of manually defining a tree
    # manualTree = GeneticTree(ATTACKER, IP_ACTION)
    # manualTree.root.func = hard_coded_range_if # basically a function pointer
    # manualTree.root.children = [Node(IP_ACTION), Node(IP_ACTION)]
    # manualTree.root.children[0].func = action0
    # manualTree.root.children[1].func = action1

    # context = {'ip address': '192.168.1.200', 'service': 'ssh'}
    # manualTree.execute(context)

    manualTargetIPAddress = "192.168.1.124"

    # Defined Context for testing leaf actions
    downloadFileSSH =  {"ip address": manualTargetIPAddress,
                        "service": SSH,
                        "port": 22,
                        "action": "transferFile",
                        "subaction":"downloadFile",
                        "localDirectory": "/home/spiegel/Capstone-Project-2022/downloads",
                        "remoteDirectory": "/home/spiegel/flags",
                        "fileName": "user1.txt",
                        "username": "spiegel",
                        "password": "1226"
                        }

    uloadFileSSH = {"ip address": manualTargetIPAddress,
                    "service": SSH,
                    "port": 22,
                    "action": "transferFile",
                    "subaction":"uploadFile",
                    "localDirectory": "/home/spiegel/Capstone-Project-2022/binaries",
                    "remoteDirectory": "/home/spiegel/flags",
                    "fileName": "virus.txt",
                    "username": "spiegel",
                    "password": "1226"
                    }

    uploadDirectorySSHSCP = {"ip address": manualTargetIPAddress,
                            "service": SSH,
                            "port": 22,
                            "action": "transferFile",
                            "subaction":"uploadDirectory",
                            "localDirectory": "/home/spiegel/Capstone-Project-2022/binaries",
                            "remoteDirectory": "/home/spiegel",
                            "fileName": "virus.txt",
                            "username": "spiegel",
                            "password": "1226"
                            }

    downloadDirectorySSHSCP =  {"ip address": manualTargetIPAddress,
                                "service": SSH,
                                "port": 22,
                                "action": "transferFile",
                                "subaction":"downloadDirectory",
                                "localDirectory": "/home/spiegel/Capstone-Project-2022/downloads",
                                "remoteDirectory": "/home/spiegel/Documents/secretPlans",
                                "fileName": "virus.txt",
                                "username": "spiegel",
                                "password": "1226"
                                }
    # See the geneticTree sftp primitive on how to use SFTP
    sftpDownloadFile =  {"ip address": manualTargetIPAddress,
                        "service": SFTP,
                        "port": 22,
                        "action": "transferFile",
                        "subaction":"downloadFile",
                        "localDirectory": "downloads/sftp",
                        "remoteDirectory": "flags",
                        "fileName": "user1.txt",
                        "username": "spiegel",
                        "password": "1226"
                        }

    sftpUploadFile =  {"ip address": manualTargetIPAddress,
                        "service": SFTP,
                        "port": 22,
                        "action": "transferFile",
                        "subaction":"uploadFile",
                        "localDirectory": "downloads/sftp",
                        "remoteDirectory": "flags",
                        "fileName": "testing.txt",
                        "username": "spiegel",
                        "password": "1226"
                        }

    replicate =    {"ip address": manualTargetIPAddress,
                    "service": "ssh",
                    "port": 22,
                    "action": "transferFile",
                    "subaction":"uploadDirectory",
                    "localDirectory": "/home/spiegel/Capstone-Project-2022/src",
                    "remoteDirectory": "/home/spiegel",
                    "fileName": "virus.txt",
                    "username": "spiegel",
                    "password": "1226"
                    }

    reconContext =  {"inform": "",
                    "ip address": manualTargetIPAddress,
                    "recon": NMAP,
                    "ipRange": "192.168.1.124/24",
                    "port": 22,
                    "action": SCANNETWORKSERVICES,
                    "subaction":"",
                    "localDirectory": "downloads/sftp",
                    "remoteDirectory": "flags",
                    "fileName": "testing.txt",
                    "username": "spiegel",
                    "password": "1226"
                    }

    replicateAgent = {"ip address": manualTargetIPAddress,
                            "service": SSH,
                            "port": 22,
                            "action": "transferFile",
                            "subaction":"uploadDirectory",
                            "localDirectory": "/home/spiegel/Capstone-Project-2022/src",
                            "remoteDirectory": "/home/spiegel",
                            "fileName": "virus.txt",
                            "username": "spiegel",
                            "password": "1226"
                            }

    unifiedContext = {  "action": BOB_TRANSFREFILE,
                        "subaction": BOB_SUBACTION,
                        "fileName": BOB_FILENAME
                        }
    unifiedContext2 = {  "action": ANDERSON_TRANSFREFILE,
                        "subaction": ANDERSON_SUBACTION,
                        "fileName": ANDERSON_FILENAME
                        }

    # Agent Bob
    # Bob is well Bob and requires a lot of help
    # you must provide a context and a Tree or bob
    # will not know what to do
    #print("\n\nAgent Bob")
    #AgentBob = SimpleAgent("Bob", unifiedContext, ATTACKER, BOB)
    #AgentBob.run()

    # # Agent Anderson
    # # Main goal: Find a target without knowing the IP address and download the flag
    print("\n\nAgent Anderson")
    AgentAnderson = SimpleAgent("Anderson", unifiedContext2, ATTACKER, ANDERSON)
    AgentAnderson.run()


    # # Agent Smith
    # # Main goal: Fing Targets with open SSH services and upload itself to the remote system
    # print("\n\nAgent Smith")
    # AgentSmith = SimpleAgent("Anderson", reconContext)
    # # We provide the range to scan on the network
    # AgentSmith.recon("24")
    # possibleTargets = AgentSmith.filterForService(SSH)
    # print("Targets with Service: ", possibleTargets)
    # # Loginto SSH services and stetal the flags from a known location
    # AgentSmith.replaceContext(replicateAgent)
    # AgentSmith.generateTree(ATTACKER, SERVICE, 4)
    # # Uploading Agent Replication to target
    # print("Copy Agent To target")
    # AgentSmith.attackTargets(possibleTargets)


