def extend_key(text: str, key: str) -> str:
    """
    Розширює ключ до довжини тексту.
    
    :param text: Текст, який потрібно зашифрувати або дешифрувати.
    :param key: Початковий ключ.
    :return: Розширений ключ, однаковий за довжиною з текстом.
    """
    if not key.isalpha():
        raise ValueError("Ключ повинен містити лише літери.")
    return (key * (len(text) // len(key) + 1))[:len(text)]

def vigenere_cipher(text: str, key: str, encrypt: bool = True) -> str:
    """
    Виконує шифрування або дешифрування тексту за допомогою шифру Віженера.
    
    :param text: Вхідний текст (відкритий або зашифрований).
    :param key: Ключ для шифрування/дешифрування.
    :param encrypt: True для шифрування, False для дешифрування.
    :return: Оброблений текст.
    """
    key = extend_key(text, key)
    result_text = []

    for i, char in enumerate(text):
        if char.isupper():
            shift = ord(key[i].upper()) - ord('A')
            shift = shift if encrypt else -shift  # Зміщення залежить від операції
            result_text.append(chr((ord(char) - ord('A') + shift + 26) % 26 + ord('A')))
        elif char.islower():
            shift = ord(key[i].lower()) - ord('a')
            shift = shift if encrypt else -shift  # Зміщення залежить від операції
            result_text.append(chr((ord(char) - ord('a') + shift + 26) % 26 + ord('a')))
        else:
            result_text.append(char)  # Неалфавітні символи залишаються без змін

    return ''.join(result_text)


def read_file(file_path: str) -> str:
    """
    Зчитує текст із файлу.
    
    :param file_path: Шлях до файлу.
    :return: Вміст файлу.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        return ""
    except Exception as e:
        print(f"Помилка читання файлу {file_path}: {e}")
        return ""


def write_file(file_path: str, text: str):
    """
    Записує текст у файл.
    
    :param file_path: Шлях до файлу.
    :param text: Текст для запису.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Помилка запису файлу {file_path}: {e}")

if __name__ == "__main__":
    # Текстовий файл для обробки
    input_file = 'plain_text.txt'
    encrypted_file = 'task_1/encrypted_text_vigenere.txt'
    decrypted_file = 'task_1/decrypted_text_vigenere.txt'

    # Ключ для шифрування
    key = "CRYPTOGRAPHY"

    # Читання вихідного тексту
    plain_text = read_file(input_file)
    
    if plain_text:
        print("\n=== Оригінальний текст ===")
        print(plain_text)

        # Шифрування тексту
        encrypted_text = vigenere_cipher(plain_text, key, encrypt=True)
        write_file(encrypted_file, encrypted_text)
        print("\n=== Результат шифрування ===")
        print(encrypted_text)
        print(f"Зашифрований текст збережено у файлі: {encrypted_file}")

        # Дешифрування тексту
        decrypted_text = vigenere_cipher(encrypted_text, key, encrypt=False)
        write_file(decrypted_file, decrypted_text)
        print("\n=== Результат дешифрування ===")
        print(decrypted_text)
        print(f"Розшифрований текст збережено у файлі: {decrypted_file}")


   


