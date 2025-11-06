import tkinter as tk
from tkinter import messagebox

class AgeVerification(tk.Toplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.title("Vérification d'âge")
        self.geometry("400x200")
        self.config(bg="#2e2e2e")
        self.resizable(False, False)
        self.on_confirm = on_confirm

        tk.Label(
            self,
            text="Avez-vous plus de 18 ans ?",
            font=("Arial", 14),
            bg="#2e2e2e",
            fg="white"
        ).pack(pady=20)

        btn_frame = tk.Frame(self, bg="#2e2e2e")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Oui", width=10, bg="green", fg="white",
            command=self.confirm_age
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="Non", width=10, bg="red", fg="white",
            command=self.deny_age
        ).pack(side="left", padx=10)

    def confirm_age(self):
        """Si l'utilisateur est majeur : fermer et lancer l'app."""
        self.destroy()
        if callable(self.on_confirm):
            self.on_confirm()

    def deny_age(self):
        """Si l'utilisateur n'est pas majeur : message et fermeture."""
        messagebox.showwarning(
            "Accès refusé",
            "Désolé, vous devez être majeur pour accéder au site."
        )
        self.destroy()
        self.master.destroy()
