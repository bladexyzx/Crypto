import math 
class SimpleCiphers:
    def __init__(self, alphabet):
        """
        Инициализация алфавита и его мощности для последующего шифрования
        :param alphabet: Исходный алфавит (строка символов).
        """
        self.alphabet = alphabet
        self.m = len(alphabet)
        
    def simple_substitution_encrypt(self, text, key):
        if len(key) != self.m:
            return f'Длина ключа ({key}) не соответствует мощности алфавита ({self.m})'
        if sorted(key) != sorted(self.alphabet):
            return f'Один или более символов не указаны в алфавите или наоборот'
        result = ''
        for char in text:
            index = self.alphabet.find(char)
            result += key[index]
        return result
    def simple_substitution_decrypt(self, text, key):
        if len(key) != self.m:
            return f'Длина ключа ({key}) не соответствует мощности алфавита ({self.m})'
        if sorted(key) != sorted(self.alphabet):
            return f'Один или более символов не указаны в алфавите или наоборот'
        result = ''
        for char in text:
            index = key.find(char)
            result += self.alphabet[index]
        return result

if __name__ == "__main__":
    encrypt_or_decrypt = input("Вы хотите зашифровать или расшировать? 1 - зашифровка, 2 - расшифровка \n")
    if encrypt_or_decrypt == "1":
        encrypt_way = input("Каким способом вы хотите зашифровать текст? \n 1 - шифр простой замены \n 2 - аффинный шифр \n 3 - аффинный рекурентный шифр")
        if encrypt_way == "1":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Текст, который вы хотите зашифровать: ")
            key = input("Введите ключ: ")
            print("Шифртекст: ", app.simple_substitution_encrypt(text, key))
    elif encrypt_or_decrypt == '2':
        encrypt_way = input("Каким способом вы хотите расшифровать текст? \n 1 - шифр простой замены \n 2 - аффинный шифр \n 3 - аффинный рекурентный шифр \n")
        if encrypt_way == "1":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Шифртекст, который вы хотите расшифровать: ")
            key = input("Введите ключ: ")
            print("Исходный текст: ", app.simple_substitution_decrypt(text, key))
        