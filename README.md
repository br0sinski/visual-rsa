# visual-rsa
A visual representation of the RSA Algorithm

## Bonusaufgabe 1 ausfuehren/testen

1. In das Repo clonen:
   ```bash
   git clone https://github.com/br0sinski/visual-rsa.git
   ```

2. In das Directory gehen:
   ```bash
   cd visual-rsa
   ```

3. Das Programm ausfuehren:
   ```bash
   python3 crypto/main.py
   ```

**Hinweis:** `pip install` ist noch nicht erforderlich, da diese Teilaufgabe keine externen Bibliotheken verwendet.

## Bonusaufgabe 2 ausfuehren/testen (empfohlen)

### Methode 1: Ausfuehren des Quellcodes

1. Repository klonen (falls noch nicht geschehen):
   ```bash
   git clone https://github.com/br0sinski/visual-rsa.git
   cd visual-rsa
   ```

2. Virtual Enviornment erstellen
   ```bash
   # Virtual Environment erstellen
   python -m venv venv
   
   # Virtual Environment aktivieren
   # Fuer Linux/MacOS:
   source venv/bin/activate
   # Fuer Windows
   # .\venv\Scripts\activate
   ```

3. Dependencies installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. Programm starten:
   ```bash
   python3 gui/main.py
   ```

### Methode 2: Vorgefertigte Binaries aus Releases (nicht empfohlen: Windows Defender setzt eine False Positive??? - Unter Windows 10 alles fine, unter 11 nicht)

1. Gehe auf die [Releases-Seite](https://github.com/br0sinski/visual-rsa/releases) des Projekts
2. Lade je nach Betriebssystem die vorgefertigten Binaries runter:
   - Fuer Windows: `visual-rsa.exe`
   - Fuer Linux: `visual-rsa`
3. Fuehre die Binary asu!:
   - Windows: Doppelklick auf die `.exe` Datei
   - Linux:
     ```bash
     chmod +x visual-rsa
     ./visual-rsa
     ```

