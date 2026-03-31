import socket
import requests
import ipaddress
from datetime import datetime

# Ports IoT communs
PORTS_IOT = {
    80:   "HTTP",
    443:  "HTTPS",
    22:   "SSH",
    23:   "Telnet",
    1883: "MQTT",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    554:  "RTSP-Camera"
}

# Mots de passe par défaut IoT
CREDENTIALS_DEFAUT = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "1234"),
    ("root", "root"),
    ("root", "toor"),
    ("user", "user"),
    ("guest", "guest"),
    ("admin", ""),
]

def afficher_titre(texte):
    print(f"\n{'='*50}")
    print(f"  {texte}")
    print(f"{'='*50}")

def scanner_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultat = sock.connect_ex((str(ip), port))
        sock.close()
        return resultat == 0
    except:
        return False

def verifier_credentials(ip, port):
    vulnerable = []
    for user, password in CREDENTIALS_DEFAUT:
        try:
            url = f"http://{ip}:{port}"
            response = requests.get(
                url,
                auth=(user, password),
                timeout=2
            )
            if response.status_code == 200:
                vulnerable.append((user, password))
        except:
            pass
    return vulnerable

def scanner_appareil(ip):
    ports_ouverts = []
    for port, service in PORTS_IOT.items():
        if scanner_port(ip, port):
            ports_ouverts.append((port, service))
    return ports_ouverts

def scanner_reseau(reseau):
    afficher_titre(f"Scan du réseau : {reseau}")
    appareils = []

    try:
        network = ipaddress.IPv4Network(reseau, strict=False)
        total = sum(1 for _ in network.hosts())
        print(f"  Scan de {total} adresses IP...")
        print(f"  Patience — cela peut prendre quelques minutes\n")

        for i, ip in enumerate(network.hosts()):
            if scanner_port(ip, 80, timeout=0.5) or \
               scanner_port(ip, 22, timeout=0.5) or \
               scanner_port(ip, 23, timeout=0.5):
                print(f"  [TROUVE] Appareil actif : {ip}")
                appareils.append(str(ip))

    except Exception as e:
        print(f"  Erreur : {e}")

    return appareils

def analyser_appareil(ip):
    afficher_titre(f"Analyse de {ip}")
    resultats = {
        'ip': ip,
        'ports': [],
        'vulnerable': [],
        'risque': 'FAIBLE'
    }

    # Scanner les ports
    print(f"  Scan des ports IoT...")
    ports = scanner_appareil(ip)

    if ports:
        print(f"  Ports ouverts :")
        for port, service in ports:
            print(f"    -> Port {port} ({service}) ouvert")
            resultats['ports'].append((port, service))

            # Vérifier Telnet — très dangereux
            if port == 23:
                print(f"    !!! DANGER : Telnet activé — pas de chiffrement !")
                resultats['risque'] = 'CRITIQUE'

        # Vérifier credentials sur HTTP
        print(f"\n  Vérification mots de passe par défaut...")
        for port, service in ports:
            if service in ['HTTP', 'HTTP-Alt']:
                creds = verifier_credentials(ip, port)
                if creds:
                    for user, pwd in creds:
                        print(f"    !!! VULNERABLE : {user}/{pwd} fonctionne !")
                        resultats['vulnerable'].append((user, pwd))
                        resultats['risque'] = 'CRITIQUE'

        if not resultats['vulnerable']:
            print(f"  Mots de passe par défaut : OK")

    else:
        print(f"  Aucun port IoT ouvert détecté")

    return resultats

def generer_rapport(resultats_liste):
    afficher_titre("RAPPORT FINAL")
    heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rapport = f"\n{'='*50}\n"
    rapport += f"IoT Security Report — {heure}\n"
    rapport += f"{'='*50}\n"

    critiques = 0
    for r in resultats_liste:
        rapport += f"\nIP : {r['ip']}\n"
        rapport += f"Risque : {r['risque']}\n"
        rapport += f"Ports ouverts : {len(r['ports'])}\n"

        for port, service in r['ports']:
            rapport += f"  -> {port} ({service})\n"

        if r['vulnerable']:
            rapport += f"Credentials vulnérables :\n"
            for user, pwd in r['vulnerable']:
                rapport += f"  -> {user}/{pwd}\n"
            critiques += 1

    rapport += f"\n{'='*50}\n"
    rapport += f"Total appareils scannés : {len(resultats_liste)}\n"
    rapport += f"Appareils critiques     : {critiques}\n"

    print(rapport)

    with open('iot_rapport.txt', 'a') as f:
        f.write(rapport)
    print(f"  Rapport sauvegardé dans iot_rapport.txt")

# Programme principal
print("="*50)
print("  IoT Security Survey Tool — Projet 9")
print("  USAGE EDUCATIF UNIQUEMENT !")
print("="*50)
print("\n1. Scanner un réseau complet")
print("2. Analyser une seule IP")
choix = input("\nTon choix (1 ou 2) : ")

resultats = []

if choix == "1":
    reseau = input("Entre le réseau (ex: 192.168.1.0/24) : ")
    appareils = scanner_reseau(reseau)
    if appareils:
        for ip in appareils:
            r = analyser_appareil(ip)
            resultats.append(r)
    else:
        print("\n  Aucun appareil trouvé sur ce réseau")

elif choix == "2":
    ip = input("Entre l'adresse IP : ")
    r = analyser_appareil(ip)
    resultats.append(r)

if resultats:
    generer_rapport(resultats)
