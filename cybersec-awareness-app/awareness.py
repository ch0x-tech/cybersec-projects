import time
import os

def effacer():
    os.system('clear')

def afficher_titre(texte):
    print(f"\n{'='*50}")
    print(f"  {texte}")
    print(f"{'='*50}\n")

# Base de données des quiz
QUIZ = [
    {
        "question": "Qu'est-ce qu'une attaque de phishing ?",
        "options": [
            "A. Un virus qui chiffre tes fichiers",
            "B. Un faux email qui vole tes identifiants",
            "C. Une attaque sur le réseau Wi-Fi",
            "D. Un logiciel espion"
        ],
        "reponse": "B",
        "explication": "Le phishing est une technique qui utilise de faux emails ou sites web pour voler les identifiants des utilisateurs."
    },
    {
        "question": "Quel mot de passe est le plus sécurisé ?",
        "options": [
            "A. password123",
            "B. MonNom1990",
            "C. X#9kL@2mP!qR",
            "D. azerty"
        ],
        "reponse": "C",
        "explication": "Un bon mot de passe doit avoir majuscules, chiffres, symboles et être long. X#9kL@2mP!qR coche toutes ces cases."
    },
    {
        "question": "Qu'est-ce que le 2FA ?",
        "options": [
            "A. Un antivirus",
            "B. Une double authentification",
            "C. Un pare-feu",
            "D. Un VPN"
        ],
        "reponse": "B",
        "explication": "2FA (Two-Factor Authentication) ajoute une deuxième couche de sécurité en plus du mot de passe — comme un code SMS."
    },
    {
        "question": "Tu reçois un email urgent de ta banque demandant ton mot de passe. Que fais-tu ?",
        "options": [
            "A. Tu réponds avec ton mot de passe",
            "B. Tu cliques sur le lien dans l'email",
            "C. Tu ignores et appelles ta banque directement",
            "D. Tu transfères l'email à tes amis"
        ],
        "reponse": "C",
        "explication": "Les banques ne demandent JAMAIS ton mot de passe par email. Toujours contacter directement ta banque par téléphone."
    },
    {
        "question": "Qu'est-ce qu'un ransomware ?",
        "options": [
            "A. Un logiciel qui surveille ton écran",
            "B. Un virus qui chiffre tes fichiers et demande une rançon",
            "C. Un programme qui vole tes contacts",
            "D. Un faux antivirus"
        ],
        "reponse": "B",
        "explication": "Un ransomware chiffre tous tes fichiers et demande une rançon pour les récupérer. WannaCry en 2017 a infecté 200 000 ordinateurs."
    },
    {
        "question": "Quel réseau Wi-Fi est le plus sûr pour travailler ?",
        "options": [
            "A. Wi-Fi public gratuit au café",
            "B. Wi-Fi de l'hôtel",
            "C. Ton réseau personnel avec WPA3",
            "D. Wi-Fi ouvert sans mot de passe"
        ],
        "reponse": "C",
        "explication": "Ton réseau personnel avec WPA3 est le plus sécurisé. Les Wi-Fi publics peuvent être surveillés par des hackers."
    },
    {
        "question": "Qu'est-ce qu'un VPN ?",
        "options": [
            "A. Un antivirus",
            "B. Un réseau privé virtuel qui chiffre ta connexion",
            "C. Un gestionnaire de mots de passe",
            "D. Un pare-feu"
        ],
        "reponse": "B",
        "explication": "Un VPN chiffre ta connexion internet et cache ton adresse IP. Très utile sur les Wi-Fi publics."
    },
    {
        "question": "Comment reconnaître un site web sécurisé ?",
        "options": [
            "A. Il a une belle interface",
            "B. Il commence par https:// avec un cadenas",
            "C. Il charge rapidement",
            "D. Il a beaucoup de visiteurs"
        ],
        "reponse": "B",
        "explication": "HTTPS et le cadenas vert indiquent que la connexion est chiffrée. HTTP sans S = données en clair = dangereux !"
    },
    {
        "question": "Qu'est-ce que l'ingénierie sociale ?",
        "options": [
            "A. Programmer des robots",
            "B. Construire des réseaux",
            "C. Manipuler les personnes pour obtenir des informations",
            "D. Développer des applications"
        ],
        "reponse": "C",
        "explication": "L'ingénierie sociale exploite la psychologie humaine pour obtenir des informations confidentielles sans hacker les systèmes."
    },
    {
        "question": "Quelle est la meilleure pratique pour les mises à jour ?",
        "options": [
            "A. Les ignorer — ça ralentit l'ordinateur",
            "B. Les faire une fois par an",
            "C. Les installer dès qu'elles sont disponibles",
            "D. Les désactiver complètement"
        ],
        "reponse": "C",
        "explication": "Les mises à jour corrigent des failles de sécurité. Ne pas les installer laisse ton système vulnérable aux attaques."
    }
]

