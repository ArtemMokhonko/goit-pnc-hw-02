from collections import Counter
import math
from vigenere import read_file, write_file, vigenere_cipher

def find_repeated_sequences(text: str, length: int) -> dict:
    """
    Знаходить усі повторювані послідовності заданої довжини у тексті.

    :param text: Зашифрований текст.
    :param length: Довжина послідовності для аналізу.
    :return: Словник з послідовностями та їх індексами.
    """
    sequences = {}
    for i in range(len(text) - length + 1):
        sequence = text[i:i + length]
        if sequence in sequences:
            sequences[sequence].append(i)
        else:
            sequences[sequence] = [i]
    return {seq: indices for seq, indices in sequences.items() if len(indices) > 1}

def find_gcd(numbers: list) -> int:
    """
    Знаходить найбільший спільний дільник (НСД) для списку чисел.

    :param numbers: Список чисел.
    :return: НСД чисел.
    """
    gcd = numbers[0]
    for num in numbers[1:]:
        gcd = math.gcd(gcd, num)
    return gcd

def kasiski_analysis(text: str) -> int:
    """
    Виконує метод Касіскі для визначення довжини ключа.

    :param text: Зашифрований текст.
    :return: Оцінена довжина ключа.
    """
    for length in range(3, 6):  # Аналіз послідовностей довжиною 3-5 символів
        repeated_sequences = find_repeated_sequences(text, length)
        distances = []
        for indices in repeated_sequences.values():
            for i in range(1, len(indices)):
                distances.append(indices[i] - indices[i - 1])

        if distances:
            key_length = find_gcd(distances)
            if key_length > 1:
                return key_length
    return 1

def frequency_analysis(text: str) -> str:
    """
    Виконує частотний аналіз тексту для визначення найбільш ймовірного зсуву.

    :param text: Частина тексту, пов'язана з одним символом ключа.
    :return: Найбільш ймовірна літера ключа (зсув).
    """
    english_frequencies = {
        'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127, 
        'F': 0.022, 'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002, 
        'K': 0.008, 'L': 0.040, 'M': 0.024, 'N': 0.067, 'O': 0.075, 
        'P': 0.019, 'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091, 
        'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001, 'Y': 0.020, 
        'Z': 0.001
    }
    text_counter = Counter(text.upper())
    text_length = len(text)
    best_shift = 0
    max_correlation = -1

    for shift in range(26):
        correlation = 0
        for char, count in text_counter.items():
            shifted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            correlation += (count / text_length) * english_frequencies.get(shifted_char, 0)

        if correlation > max_correlation:
            max_correlation = correlation
            best_shift = shift

    return chr(best_shift + ord('A'))

def decrypt_with_kasiski(text: str) -> str:
    """
    Дешифрує текст, зашифрований шифром Віженера, за допомогою методу Касіскі.

    :param text: Зашифрований текст.
    :return: Розшифрований текст.
    """
    key_length = kasiski_analysis(text)
    print()
    print(f"Довжина ключа: {key_length}")
    if key_length == 1:
        raise ValueError("Не вдалося визначити довжину ключа методом Касіскі.")

    key = ""
    for i in range(key_length):
        subsequence = text[i::key_length]
        key += frequency_analysis(subsequence)

    print(f"Визначений ключ: {key}")
    return vigenere_cipher(text, key, encrypt=False)

if __name__ == "__main__":
    encrypted_file = 'task_1/encrypted_text_vigenere.txt'
    decrypted_file = 'task_1/decrypted_text_kasiski.txt'

    encrypted_text = read_file(encrypted_file)
    print("\n=== Зашифрований текст ===")
    print(encrypted_text)

    if encrypted_text:
        try:
            decrypted_text = decrypt_with_kasiski(encrypted_text)
            write_file(decrypted_file, decrypted_text)
            print("\n=== Результат дешифрування ===")
            print(decrypted_text)
            print(f"Розшифрований текст збережено у файлі: {decrypted_file}")
        except ValueError as e:
            print(f"Помилка: {e}")




