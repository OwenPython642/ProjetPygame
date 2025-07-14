import os
import sys

# === Config utilisateur ===
fichier_principal = r"pygame/main.py"  # Script à compiler
dossier_assets = r"pygame/assets"  # Racine des assets (avec sous-dossiers inclus)

# === Détection du séparateur en fonction du système ===
separateur = ";" if sys.platform == "win32" else ":"

# === Construction de la commande ===
commandes = ["pyinstaller", "--onefile", "--noconsole"]

# Ajout des fichiers dans le dossier d'assets (récursif)
for racine, _, fichiers in os.walk(dossier_assets):
    for fichier in fichiers:
        chemin_source = os.path.join(racine, fichier)
        chemin_relatif = os.path.relpath(chemin_source, ".")
        dossier_destination = os.path.dirname(chemin_relatif)
        argument = f'--add-data "{chemin_relatif}{separateur}{dossier_destination}"'
        commandes.append(argument)

# Ajout du script principal
commandes.append(fichier_principal)

# Affichage de la commande finale
commande_finale = " ".join(commandes)
print("\nCommande PyInstaller à utiliser :\n")
print(commande_finale)
