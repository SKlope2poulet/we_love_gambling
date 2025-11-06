#!/bin/bash
set -e

# Nom de la branche principale et de dev
MAIN_BRANCH="main"
DEV_BRANCH="dev"

# Crée et pousse la branche main si elle n'existe pas
if ! git show-ref --verify --quiet refs/heads/$MAIN_BRANCH; then
  git checkout -b $MAIN_BRANCH
  git push -u origin $MAIN_BRANCH
else
  git checkout $MAIN_BRANCH
  git pull origin $MAIN_BRANCH
fi

# Crée et pousse la branche dev si elle n'existe pas
if ! git show-ref --verify --quiet refs/heads/$DEV_BRANCH; then
  git checkout -b $DEV_BRANCH
  git push -u origin $DEV_BRANCH
else
  git checkout $DEV_BRANCH
  git pull origin $DEV_BRANCH
fi

# Liste de toutes les user stories
stories=(
  "Inscription_Connexion_solde"
  "Gestion_portefeuille"
  "Dashboard_KPI"
  "Verification_majorite"
  "Avertissement_argent_fictif"
  "Consultation_CGU_confidentialite"
  "UI_navigation_claire"
  "Bouton_recharger_solde"
  "Page_accueil_liste_jeux"
  "Barre_navigation_fixe"
  "Regles_jeu_page"
  "Acces_plusieurs_jeux"
  "Jackpot_temps_reel"
  "Chargement_rapide"
  "Interface_jeu_de_table"
  "Blackjack_mise"
  "Blackjack_multihand"
  "Blackjack_split"
  "Blackjack_double"
  "Blackjack_carte_cachee"
  "Blackjack_stand"
  "Blackjack_hit"
  "Blackjack_autoplay"
  "SlotMachine_mise"
  "SlotMachine_spin"
  "SlotMachine_autoplay"
  "SlotMachine_recapitulatif"
  "ChickenRoad_avancer"
  "ChickenRoad_difficulte"
  "ChickenRoad_mise"
  "ChickenRoad_cashout"
  "ChickenRoad_voir_perte"
  "ChickenRoad_case_perdante"
  "Alerte_solde_bas"
  "Jeu_responsable_information"
  "Admin_validation_comptes"
  "Admin_fraude_journaux"
  "Admin_promotions"
  "Admin_configuration"
  "Admin_rapports"
  "Palette_Blackjack"
  "Palette_Plinko"
  "Palette_MinesTiles"
  "Palette_ChickenRoad"
  "Palette_SlotMachine"
  "Palette_Roulette"
  "Palette_PenaltyShootout"
  "MinesTiles_taille_grille"
  "MinesTiles_nombre_bombes"
  "MinesTiles_multiplicateur"
  "Roulette_table_mise"
  "Roulette_strategie"
  "Roulette_roue_dynamique"
  "Roulette_gain_potentiel"
  "Plinko_niveau_risque"
  "Plinko_physique_realiste"
)

# Création des branches depuis dev
for story in "${stories[@]}"; do
  branch="feature/${story}"
  echo "➡️  Création de la branche $branch"
  git checkout $DEV_BRANCH
  git branch "$branch"
  git push -u origin "$branch"
done

echo "✅ Toutes les branches ont été créées et poussées sur GitHub."