# Scénarios éducatifs
SCENARIOS = [
    {
        "titre": "L'email suspect",
        "histoire": """
Tu reçois cet email :

De : support@g00gle.com
Objet : URGENT - Votre compte sera suspendu !

'Cliquez ici pour vérifier votre compte
immédiatement sinon il sera supprimé dans 24h'
        """,
        "question": "Que remarques-tu de suspect ?",
        "indices": [
            "1. L'adresse email : g00gle.com (deux zéros) pas google.com",
            "2. Le ton urgent — les hackers créent la panique",
            "3. Demande de cliquer sur un lien",
            "4. Menace de suppression du compte"
        ],
        "lecon": "Toujours vérifier l'adresse email exacte de l'expéditeur !"
    },
    {
        "titre": "Le mot de passe faible",
        "histoire": """
Ton ami utilise ces mots de passe :
- Facebook  : azerty123
- Gmail     : azerty123
- Banque    : azerty123

Il pense que c'est facile à retenir.
        """,
        "question": "Quels sont les problèmes ?",
        "indices": [
            "1. Même mot de passe partout — si un compte est piraté tous le sont",
            "2. azerty123 est dans les 100 mots de passe les plus utilisés",
            "3. Pas de majuscules ni de symboles",
            "4. Solution : gestionnaire de mots de passe"
        ],
        "lecon": "Un mot de passe unique et fort pour chaque compte !"
    },
    {
        "titre": "Le Wi-Fi public",
        "histoire": """
Tu es dans un café et tu vois deux réseaux Wi-Fi :
- CafeWifi_Free (ouvert, pas de mot de passe)
- CafeWifi_Secure (mot de passe requis)

Tu te connectes au réseau gratuit pour travailler
sur des documents confidentiels de ton entreprise.
        """,
        "question": "Qu'est-ce qui peut mal se passer ?",
        "indices": [
            "1. Le réseau ouvert peut être un faux point d'accès hacker",
            "2. Tes données transitent en clair — lisibles par tous",
            "3. Un hacker peut intercepter tes documents confidentiels",
            "4. Solution : utiliser un VPN sur Wi-Fi public"
        ],
        "lecon": "Ne jamais envoyer des données sensibles sur Wi-Fi public sans VPN !"
    }
]

def jouer_quiz():
    effacer()
    afficher_titre("QUIZ CYBERSÉCURITÉ")
    score = 0
    total = len(QUIZ)

    for i, q in enumerate(QUIZ):
        print(f"Question {i+1}/{total}")
        print(f"\n{q['question']}\n")
        for option in q['options']:
            print(f"  {option}")

        reponse = input("\nTa réponse (A/B/C/D) : ").upper().strip()

        if reponse == q['reponse']:
            print(f"\n  CORRECT ! +1 point")
            score += 1
        else:
            print(f"\n  INCORRECT ! La bonne réponse était : {q['reponse']}")

        print(f"  {q['explication']}")
        print(f"\n  Score actuel : {score}/{i+1}")
        input("\n  Appuie sur Entrée pour continuer...")
        effacer()

    # Résultat final
    afficher_titre("RÉSULTAT FINAL")
    pourcentage = (score / total) * 100
    print(f"  Score : {score}/{total} ({pourcentage:.0f}%)\n")

    if pourcentage >= 80:
        print("  EXCELLENT ! Tu maîtrises bien la cybersécurité !")
    elif pourcentage >= 60:
        print("  BIEN ! Mais tu peux encore t'améliorer.")
    elif pourcentage >= 40:
        print("  MOYEN. Relis les explications et réessaie.")
    else:
        print("  FAIBLE. Tu as besoin de plus de formation !")

    # Sauvegarder le score
    from datetime import datetime
    heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('scores.txt', 'a') as f:
        f.write(f"[{heure}] Score: {score}/{total} ({pourcentage:.0f}%)\n")

    print(f"\n  Score sauvegardé dans scores.txt")

def jouer_scenario():
    effacer()
    afficher_titre("SCÉNARIOS DE SÉCURITÉ")

    for i, s in enumerate(SCENARIOS):
        print(f"Scénario {i+1}/{len(SCENARIOS)} — {s['titre']}")
        print(s['histoire'])
        print(f"Question : {s['question']}")
        input("\nAppuie sur Entrée pour voir les indices...")

        print("\nIndices :")
        for indice in s['indices']:
            print(f"  {indice}")
            time.sleep(0.5)

        print(f"\nLeçon : {s['lecon']}")
        input("\nAppuie sur Entrée pour continuer...")
        effacer()

    print("Tous les scénarios terminés ! Tu es plus vigilant maintenant.")

# Menu principal
while True:
    effacer()
    afficher_titre("App Sensibilisation Cybersécurité")
    print("  1. Quiz cybersécurité (10 questions)")
    print("  2. Scénarios éducatifs (3 scénarios)")
    print("  3. Voir mes scores")
    print("  4. Quitter")

    choix = input("\nTon choix : ")

    if choix == "1":
        jouer_quiz()
    elif choix == "2":
        jouer_scenario()
    elif choix == "3":
        effacer()
        afficher_titre("MES SCORES")
        try:
            with open('scores.txt', 'r') as f:
                print(f.read())
        except:
            print("  Pas encore de scores !")
        input("\nAppuie sur Entrée pour continuer...")
    elif choix == "4":
        print("\n  Au revoir et reste vigilant !")
        break
    else:
        print("  Choix invalide !")
        time.sleep(1)
