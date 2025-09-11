import fastf1
from matplotlib import pyplot as plt


# Active le cache FastF1
fastf1.Cache.enable_cache('cache')

# Fonction pour choisir le GP
def choisir_gp():
    while True:
        try:
            annee = int(input("Entrez l'année du GP (ex: 2025) : "))
            gp_nom = input("Entrez le nom du GP (ex: Monza, Silverstone) : ").strip()
            session_type = input("Type de session (R = Course, Q = Qualif, FP1 = Essais) : ").strip().upper()
            # Vérification des entrées
            if session_type not in ['R', 'Q', 'FP1', 'FP2', 'FP3']:
                raise ValueError("Type de session invalide")
            return annee, gp_nom, session_type
        except ValueError as e:
            print(f"Erreur : {e}. Réessayez.")

# Fonction pour choisir les pilotes
def choisir_pilotes():
    while True:
        pilote1 = input("Entrez le numéro du pilote 1 (ex: VER, LEC) : ").strip().upper()
        pilote2 = input("Entrez le numéro du pilote 2 (ex: VER, LEC) : ").strip().upper()
        if pilote1 == pilote2:
            print("Veuillez choisir deux pilotes différents.")
            continue
        return pilote1, pilote2

# Récupération choix utilisateur
annee, gp_nom, session_type = choisir_gp()
pilote1, pilote2 = choisir_pilotes()

# Charger la session FastF1 avec gestion des erreurs
try:
    print(f"Chargement des données pour {gp_nom} {annee} - {session_type}...")
    session = fastf1.get_session(annee, gp_nom, session_type)
    session.load()
except Exception as e:
    print(f"Erreur lors du chargement de la session : {e}")
    exit(1)

# Vérifier si les pilotes existent
drivers = session.drivers
if pilote1 not in drivers or pilote2 not in drivers:
    print(f"Un ou les deux pilotes choisis ne sont pas présents durant cette session, voici la liste des pilotes qui étaient présents: {drivers}")
    exit(1)

# Récupérer les meilleurs tours (récupère tout les tours du pilote et sélectionne le meilleur)
laps1 = session.laps.pick_driver(pilote1)
laps2 = session.laps.pick_driver(pilote2)

best1 = laps1.pick_fastest()
best2 = laps2.pick_fastest()

# Vérifier que les tours existent
if best1 is None or best2 is None:
    print("Aucun tour valide trouvé pour un des pilotes.")
    exit(1)

# Télémétrie
tel1 = best1.get_car_data().add_distance()
tel2 = best2.get_car_data().add_distance()

# Plot vitesse
plt.figure(figsize=(10, 5))
plt.plot(tel1['Distance'], tel1['Speed'], label=pilote1)
plt.plot(tel2['Distance'], tel2['Speed'], label=pilote2)
plt.xlabel('Distance (m)')
plt.ylabel('Vitesse (km/h)')
plt.title(f'Comparaison vitesse {pilote1} vs {pilote2} - {gp_nom} {annee} {session_type}')
plt.legend()
plt.show()

# Afficher les meilleurs temps
print(f"{pilote1} meilleur tour : {best1['LapTime']}")
print(f"{pilote2} meilleur tour : {best2['LapTime']}")
