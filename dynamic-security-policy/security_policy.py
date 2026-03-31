import time
import logging
import subprocess
from datetime import datetime
from collections import defaultdict

# Configuration
SEUIL_TENTATIVES = 3
FENETRE_TEMPS = 60
DUREE_BAN = 300
LOG_SSH = "/var/log/auth.log"

# Configuration logs
logging.basicConfig(
    filename="security_events.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class SecurityPolicy:
    def __init__(self):
        self.tentatives = defaultdict(list)
        self.ip_bannies = {}

    def enregistrer_tentative(self, ip):
        maintenant = time.time()
        self.tentatives[ip].append(maintenant)

        self.tentatives[ip] = [
            t for t in self.tentatives[ip]
            if maintenant - t <= FENETRE_TEMPS
        ]

        nb = len(self.tentatives[ip])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"Tentative SSH depuis {ip} — {nb}/{SEUIL_TENTATIVES}")

        if nb >= SEUIL_TENTATIVES:
            self.bannir_ip(ip)

    def bannir_ip(self, ip):
        if ip in self.ip_bannies:
            return

        print(f"\n{'='*50}")
        print(f"!!! ALERTE — IP bannie : {ip}")
        print(f"!!! {SEUIL_TENTATIVES} tentatives en {FENETRE_TEMPS}s")
        print(f"{'='*50}\n")

        logging.warning(f"IP BANNIE : {ip}")

        try:
            subprocess.run(
                ["sudo", "iptables", "-A", "INPUT",
                 "-s", ip, "-j", "DROP"],
                capture_output=True
            )
            print(f"  iptables — IP {ip} bloquée !")
        except:
            print(f"  Erreur iptables")

        self.ip_bannies[ip] = time.time()
        self.tentatives[ip] = []

    def debannir_ip(self, ip):
        print(f"  IP {ip} débannie après {DUREE_BAN}s")
        logging.info(f"IP DEBANNIE : {ip}")
        try:
            subprocess.run(
                ["sudo", "iptables", "-D", "INPUT",
                 "-s", ip, "-j", "DROP"],
                capture_output=True
            )
        except:
            pass
        del self.ip_bannies[ip]

    def verifier_debannissement(self):
        maintenant = time.time()
        for ip, heure_ban in list(self.ip_bannies.items()):
            if maintenant - heure_ban >= DUREE_BAN:
                self.debannir_ip(ip)

    def afficher_statut(self):
        print(f"\n--- Statut ---")
        print(f"IPs surveillées : {len(self.tentatives)}")
        print(f"IPs bannies     : {len(self.ip_bannies)}")
        if self.ip_bannies:
            for ip in self.ip_bannies:
                print(f"  -> {ip} bannie")
        print(f"--------------\n")


# Programme principal
print("="*50)
print("  Politique Sécurité Dynamique — LAB REEL")
print(f"  Seuil    : {SEUIL_TENTATIVES} tentatives")
print(f"  Fenetre  : {FENETRE_TEMPS} secondes")
print(f"  Ban      : {DUREE_BAN} secondes")
print("="*50)
print("En surveillance des logs SSH...")
print("Historique ignoré — seulement nouveaux logs")
print("(Ctrl+C pour arrêter)\n")

policy = SecurityPolicy()

# Commencer à la fin du fichier — ignorer l'historique
try:
    with open(LOG_SSH, 'r') as f:
        derniere_position = len(f.readlines())
    print("En attente de nouvelles tentatives...\n")
except Exception as e:
    print(f"Erreur ouverture log : {e}")
    derniere_position = 0

try:
    while True:
        try:
            with open(LOG_SSH, 'r') as f:
                lignes = f.readlines()

            # Lire seulement les nouvelles lignes
            nouvelles = lignes[derniere_position:]
            derniere_position = len(lignes)

            for ligne in nouvelles:
                if "Failed password" in ligne:
                    parts = ligne.split("from ")
                    if len(parts) > 1:
                        ip = parts[1].split(" ")[0].strip()
                        policy.enregistrer_tentative(ip)

        except Exception as e:
            print(f"Erreur lecture log : {e}")

        policy.verifier_debannissement()
        time.sleep(2)

except KeyboardInterrupt:
    policy.afficher_statut()
    print("\nSurveillance arrêtée.")
