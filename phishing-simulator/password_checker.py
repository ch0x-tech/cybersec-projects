import re

def verifier_mot_de_passe(mdp):
    score = 0
    conseils = []

    if len(mdp) >= 8:
        score += 1
    else:
        conseils.append("Ajoute au moins 8 caracteres")

    if re.search(r'[A-Z]', mdp):
        score += 1
    else:
        conseils.append("Ajoute au moins une majuscule")

    if re.search(r'[0-9]', mdp):
        score += 1
    else:
        conseils.append("Ajoute au moins un chiffre")

    if re.search(r'[!@#$%^&*(),.?]', mdp):
        score += 1
    else:
        conseils.append("Ajoute un symbole comme ! @ # $")

    if len(set(mdp)) > 6:
        score += 1
    else:
        conseils.append("Varie plus tes caracteres")

    if score <= 2:
        niveau = "FAIBLE"
        couleur = "\033[91m"
    elif score == 3:
        niveau = "MOYEN"
        couleur = "\033[93m"
    else:
        niveau = "FORT"
        couleur = "\033[92m"

    reset = "\033[0m"
    barre = "█" * score + "░" * (5 - score)

    return score, niveau, couleur, barre, reset, conseils


# --- Programme principal ---
print("=== Verificateur de mot de passe ===")
print("(tape 'quitter' pour arreter)\n")

while True:
    mdp = input("Entre un mot de passe : ")

    if mdp.lower() == "quitter":
        print("Au revoir !")
        break

    score, niveau, couleur, barre, reset, conseils = verifier_mot_de_passe(mdp)

    print(f"\nForce : [{barre}] {score}/5")
    print(f"Niveau : {couleur}{niveau}{reset}")

    if conseils:
        print("\nConseils :")
        for c in conseils:
            print(f"  -> {c}")
    print()
