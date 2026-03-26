import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Configuration
DOSSIER_SURVEILLE = "./honeypot"
SEUIL_ALERTE = 3
FENETRE_TEMPS = 10

# Configuration du log
logging.basicConfig(
    filename="alerts.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

class DetecteurRansomware(FileSystemEventHandler):
    def __init__(self):
        self.evenements = []
        self.fichiers_touches = []

    def analyser(self, type_event, chemin):
        maintenant = time.time()
        self.evenements.append(maintenant)
        self.fichiers_touches.append(f"{type_event}:{chemin}")

        # Garder seulement les evenements dans la fenetre de temps
        combined = list(zip(self.evenements, self.fichiers_touches))
        combined = [(e, f) for e, f in combined
                   if maintenant - e <= FENETRE_TEMPS]

        if combined:
            self.evenements, self.fichiers_touches = zip(*combined)
            self.evenements = list(self.evenements)
            self.fichiers_touches = list(self.fichiers_touches)
        else:
            self.evenements = []
            self.fichiers_touches = []

        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"{type_event} detecte : {chemin}")

        # Verifier si le seuil est atteint
        if len(self.evenements) >= SEUIL_ALERTE:
            self.alerte()

    def alerte(self):
        print(f"\n{'='*50}")
        print(f"!!! ALERTE RANSOMWARE !!!")
        print(f"{len(self.evenements)} modifications en {FENETRE_TEMPS}s")
        print(f"\nFichiers touches :")
        for f in self.fichiers_touches:
            type_ev, chemin = f.split(":", 1)
            print(f"  -> [{type_ev}] {chemin}")
        print(f"{'='*50}\n")

        # Sauvegarder dans le log
        fichiers_str = " | ".join(self.fichiers_touches)
        message = (f"ALERTE RANSOMWARE ! "
                  f"{len(self.evenements)} modifications en "
                  f"{FENETRE_TEMPS}s | Fichiers: {fichiers_str}")
        logging.warning(message)

        # Reset apres alerte
        self.evenements = []
        self.fichiers_touches = []

    def on_modified(self, event):
        if not event.is_directory:
            self.analyser("MODIFICATION", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.analyser("CREATION", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.analyser("SUPPRESSION", event.src_path)


# Lancement
print("="*50)
print("  Detecteur de Ransomware - Projet 12")
print(f"  Surveillance : {DOSSIER_SURVEILLE}")
print(f"  Seuil alerte : {SEUIL_ALERTE} changements")
print(f"  Fenetre temps : {FENETRE_TEMPS} secondes")
print("="*50)
print("En attente d'activite suspecte...")
print("(Ctrl+C pour arreter)\n")

detecteur = DetecteurRansomware()
observer = Observer()
observer.schedule(detecteur, DOSSIER_SURVEILLE, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("\nSurveillance arretee.")

observer.join()
