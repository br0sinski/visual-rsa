from rsa import RSA
import asyncio, time

async def main():

    """
    Ab dem Punkt habe ich die einzelnen ü's copy und pasted ;/
    """

    rsa = RSA()
    key_size = 1024
    message = "Hallo Niklas! =)"

    """
    Schreiben Sie ein Testprogramm, das:
    • Ein RSA-Schlüsselpaar generiert
    • Die Laufzeit der einzelnen Operationen misst und ausgibt. (Tuts in jedem Sektor)
    """

    print("Generiere Schlüsselpaar: ")
    start = time.time()
    public_key, private_key = await rsa.generate_keys(key_size)
    print(f"Schlüsselpaar generiert in {time.time() - start:.5f} Sekunden.")

    n, e = public_key
    n_priv, d = private_key
    print(f"[EXTRA DETAIL] Öffentlicher Schlüssel (n, e):\n n = {n}\n e = {e}")
    print(f"[EXTRA DETAIL] Privater Schlüssel (n, d):\n n = {n_priv}\n d = {d}")

    print(f"Ursprüngliche Nachricht: {message}")
    """
    • Eine Textnachricht verschlüsselt und wieder entschlüsselt.
    """
    print("Verschlüssele Nachricht...")
    start = time.time()
    ciphertext = await rsa.encrypt(message, public_key)
    print(f"Verschlüsselt in {time.time() - start:.5f} Sekunden.")
    print(f"[EXTRA DETAIL] Ciphertext (als int): {ciphertext}")

    print("Entschlüssele Nachricht.....")
    start = time.time()
    decrypted = await rsa.decrypt(ciphertext, private_key)
    print(f"Entschlüsselt in {time.time() - start:.5f} Sekunden.")
    print(f"Entschlüsselte Nachricht: {decrypted}")

    """
    • Eine Nachricht signiert und die Signatur verifiziert
    """

    print("Signiere Nachricht.......")
    start = time.time()
    signature = await rsa.sign(message, private_key)
    print(f"Signiert in {time.time() - start:.5f} Sekunden.")
    print(f"[EXTRA DETAIL] Signatur (als int): {signature}")

    print("Verifiziere Signatur........")
    start = time.time()
    verified = await rsa.verify(message, signature, public_key)
    print(f"Verifiziert in {time.time() - start:.5f} Sekunden.")
    print(f"Signatur gültig: {verified}")

if __name__ == "__main__":
    asyncio.run(main())
