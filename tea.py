#!/usr/bin/env python3
"""
Автор: студент Лукьянов Александр Дмитриевич

Данный файл содержит реализацию алгоритма шифрования TEA (Tiny Encryption Algorithm).
Алгоритм работает с блоками по 64 бита и использует ключ длиной 128 бит.

Программа запускается в диалоговом режиме в терминале:
- пользователь вводит ключ;
- выбирает шифрование или расшифрование;
- вводит текст и получает результат.
"""

# Учебный комментарий: начало детализации алгоритма
# TEA использует 64-битные блоки данных
# Ключ алгоритма TEA имеет длину 128 бит
# Начало цикла шифрования (32 раунда)



# Подключаем необходимые стандартные библиотеки Python
import struct
from typing import Tuple

# Маска для ограничения чисел 32 битами
MASK32 = 0xFFFFFFFF

# Магическая константа DELTA (используется в каждом раунде)
DELTA = 0x9E3779B9

# Размер блока в байтах (64 бита = 8 байт)
BLOCK_SIZE = 8


def _u32(x: int) -> int:
    """
    Ограничивает число 32 битами.
    Нужно, чтобы все операции выполнялись по модулю 2^32.
    """
    return x & MASK32


def _split_u32_be(block: bytes) -> Tuple[int, int]:
    """
    Разбивает 8 байт на два 32-битных числа.
    """
    return struct.unpack(">2I", block)


def _join_u32_be(v0: int, v1: int) -> bytes:
    """
    Собирает два 32-битных числа обратно в 8 байт.
    """
    return struct.pack(">2I", _u32(v0), _u32(v1))


def _key_u32_be(key: bytes) -> Tuple[int, int, int, int]:
    """
    Разбивает ключ длиной 16 байт на 4 части по 32 бита.
    """
    return struct.unpack(">4I", key)


def tea_encrypt_block(block: bytes, key: bytes, rounds: int = 32) -> bytes:
    """
    Шифрует один 64-битный блок данных алгоритмом TEA.
    """
    # Делим блок на две половины
    v0, v1 = _split_u32_be(block)

    # Делим ключ на 4 части
    k0, k1, k2, k3 = _key_u32_be(key)

    # Начальное значение суммы
    s = 0

    # Основной цикл шифрования (32 раунда)
    for _ in range(rounds):
        s = _u32(s + DELTA)
        v0 = _u32(v0 + (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1)))
        v1 = _u32(v1 + (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3)))

    # Собираем зашифрованный блок
    return _join_u32_be(v0, v1)


def tea_decrypt_block(block: bytes, key: bytes, rounds: int = 32) -> bytes:
    """
    Расшифровывает один 64-битный блок данных алгоритмом TEA.
    """
    v0, v1 = _split_u32_be(block)
    k0, k1, k2, k3 = _key_u32_be(key)

    # Начальное значение суммы для расшифрования
    s = _u32(DELTA * rounds)

    # Основной цикл расшифрования
    for _ in range(rounds):
        v1 = _u32(v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3)))
        v0 = _u32(v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1)))
        s = _u32(s - DELTA)

    return _join_u32_be(v0, v1)


def pkcs7_pad(data: bytes) -> bytes:
    """
    Добавляет padding, чтобы длина данных была кратна 8 байтам.
    """
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data: bytes) -> bytes:
    """
    Убирает padding после расшифрования.
    """
    return data[:-data[-1]]


def ecb_encrypt(data: bytes, key: bytes) -> bytes:
    """
    Шифрует данные в режиме ECB.
    """
    data = pkcs7_pad(data)
    result = b""

    for i in range(0, len(data), BLOCK_SIZE):
        result += tea_encrypt_block(data[i:i + BLOCK_SIZE], key)

    return result


def ecb_decrypt(data: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные в режиме ECB.
    """
    result = b""

    for i in range(0, len(data), BLOCK_SIZE):
        result += tea_decrypt_block(data[i:i + BLOCK_SIZE], key)

    return pkcs7_unpad(result)


# ================== ДИАЛОГОВЫЙ РЕЖИМ ==================

def dialog_mode():
    """
    Диалоговый режим работы программы.
    Пользователь вводит данные через терминал.
    """
    print("=== Алгоритм шифрования TEA ===")

    # Ввод ключа
    key_hex = input("Введите ключ (32 hex-символа): ")
    key = bytes.fromhex(key_hex)

    while True:
        print("\nВыберите действие:")
        print("1 — Зашифровать")
        print("2 — Расшифровать")
        print("0 — Выход")

        choice = input("> ")

        if choice == "0":
            print("Завершение работы программы.")
            break

        text = input("Введите текст: ")

        if choice == "1":
            encrypted = ecb_encrypt(text.encode("utf-8"), key)
            print("Зашифрованный текст (hex):")
            print(encrypted.hex())

        elif choice == "2":
            decrypted = ecb_decrypt(bytes.fromhex(text), key)
            print("Расшифрованный текст:")
            print(decrypted.decode("utf-8"))

        else:
            print("Ошибка: неверный пункт меню.")


# ================== ТОЧКА ВХОДА В ПРОГРАММУ ==================

if __name__ == "__main__":
    # Запуск диалогового режима
    dialog_mode()
