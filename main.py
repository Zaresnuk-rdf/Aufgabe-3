import tkinter as tk

# GUI erstellen
fenster = tk.Tk()
fenster.title("Kundenabfrage nach Alter")

tk.Label(fenster, text="Alter eingeben:").pack(pady=5)
alter_entry = tk.Entry(fenster)
alter_entry.pack(pady=5)
tk.Button(fenster, text="Kunden suchen").pack(pady=5)
ausgabe_text = tk.Text(fenster, height=15, width=50)
ausgabe_text.pack(pady=5)

fenster.mainloop()

import mariadb
import sys

# Datenbankverbindung herstellen
try:
    conn = mariadb.connect(
        user="dein_benutzername",
        password="dein_passwort",
        host="localhost",
        port=3306,
        database="deine_datenbank"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    print(f"Fehler beim Verbinden mit MariaDB: {e}")
    sys.exit(1)

from datetime import date
from tkinter import messagebox

# Funktion zur Kundenabfrage
def kunden_abfragen():
    try:
        alter = int(alter_entry.get())
    except ValueError:
        messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben!")
        return

    heute = date.today()
    stichtag = date(heute.year - alter, heute.month, heute.day)

    try:
        cur.execute(
            "SELECT Anrede, Vorname, Name, Telefon FROM kunden WHERE Geburtsdatum > ?",
            (stichtag,)
        )
        kunden = cur.fetchall()

        ausgabe_text.delete("1.0", tk.END)
        if not kunden:
            ausgabe_text.insert(tk.END, f"Keine Kunden unter {alter} Jahren gefunden.")
        else:
            for anrede, vorname, nachname, telefon in kunden:
                ausgabe_text.insert(tk.END, f"{anrede} {vorname} {nachname} - Tel: {telefon}\n")

    except mariadb.Error as e:
        messagebox.showerror("Datenbankfehler", f"Fehler: {e}")


# Klasse für Kundenobjekte
class Kunde:
    def __init__(self, anrede, vorname, nachname, telefon):
        self.anrede = anrede
        self.vorname = vorname
        self.nachname = nachname
        self.telefon = telefon

# In der Funktion kunden_abfragen():
kunden_liste = []
for anrede, vorname, nachname, telefon in kunden:
    kunde = Kunde(anrede, vorname, nachname, telefon)
    kunden_liste.append(kunde)

# Ausgabe aktualisieren
ausgabe_text.delete("1.0", tk.END)
if not kunden_liste:
    ausgabe_text.insert(tk.END, f"Keine Kunden unter {alter} Jahren gefunden.")
else:
    for kunde in kunden_liste:
        ausgabe_text.insert(tk.END, f"{kunde.anrede} {kunde.vorname} {kunde.nachname} - Tel: {kunde.telefon}\n")
