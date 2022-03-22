import os,json
from time import gmtime, strftime, sleep

#Configuer au prealable la commande cli aws avec votre API SECRET KEY et aussi la region souhaité

FILE_CREATION_IP = "ip.json"
GOOD_FILE = 'good.log'
BAD_FILE = 'bad.log'
API_TELEGRAM_API_KEY = ""

#OBLIGATOIRE Fichier contenant les IPs à prendre en otage
IP_LIST = 'list.ip'

#Valeur int renvoyé si la commande exécuté avec succès
REP_GOOD = 0


def logger(e,l=BAD_FILE):
    with open(l,'a') as f:
        t = strftime("%a, %d %b %Y %H:%M:%S ", gmtime())
        error = t+"->> "+e+"\n"
        f.write(error)

def notification(notif):
    try:
        os.system('curl -s -X POST https://api.telegram.org/'+API_TELEGRAM_API_KEY+'/sendMessage -d chat_id=1746121134 -d text="'+notif+'"')
    except Exception as e:
        logger("Notification BUG : "+e)

def createEIP():
    try:
        cmd = "aws ec2 allocate-address --output json > "+FILE_CREATION_IP
        c = os.system(cmd)

        if c == REP_GOOD:
            with open(FILE_CREATION_IP,"r") as f:
                elasticIp = f.read()
                elasticIp = json.loads(elasticIp)

            print(str(elasticIp["AllocationId"]))
            return elasticIp["PublicIp"]
        else:
            message = "Impossible de creer l'addresse IP code erreur : "+c
            notification(message)
            return False

    except Exception as e:
        logger("createEIP BUG : "+str(e))


def deleteEIP(AllocationId):
    try:
        cmd = "aws ec2 release-address --allocation-id "+AllocationId
        c = os.system(cmd)
        if c==REP_GOOD:
            print("delete ip for allocation ID : "+AllocationId)
        return c

    except Exception as e:
        logger("DeleteEIP BUG : "+e)


def verifcation(eIp,IP_LIST):

    try:
        cmd = "grep "+eIp+" "+IP_LIST
        c = os.system(cmd)
        if c==REP_GOOD:
            message = "Bravo ! patron je viens de prendre en otage l'adresse : "+eIp+" en otage."
            notification(message)
            logger(eIp,GOOD_FILE)
        else:
            return False
    except Exception as e:
        logger("Verification BUG : "+e)


def main():
    counter = 0

main()
