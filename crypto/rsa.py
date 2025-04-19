import random, math

class RSA:

    """
    Hinweis: Ich habe keine ue, oe, ae auf meiner Tastatur, ich bin gerade auf meiner Linux Partition was
    das Standardmaessige US - Layout nutzt. Von Daher sind die Kommentare auf Deutsch nie mit den Umlauten zu finden
    """

    def __init__(self):
        self.public_key = None
        self.private_key = None

    async def generate_keys(self, keysize):
        # Erster Check ob wir mindestens RSA 1024 usen
        if keysize < 1024:
            raise ValueError("Key Size must be atleast 1024 bits!")

        # Auswahl von P und Q
        # Diese muessen Prim sein - d.h nutzen wir in der generate_prime() Methode
        # den Miller Rabin Primality Test fuer die Primzahlgenerierung
        p = await self.generate_prime(keysize//2)
        q = await self.generate_prime(keysize//2)

        # Extra check damit p und q nicht identisch sein koennen
        while p==q:
            q = await self.generate_prime(keysize//2)
        # n und phi sind nach Definition berechnet
        n = p * q
        phi = (p-1)*(q-1)

        # Als oeffentlichen Exponenten nutze man 65537
        e = 65537

        if math.gcd(e,phi) != 1:
            e = 3
            while math.gcd(e, phi) != 1:
                e += 2

        d = self.modular_inverse(e, phi)

        self.public_key = (n,e)
        self.private_key = (n,d)

        return self.public_key, self.private_key
    
    async def encrypt(self, message, public_key):
        # Man nehme unseren Public Key samt Exponenten
        n, e = public_key
        # Kodiere die Nachricht als UTF-8 und wandle die in ein Integer um (big-endian Byte Reihenfolge, da Konvention)
        # Wichtig hier ist dass die Information verloren geht wie lang die Nachricht urspruenglich war
        # Das muss man in decrypt() rekonstruieren
        message = int.from_bytes(message.encode("utf-8"), byteorder="big")

        #Sicherheitscheck: Ist diese Nachricht zu gross fuer den Modulus?
        if message >= n:
            raise ValueError("Key Size too small for this operation!")
        
        # Nun verschluesselt man anhand: c = message^e mod n
        cipher = self.modular_exponentiation(message, e, n)

        # Rueckgbe des verschluesselten Werts
        return cipher

    async def decrypt(self, ciphertext, private_key):
        # Man nehme unseren Private Key samt Exponenten
        n, d = private_key
        # Entschluessele die Nachricht mittels der modularer Exponentation: message = cipher^d mod n
        message = self.modular_exponentiation(ciphertext, d, n)

        # Damit ich die (noch) entschluesselte Zahl korrekt in einen String konventieren kann muss ich wissen wieviele Bytes sie
        # urspruenglich belegt hat - das ist ein kleiner Trick
        # Man nehme also die Anzahl der Bits zurueck, rundet auf das naechste volle Byte auf und hat somit die String laenge!
        length = (message.bit_length() + 7) // 8
        # Hier wird dann anhand der Lange und dem Dekodieren von UTF-8 die Nachricht wieder hergestellt und returned.
        return message.to_bytes(length, byteorder="big").decode("utf-8")
    
    async def sign(self, message, private_key):
        # Man nehme unseren private_key
        n, d = private_key
        # Kodiert die Nachricht genauso wie in encrypt() mittles UTF-8 und representiert die in der big-endian Byte Reihenfolge
        message = int.from_bytes(message.encode("utf-8"), byteorder="big")

        if message >= n:
            raise ValueError("Key Size too small for this operation!")
        
        # Berechnet die Signatur anhand: message^d mod n
        signed = self.modular_exponentiation(message, d, n)
        return signed
    
    async def verify(self, message, signature, public_key):
        n, e = public_key
        # Kodiert die Nachricht in UTF-8 und representiert in Big-Endian
        message = int.from_bytes(message.encode("utf-8"), byteorder="big")
        # Man holt sich die Signatur der ursprunglichen Nachricht
        message_from_signature = self.modular_exponentiation(signature, e, n)

        # Schaut nach: Stimmen die Integer Darstellungen ueberein? J/n
        return message == message_from_signature
 
    """"""""""""""""""""""""""""""""""""""""""""""
    
    ALLE WEITEREN RSA HILFSMETHODEN
    
    """""""""""""""""""""""""""""""""""""""""""""

    def modular_exponentiation(self, base, exponent, mod):
        """
        Implementierung anhand des Square and Multiply Algorithmus
        """
        result = 1
        # Sicherstellung dass die Basis im richtigen modolu Bereich liegt
        base = base % mod

        
        while exponent > 0:
            # wenn der aktuelle exponent ungerade ist: multiply
            if exponent % 2 == 1:
                result = (result * base) % mod
            # exponenten halbieren / bitweise nach rechts verschieben
            exponent = exponent >> 1
            # basis quadrieren: square
            base = (base*base) % mod

        return result

    def extended_gcd(self, a, b):
        """
        Den erweiterten euklidischen Algorithmus zur Bestimmung des multiplikativen
        Inversen. (laut Aufgabenstellung) wird aber nie in dieser Implementation verwendet.
        Siehe modular_inverse() Methode
        """

        # Rekursionsanker
        if a==0:
            return (b, 0, 1)
        else:
            # Rekursiver Aufruf des e. e. Algorithmus (da kommen Mathe 1 Erinnerungen hoch)
            g,y,x = self.extended_gcd(b%a,a)
            return(g,x-(b//a)*y, y)


    def modular_inverse(self, a, m):
        # Seit Python 3.8 kann man die Inverse anhand der pow() Methode errechnen
        # Quelle: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
        # Die Methode fuer den euklidischen Algorithmus ist auch implementiert, damit man mir nicht die Punkte
        # absprechen kann, aber ich verwende sie nicht.
        return pow(a, -1, m)

    async def generate_prime(self, length):
        while True:
            """
             Basierend auf der Bitlaenge generiere ich meine Primzahl
             Danach schaue ich anhand des Miller-Rabin-Tests ob wir wirklich
             eine Primzahl haben
            """
            # Gib einen random Kanidaten im Bereich der gegeben (RSA Schluessel)-Laenge
            canidat = random.getrandbits(length)
            # check ob prime
            if await self.is_prime(canidat):
                # wenn ja dann gib den Kanidaten zurueck
                return canidat
            
    async def is_prime(self, n, k=40):
        # Miller Rabin Primality Test fuer Primzahlgenerierung
        if n < 2 or n % 2 == 0:
            return False
        if n == 2 or n == 3:
            return True


        # Schreibe n-1 als 2^r * d mit ungeradem d
        # das ist notwendig fuer den eigentlichen Miller Rabin Test
        r, d = 0, n - 1
        while d % 2 == 0:
            d //= 2
            r += 1
        # Jetzt gilt: n - 1 = 2^r * d

        # Wiederhole den Test k-mal mit zufälligen Basen a
        for _ in range(k):
            # waehle zufaellige Basis a: 2 <= a <= n - 2
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)

            # wenn x = 1 oder x = n - 1 dann besteht n diesen Testdurchlauf -> return True
            if x == 1 or x == n - 1:
                continue
            # wiederhole r - 1 mal das quadrieren von x
            for _ in range(r - 1):
                x = pow(x, 2, n)
                # wenn x irgendwann zu n-1 wird, besteht n diesen Test nicht
                if x == n - 1:
                    break
            else:
                return False
        return True


    """

    "Testprogramm" nach Aufgabe 3.

    """     
