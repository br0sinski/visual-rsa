Dokumentation

Die RSA-Implementierung befindet sich in der Datei RSA.py.

Wesentliche Punkte:

Schlüsselerzeugung // generate_keys(keysize):
Zur Generierung wird zunächst überprüft, dass der Schlüssel mindestens 1024 Bit groß ist. Danach werden zwei Primzahlen (p und q) erzeugt. Die Primzahlen werden  eines asynchron und basierend auf dem Miller Rabin Tests (siehe Methode is_prime()) generiert

Berechnung von n und phi:
Mit den gefundenen p und q werden n (Produkt der beiden Zahlen) und phi (Eulersche Funktion, berechnet als (p-1)*(q-1)) bestimmt. Diese Werte sind entscheidend für die weiteren Schritte wie z. B. die Ermittlung des öffentlichen und privaten Exponenten

Öffentlicher Exponent (e):
Standardmäßig wird hier der Wert 65537 verwendet, da dies in der üblich ist. Sollte 65537 jedoch nicht teilerfremd zu phi sein, wird ein alternativer Wert (beginnend bei 3 und steigend um 2) gesucht bis ein passender Exponent gefunden wird.

Privater Exponent (d) und Modular Inverse:
Die Berechnung des privaten Exponenten erfolgt durch Bestimmung des modularen Inversen von e modulo phi - Hier wird die Python-eigene pow()-Funktion genutzt (seit Python 3.8/den hinterlassenen Kommentar) und die alternative Implementierung mittels des erweiterten euklidischen Algorithmus 
wird mitgeliefert damit es konform mit der Aufgabenstellung ist. In der Implementierung hat sich jedoch die pow()-Funktion als effizienter erwiesen.

Verschlüsselung und Entschlüsselung:
Bei der Verschlüsselung wird die Nachricht zunächst in UTF-8 kodiert und anschließend in eine Integer-Darstellung konvertiert – unter der Big-Endian Byte-Reihenfolge. Dabei wird ein Sicherheitscheck vorgenommen, ob die Nachricht nicht zu groß für den Modulus n ist

Digitale Signatur:
Die Signierung funktioniert parallel zur Verschlüsselung, indem die Nachricht mit dem privaten Schlüssel expotentiert wird. Die Überprüfung erfolgt indem man den signierten Wert mit dem öffentlichen Schlüssel expotentiert und anschließend prüft, ob die ursprüngliche Nachricht wiederhergestellt werden kann.

Dokumentation der GUI / view Implementierung
Die Datei view.py ist eine in PyQt5 implementierte visuelle Darstellung des RSA
Man hat sich für  PyQt5 entschieden da es sich irgendwie angenehmer gegenüber Tkinter darstellte (und weil PyGTK viel Stress gemacht hat)

Folgende Komponenten sind zu finden:

Linker Teilbereich der GUI:
In diesem Bereich können alle notwendigen Eingabefelder, Ausgabefelder, Spinboxes und Buttons abgelegt werden, um die RSA-Parameter einzustellen und Operationen auszulösen.
Diese sind auch reaktiv und passen sich je nach Eingabe an - das handled die update_values() - Methode. Ist eine Eingabe ungültig oder nicht vollständig, werden die Output-Felder geleert und Buttons entsprechend deaktiviert.

Eingabefelder: p, q, e und die Nachricht.
Ausgabefelder: Berechnete Werte wie n, phi und der private Exponent (d) anhand der Eingabefelder

Rechtes Panel – Terminal:
Dieser Bereich dient als Terminal/Log-Ausgabe in dem alle Schritte und Fehlermeldungen für den Benutzer festgehalten werden. Hier können alle Aktionen (z. B. Schlüsselgenerierung, Verschlüsselung, Signatur) eingesehen werden

Auto-Generierung:
Eine zusätzliche Funktion (auto_generate_values()) ist implementiert, die per Zufall vordefinierte Werte für p und q wählt, die Konvention bei e (65537) setzt - anschließend wird automatisch die Berechnungen ausgelöst. 
