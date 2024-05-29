import os
import re

def create_m3u_playlists(folder_path):
    # Erstelle ein Wörterbuch, um die Dateipfade für jedes Spiel zu speichern
    spiele = {}

    # Regex-Muster, um Dateinamen zu erfassen und den Spielnamen-Teil zu extrahieren
    muster = re.compile(r"^(.*)\s\(Disc\s\d+\).*\.chd$", re.IGNORECASE)

    # Iteriere über alle Dateien im angegebenen Ordner
    for dateiname in os.listdir(folder_path):
        # Überprüfe, ob die Datei mit .chd endet
        if dateiname.endswith(".chd"):
            # Vergleiche den Dateinamen mit dem Regex-Muster
            match = muster.match(dateiname)
            if match:
                spiel_name = match.group(1)
                # Füge die Datei zur entsprechenden Liste der Discs des Spiels hinzu
                if spiel_name not in spiele:
                    spiele[spiel_name] = []
                spiele[spiel_name].append(dateiname)

    # Erstelle M3U-Dateien für jedes Spiel
    for spiel_name, dateien in spiele.items():
        # Sortiere die Dateien, um die richtige Reihenfolge sicherzustellen
        dateien.sort()

        # Definiere den Pfad für die M3U-Datei
        m3u_dateiname = f"{spiel_name}.m3u"
        m3u_dateipfad = os.path.join(folder_path, m3u_dateiname)

        # Schreibe die Dateipfade in die M3U-Datei
        with open(m3u_dateipfad, 'w') as m3u_datei:
            for datei in dateien:
                # Konvertiere den Pfad in Unix-Format ohne Laufwerksbuchstaben
                relativer_pfad = os.path.relpath(os.path.join(folder_path, datei), start=folder_path)
                unix_stil_pfad = f"/{relativer_pfad.replace(os.sep, '/')}"
                m3u_datei.write(f"{unix_stil_pfad}\n")

    print("M3U-Playlists erfolgreich erstellt.")

# Spezifizieren Sie den Ordner, der die CHD-Dateien enthält
folder_path = os.path.dirname(os.path.abspath(__file__))  # Aktuelles Verzeichnis
create_m3u_playlists(folder_path)
