from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QSpinBox
from PyQt5.QtCore import Qt

from crypto.rsa import RSA

import asyncio, random

class RSAView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("visual-rsa - br0sinski@github")
        self.setGeometry(100, 100, 1000, 600)

        curr_view = QHBoxLayout()
        self.separator = "---------------------------------------------------------------------------------------------"

        """
        Linkes Panel dafuer gedacht dass man alle Werte manipulieren und einsehen kann die der RSA so braucht.
        """
        left_panel = QVBoxLayout()

        """
        Fuer alle noetigen Fields, Inputs, Outputs wurden Hilfsmethoden geschrieben, diese werden hier aufgerufen und spaeter geaddet.
        """
        self.rsa_keysize_field = self.add_spinbox(left_panel, "Key Size:", 512, 4096, 1024, " bits")
        self.message_field = self.add_input_field(left_panel, "Message:", "Please enter something to work with! =)")
        self.p_input = self.add_input_field(left_panel, "p (prime):", "Enter Value for p (HAS TO BE PRIME)", self.update_values)
        self.q_input = self.add_input_field(left_panel, "q (prime):", "Enter Value for q (HAS TO BE PRIME)", self.update_values)
        self.n_output = self.add_output_field(left_panel, "n (p * q):")
        self.phi_output = self.add_output_field(left_panel, "phi ((p-1)*(q-1)):")
        self.e_input = self.add_input_field(left_panel, "e (public exponent):", "Enter Value for exponent e", self.update_values)
        self.d_output = self.add_output_field(left_panel, "d (private exponent):")

        """
        Alle Buttons haben auch eine Hilfsmethode und rufen die gegebene Methode auf.
        """
        self.keygen_button = self.add_button(left_panel, "Generate Keypair", self.generate_keys)
        self.auto_generate_button = self.add_button(left_panel, "Auto Generate", self.auto_generate_values)
        self.encrypt_button = self.add_button(left_panel, "Encrypt", self.encrypt_message, enabled=False)
        self.decrypt_button = self.add_button(left_panel, "Decrypt", self.decrypt_message, enabled=False)
        self.sign_button = self.add_button(left_panel, "Sign", self.sign_message, enabled=False)
        self.verify_button = self.add_button(left_panel, "Verify Signature", self.verify_signature, enabled=False)

        """
        Rechtes panel - dafuer gedacht eine Art "Terminal" Ausgabe zu bieten die zeigt wie der RSA arbeitet
        """
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Process Log:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        right_panel.addWidget(self.log_output)


        curr_view.addLayout(left_panel, 1)
        curr_view.addLayout(right_panel, 2)
        central = QWidget()
        central.setLayout(curr_view)
        self.setCentralWidget(central)
        self.rsa = RSA()
        self.public_key = None
        self.private_key = None
        self.ciphertext = None
        self.signature = None

    """
    Hier sind die Hilfsmethoden damit es einfacher ist die ganzen Objekte einfacher reingeworfen werden koennen und man nicht ewig tippen muss
    """
    def add_input_field(self, layout, label, placeholder, on_change=None):
        layout.addWidget(QLabel(label))
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if on_change:
            input_field.textChanged.connect(on_change)
        layout.addWidget(input_field)
        return input_field

    def add_output_field(self, layout, label):
        layout.addWidget(QLabel(label))
        output_field = QLineEdit()
        output_field.setReadOnly(True)
        layout.addWidget(output_field)
        return output_field

    def add_spinbox(self, layout, label, min_value, max_value, default_value, suffix=""):
        layout.addWidget(QLabel(label))
        spinbox = QSpinBox()
        spinbox.setRange(min_value, max_value)
        spinbox.setValue(default_value)
        spinbox.setSuffix(suffix)
        layout.addWidget(spinbox)
        return spinbox

    def add_button(self, layout, label, callback, enabled=True):
        button = QPushButton(label)
        button.clicked.connect(callback)
        button.setEnabled(enabled)
        layout.addWidget(button)
        return button

    def log(self, message):
        self.log_output.append(message)

    def update_values(self):
        """
        Diese Methode berechnet die Methoden live und logged ggbfs Berechnungen, damit der Nutzer sieht was wie wo passiert
        """
        try:
            # Man schaue einfach ob wir Text in p,q und e haben
            p = int(self.p_input.text()) if self.p_input.text() else None
            q = int(self.q_input.text()) if self.q_input.text() else None
            e = int(self.e_input.text()) if self.e_input.text() else None

            if p and q:
                # Falls p und q da sind updaten wir den Text fuer n und phi weil diese sich nun berechnen lassen
                n = p * q
                phi = (p - 1) * (q - 1)
                self.n_output.setText(str(n))
                self.phi_output.setText(str(phi))
                self.log(f"Calculated n => p * q = {p} * {q} = {n}!")
                self.log(f"Calculated phi => (p-1) * (q-1) = ({p}-1) * ({q}-1) = {phi}!")
                self.log(self.separator)

                if e:
                    try:
                        # Falls wir einen e haben berechnen wir die modulare inverse und setzen den in das Feld ein - falls e teilerfremd zu phi, sonst gibts einen ValueError
                        # wir nutzen die modular_inverse Methode aus der ersten Bonusaufgabe
                        d = self.rsa.modular_inverse(e, phi)
                        self.d_output.setText(str(d))
                        self.log(f"Calcualted d => modular_inverse(e, phi) = modular_inverse({e}, {phi}) = {d}!")
                        self.log(self.separator)
                        self.encrypt_button.setEnabled(True)
                        self.decrypt_button.setEnabled(True)
                        self.sign_button.setEnabled(True)
                        self.verify_button.setEnabled(True)
                    except ValueError:
                        # Das geht aber nur so lange e teilerfremd zu phi ist
                        self.log(f"Error! e: {e} is not co-prime with phi = {phi} =( Choose a different e")
                        self.log(self.separator)
                        self.d_output.clear()
                        self.encrypt_button.setEnabled(False)
                        self.decrypt_button.setEnabled(False)
                        self.sign_button.setEnabled(False)
                        self.verify_button.setEnabled(False)
                else:
                    self.d_output.clear()
                    self.encrypt_button.setEnabled(False)
                    self.decrypt_button.setEnabled(False)
                    self.sign_button.setEnabled(False)
                    self.verify_button.setEnabled(False)
            else:
                self.n_output.clear()
                self.phi_output.clear()
                self.d_output.clear()
                self.encrypt_button.setEnabled(False)
                self.decrypt_button.setEnabled(False)
                self.sign_button.setEnabled(False)
                self.verify_button.setEnabled(False)
        except ValueError:
            self.log("Error: Invalid input for RSA parameters - Try different ones or use AutoGen!")
            self.log(self.separator)

    def generate_keys(self):
        asyncio.run(self.gen_keys())

    async def gen_keys(self):
        key_size = self.rsa_keysize_field.value()
        self.log(f"Generating {key_size}bit RSA keyspair..")
        self.public_key, self.private_key = await self.rsa.generate_keys(key_size)
        self.log(f"Public-Key: {self.public_key}")
        self.log(f"Private-Key: {self.private_key}")
        self.log(self.separator)
        self.encrypt_button.setEnabled(True)
        self.decrypt_button.setEnabled(True)
        self.sign_button.setEnabled(True)
        self.verify_button.setEnabled(True)

    def encrypt_message(self):
        asyncio.run(self.async_encrpyt_message())

    async def async_decrypt_message(self):
        if not self.private_key:
            return
        if not self.ciphertext:
            self.log("Error: No text to decrypt")
            return
        self.log("Decrypting ciphertext...")
        #Rufe die Decrypt Methode auf aus Boniaufgabe 1
        decrypted_message = await self.rsa.decrypt(self.ciphertext, self.private_key)
        self.log(f"Decrypted Message: {decrypted_message}")
        self.log(self.separator)


    def decrypt_message(self):
        asyncio.run(self.async_decrypt_message())


    async def sign_message_async(self):
        if not self.private_key:
            return
        message = self.message_field.text()
        if not message:
            self.log("Error: Please enter a message to sign")
            return
        self.log(f"Signing message: {message}")
        self.signature = await self.rsa.sign(message, self.private_key)
        self.log(f"Signature: {self.signature}")
        self.log(self.separator)

    def sign_message(self):
        asyncio.run(self.sign_message_async())

    async def verify_signature_async(self):
        if not self.public_key:
            self.log("Error: Public key not generated. Please generate keys first.")
            return
        message = self.message_field.text()
        if not message or not self.signature:
            self.log("Error: No message or signature to verify.")
            return
        self.log(f"Verfiying signature for the message: {message}")
        self.log(f"Signature: {str(self.signature)}")  
        is_valid = await self.rsa.verify(message, self.signature, self.public_key)
        
        if is_valid:
            self.log(f"Signature is valid: {is_valid}")
        else:
            self.log("Signature is invalid.")

    def verify_signature(self):
        asyncio.run(self.verify_signature_async())

    def auto_generate_values(self):
        self.log("Auto-generating RSA parameters...")
        p = random.choice([61, 53, 47, 71])  
        q = random.choice([67, 59, 73, 79])
        # setze 65537 laut "Konvention"
        e = 65537  
        self.p_input.setText(str(p))
        self.q_input.setText(str(q))
        self.e_input.setText(str(e))
        self.update_values()

    async def async_encrpyt_message(self):
        # Check ob wir einen publickey schon haben
        if not self.public_key:
            self.log("Error: Publickey not generated yet. Please generate the keys first then try again (I havent yet implemented that the programm creates keys automatically - do it yourself!)")
            self.log(self.separator)
            return
        message = self.message_field.text()
        if not message:
            self.log("Error: No message was given - enter a message first")
            self.log(self.separator)
            return
        self.log(f"Encrypting message: {message}")

        #falls Text vorhanden und Keys vorhanden rufe die Methode aus der ersten Bonusaufgabe auf und verschluessele!
        self.ciphertext = await self.rsa.encrypt(message, self.public_key)
        self.log(f"Encrypted message: {self.ciphertext}")
        self.log(self.separator)
