import math

class KeyValidityError(Exception):
    """Некорректный ключ"""
    pass

class CharacterMismatch(Exception):
    """ Несоответствие символов алфавита и ключа, релевантно только для шифра простой замены, 
        так как ключом является тот же алфавит, преобразованный некой подстановкой
    """
    pass

class SaveFileException(Exception):
    """Ошибка сохранения файла"""
    pass



def save_in_file(text):
    ans = input("Сохранить содержимое вывода в отдельный файл? [y/n]: ")
    if ans == 'y':
        filename = input("Введите название файла: ")
        if not filename.endswith(".txt"):
            filename += ".txt"
        try:
            with open(filename, "w") as f:
                f.write(text)
        except:
            raise SaveFileException("Ошибка записи файла")

class SimpleCiphers:
    def __init__(self, alphabet):
        """
        Инициализация алфавита и его мощности для последующего шифрования
        :param alphabet: Исходный алфавит (строка символов).
        """
        self.alphabet = alphabet
        self.m = len(alphabet) - alphabet.count(".") - alphabet.count(" ") - alphabet.count(",")
    
    @staticmethod
    def gcd(a, b):
        """Алгоритм Евклида"""
        while b != 0:
            a, b = b, a % b
        return a
    
    def inverse(self, a):
        return pow(a, -1, self.m)
    
    def simple_substitution_encrypt(self, text, key):
        if len(key) != self.m:
            raise KeyValidityError(f'Длина ключа ({key}) не соответствует мощности алфавита ({self.m})')
        if sorted(key) != sorted(self.alphabet):
            raise CharacterMismatch("Один или более символов не указаны в алфавите или наоборот")
        result = ''
        for char in text:
            if char in [" ", ".", ","]:
                result += char
                continue
            index = self.alphabet.find(char)
            result += key[index]
        return result
    def simple_substitution_decrypt(self, text, key):
        if len(key) != self.m:
            raise KeyValidityError(f'Длина ключа ({key}) не соответствует мощности алфавита ({self.m})')
        if sorted(key) != sorted(self.alphabet):
            raise CharacterMismatch("Один или более символов не указаны в алфавите или наоборот")
        result = ''
        for char in text:
            if char in [" ", ".", ","]:
                result += char
                continue
            index = key.find(char)
            result += self.alphabet[index]
        return result   
    
    
    
    def affine_cipher_encrypt(self, text, key_a, key_b):
        key_a = int(key_a)
        key_b = int(key_b)
        if self.gcd(key_a, self.m) != 1 :
            raise KeyValidityError("Первое число ключа и мощность алфавита не взаимно просты")
        result = ''
        for char in text:
            if char in [" ", ".", ","]:
                result += char
                continue   
            x = self.alphabet.find(char)    
            y = key_a * x + key_b
            result += self.alphabet[y % self.m]
        return result
    def affine_cipher_decrypt(self, text, key_a, key_b):
        key_a = int(key_a)
        key_b = int(key_b)
        if self.gcd(key_a, self.m) != 1 :
            raise KeyValidityError("Первое число ключа и мощность алфавита не взаимно просты")
        result = ''
        for char in text:
            if char in [" ", ".", ",", '\n']:
                result += char
                continue
            y = self.alphabet.find(char)
            x = (y - key_b) * self.inverse(key_a)
            result += self.alphabet[x % self.m]
        return result
    
    def affine_recurrent_cipher_encrypt(self, text, key_1a, key_1b, key_2a, key_2b):
        
        key_1a, key_1b, key_2a, key_2b = int(key_1a), int(key_1b), int(key_2a), int(key_2b)
        
        if self.gcd(key_1a, self.m) != 1 or self.gcd(key_2a, self.m) != 1:
            raise KeyValidityError("Первое число ключа и мощность алфавита не взаимно просты")
        result = ''
        
        
        x = self.alphabet.find(text[0])
        y = key_1a * x + key_1b
        result += self.alphabet[y % self.m]
        x = self.alphabet.find(text[1])
        y = key_2a * x + key_2b
        result += self.alphabet[y % self.m]
        
        prev2_a, prev2_b = key_1a, key_1b #i - 2 элемент
        prev1_a, prev1_b = key_2a, key_2b #i - 1 элемент
        
        for i in range(2, len(text)):
            if text[i] in [" ", ".", ","]:
                result += text[i]
                continue
            current_a = (prev1_a * prev2_a) % self.m
            current_b = (prev1_b + prev2_b) % self.m
            x = self.alphabet.find(text[i])
            y = current_a * x + current_b
            result += self.alphabet[y % self.m]
            prev2_a, prev2_b = prev1_a, prev1_b
            prev1_a, prev1_b = current_a, current_b
            
        return result


    def affine_recurrent_cipher_decrypt(self, text, key_1a, key_1b, key_2a, key_2b):
        key_1a, key_1b, key_2a, key_2b = int(key_1a), int(key_1b), int(key_2a), int(key_2b)
        
        if self.gcd(key_1a, self.m) != 1 or self.gcd(key_2a, self.m) != 1:
            raise KeyValidityError("Первое число ключа и мощность алфавита не взаимно просты")
        result = ''
        result += self.alphabet[((self.alphabet.find(text[0]) - key_1b) * self.inverse(key_1a)) % self.m]
        result += self.alphabet[((self.alphabet.find(text[1]) - key_2b) * self.inverse(key_2a)) % self.m]
        
        prev2_a, prev2_b = key_1a, key_1b #i - 2 элемент
        prev1_a, prev1_b = key_2a, key_2b #i - 1 элемент
        
        for i in range(2, len(text)):
            if text[i] in [" ", ".", ","]:
                result += text[i]
                continue
            
            current_a = (prev1_a * prev2_a) % self.m
            current_b = (prev1_b + prev2_b) % self.m
            y = self.alphabet.find(text[i])
            x = (y - current_b) * self.inverse(current_a)
            result += self.alphabet[x % self.m]
            prev2_a, prev2_b = prev1_a, prev1_b
            prev1_a, prev1_b = current_a, current_b
            
        return result
        
