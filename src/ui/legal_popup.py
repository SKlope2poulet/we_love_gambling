import tkinter as tk

class LegalPopup:
    """Fenêtre d'affichage des CGU et de la politique de confidentialité."""

    def __init__(self, parent):
        self.parent = parent

    def show_popup(self):
        """Affiche une fenêtre avec les CGU et la politique de confidentialité."""
        popup = tk.Toplevel(self.parent)
        popup.title("📜 CGU & Politique de confidentialité")
        popup.geometry("500x400")
        popup.configure(bg="#f5f5f5")

        text = (
            "🔒 Conditions Générales d’Utilisation (CGU)\n\n"
            "Ce site est un simulateur de jeux utilisant uniquement de l’argent fictif.\n"
            "Aucune transaction réelle n’est effectuée. Les gains et pertes n’ont aucune valeur monétaire.\n\n"
            "🛡️ Politique de confidentialité\n\n"
            "Les données saisies (comme votre pseudo ou votre âge) ne sont ni enregistrées ni partagées.\n"
            "Ce site respecte votre anonymat complet.\n\n"
            "© We Love Gambling - Tous droits réservés."
        )

        tk.Label(
            popup,
            text=text,
            wraplength=450,
            justify="left",
            bg="#f5f5f5",
            fg="#111",
            font=("Arial", 11)
        ).pack(expand=True, fill="both", padx=20, pady=20)

        tk.Button(
            popup,
            text="Fermer",
            bg="#28a745",
            fg="white",
            width=20,
            command=popup.destroy
        ).pack(pady=10)
