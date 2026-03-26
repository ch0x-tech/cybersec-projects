from PIL import Image
import random
import os

def creer_image_texte(texte, largeur=400, hauteur=200):
    img = Image.new('RGB', (largeur, hauteur), color='white')
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    draw.text((largeur//4, hauteur//3), texte,
              fill='black')
    return img

def chiffrer(image_path=None, texte=None):
    if texte:
        secret = creer_image_texte(texte)
    else:
        secret = Image.open(image_path).convert('RGB')

    largeur, hauteur = secret.size
    share1 = Image.new('RGB', (largeur, hauteur))
    share2 = Image.new('RGB', (largeur, hauteur))

    pixels_secret = secret.load()
    pixels_s1 = share1.load()
    pixels_s2 = share2.load()

    for x in range(largeur):
        for y in range(hauteur):
            r, g, b = pixels_secret[x, y]

            # Créer pixel aléatoire pour share1
            r1 = random.randint(0, 255)
            g1 = random.randint(0, 255)
            b1 = random.randint(0, 255)

            # share2 = XOR entre secret et share1
            r2 = r ^ r1
            g2 = g ^ g1
            b2 = b ^ b1

            pixels_s1[x, y] = (r1, g1, b1)
            pixels_s2[x, y] = (r2, g2, b2)

    share1.save('share1.png')
    share2.save('share2.png')
    print("Chiffrement termine !")
    print("share1.png et share2.png créés")

def dechiffrer():
    s1 = Image.open('share1.png').convert('RGB')
    s2 = Image.open('share2.png').convert('RGB')

    largeur, hauteur = s1.size
    reveal = Image.new('RGB', (largeur, hauteur))

    pixels_s1 = s1.load()
    pixels_s2 = s2.load()
    pixels_reveal = reveal.load()

    for x in range(largeur):
        for y in range(hauteur):
            r1, g1, b1 = pixels_s1[x, y]
            r2, g2, b2 = pixels_s2[x, y]

            # XOR pour révéler le secret
            pixels_reveal[x, y] = (r1^r2, g1^g2, b1^b2)

    reveal.save('reveal.png')
    print("Déchiffrement terminé !")
    print("reveal.png créé — ouvre ce fichier !")

# Menu principal
print("=== Cryptographie Visuelle ===")
print("1. Chiffrer un texte secret")
print("2. Déchiffrer (révéler le secret)")
choix = input("\nTon choix (1 ou 2) : ")

if choix == "1":
    texte = input("Entre ton message secret : ")
    chiffrer(texte=texte)
elif choix == "2":
    dechiffrer()
else:
    print("Choix invalide")