if __name__ == "__main__":
    encrypt_or_decrypt = input("Вы хотите зашифровать или расшировать? 1 - зашифровка, 2 - расшифровка \n")
    res = ''
    if encrypt_or_decrypt == "1":
        encrypt_way = input("Каким способом вы хотите зашифровать текст? \n 1 - шифр простой замены \n 2 - аффинный шифр \n 3 - аффинный рекурентный шифр \n")
        if encrypt_way == "1":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Текст, который вы хотите зашифровать: ")
            key = input("Введите ключ: ")
            res = app.simple_substitution_encrypt(text, key)
        if encrypt_way == "2":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Введите текст, который хотите зашифровать ")
            key_a = input("Введите первое число ключа. Оно должно быть взаимно простым с мощностью алфавита ")
            key_b = input("Введите второе число ключа ")
            res = app.affine_cipher_encrypt(text, key_a, key_b)
        if encrypt_way == "3":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Введите текст, который хотите зашифровать ")
            key_1a = input("Введите первое число первого ключа. Оно должно быть взаимно простым с мощностью алфавита ")
            key_1b = input("Введите второе число первого ключа ")
            key_2a = input("Введите первое число второго ключа. Оно должно быть взаимно простым с мощностью алфавита ")
            key_2b = input("Введите второе число второго ключа ")
            res = app.affine_recurrent_cipher_encrypt(text, key_1a, key_1b, key_2a, key_2b)          
    elif encrypt_or_decrypt == '2':
        encrypt_way = input("Каким способом вы хотите расшифровать текст? \n 1 - шифр простой замены \n 2 - аффинный шифр \n 3 - аффинный рекурентный шифр \n")
        if encrypt_way == "1":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Шифртекст, который вы хотите расшифровать: ")
            key = input("Введите ключ: ")
            res =  app.simple_substitution_decrypt(text, key)
        if encrypt_way == "2":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Введите шифртекст, который хотите расшифровать: ")
            key_a = input("Введите первое число ключа. Оно должно быть взаимно простым с мощностью алфавита: ")
            key_b = input("Введите второе число ключа: ")
            res = app.affine_cipher_decrypt(text, key_a, key_b)
        if encrypt_way == "3":
            user_alphabet = input("Введите алфавит: ")
            app = SimpleCiphers(user_alphabet)
            text = input("Введите шифртекст, который хотите расшифровать: ")
            key_1a = input("Введите первое число первого ключа. Оно должно быть взаимно простым с мощностью алфавита ")
            key_1b = input("Введите второе число первого ключа ")
            key_2a = input("Введите первое число второго ключа. Оно должно быть взаимно простым с мощностью алфавита ")
            key_2b = input("Введите второе число второго ключа ")
            res = app.affine_recurrent_cipher_decrypt(text, key_1a, key_1b, key_2a, key_2b)
    if res:
        print(f'{res}')
        save_in_file(res)