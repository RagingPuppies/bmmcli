import json

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def validateCluster(active_cluster, config):
    try:
        config[active_cluster]
    except:
        print(f"{bcolors.FAIL}Cluster wasn't found in bmm_config file, please choose cluster from the list or add a cluster to bmm_config file:{bcolors.ENDC}")
        for cluster in config:
            print(cluster)
        exit(1)

def csv_to_list(string):
    return string.split(",")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pretty(json_data, indent=0):
    jsonify = json_data.json()
    dest = (jsonify['destination']['connectionString']).split("/")[2].split(":")[0]
    src = (jsonify['source']['connectionString']).split("/")[2].split(":")[0]
    s = jsonify["source"]["connectionString"]
    topics = (s[s.find("(")+1:s.find(")")]).split("|")
    print(f"{bcolors.OKCYAN}Name: {jsonify['name']}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}Status: {jsonify['Status']}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}From: {src}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}To: {dest}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}Topics:{bcolors.ENDC}")
    for topic in topics:
        print(f"{bcolors.OKCYAN}  - {topic}{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}Metadata:{bcolors.ENDC}")
    for k, v in jsonify["metadata"].items():
        print(f"{bcolors.OKCYAN}    {k}: {v} {bcolors.ENDC}")
    print("")