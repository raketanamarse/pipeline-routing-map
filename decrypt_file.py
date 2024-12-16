#!/bin/python3

import os
from tkinter import Tk, filedialog, simpledialog, messagebox
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    """Генерация ключа на основе пароля и соли"""
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())

def decrypt_file(file_path: str, password: str, output_path: str):
    """Расшифровка файла"""
    with open(file_path, 'rb') as f:
        data = f.read()

    salt = data[:16]
    iv = data[16:32]
    encrypted_data = data[32:]

    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    with open(output_path, 'wb') as f:
        f.write(data)

    messagebox.showinfo("Успех", f"Файл успешно расшифрован и сохранён как {output_path}")

def main():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Выберите файл для расшифровки")
    if not file_path:
        return

    password = simpledialog.askstring("Пароль", "Введите пароль для расшифровки", show="*")
    if not password:
        messagebox.showerror("Ошибка", "Пароль не может быть пустым")
        return

    output_path = filedialog.asksaveasfilename(title="Сохранить расшифрованный файл", defaultextension=".kml")
    if not output_path:
        return

    try:
        decrypt_file(file_path, password, output_path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось расшифровать файл: {e}")

if __name__ == "__main__":
    main()
