import random
import pyperclip
from tabulate import tabulate

class PasswordGenerator():
    def __init__(self, length_pass=None, qtd_letter_upper=None, qtd_letter_lower=None, qtd_number=None, qtd_special_characters=None) -> None:
        self.length_pass = length_pass
        self.qtd_letter_upper = qtd_letter_upper
        self.qtd_letter_lower = qtd_letter_lower
        self.qtd_number = qtd_number
        self.qtd_special_characters = qtd_special_characters

        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.special_characters = "!@#$%&*+_-"
        self.numbers = "0123456789"
        self.especificacoes_list = [self.qtd_letter_lower, self.qtd_letter_upper, self.qtd_number, self.qtd_special_characters]

        self.qtd_especificacoes_definidas = 4
        for especificacao in self.especificacoes_list:
            if especificacao is not None:
                self.qtd_especificacoes_definidas -= 1
        

        print(self.qtd_especificacoes_definidas)

    def set_qtd_letter_upper(self, value):
        self.qtd_letter_upper = value

    def get_qtd_letter_upper(self):
        return self.qtd_letter_upper

    def set_qtd_letter_lower(self, value):
        self.qtd_letter_lower = value

    def get_qtd_letter_lower(self):
        return self.qtd_letter_lower

    def set_qtd_number(self, value):
        self.qtd_number = value

    def get_qtd_number(self):
        return self.qtd_number

    def set_qtd_special_characters(self, value):
        self.qtd_special_characters = value

    def get_qtd_special_characters(self):
        return self.qtd_special_characters

    def auto_mode(self):
        metodos = [
            (self.set_qtd_letter_upper, self.get_qtd_letter_upper),
            (self.set_qtd_letter_lower, self.get_qtd_letter_lower),
            (self.set_qtd_number, self.get_qtd_number),
            (self.set_qtd_special_characters, self.get_qtd_special_characters)
        ]

        self.length_pass = int(random.randint(8, 20))
        total_unspecified = sum(1 for especificacao in self.especificacoes_list if especificacao is None)
        calc = self.length_pass // total_unspecified if total_unspecified > 0 else 0

        for metodo in metodos:
            metodo_set, metodo_get = metodo
            if metodo_get() is None:
                metodo_set(calc)

        print([self.qtd_letter_lower, self.qtd_letter_upper, self.qtd_number, self.qtd_special_characters])

    def calc_pass(self) -> bool:
        # Se as quantidades não foram fornecidas, calcular automaticamente
        if None in [self.qtd_letter_upper, self.qtd_letter_lower, self.qtd_number, self.qtd_special_characters]:
            self.auto_mode()

        self.total_characters = sum([self.qtd_letter_upper, self.qtd_letter_lower, self.qtd_number, self.qtd_special_characters])
        return True if (self.total_characters == self.length_pass) else False

    def define_special_characters(self):
        k = min(self.qtd_special_characters, len(self.special_characters))
        if k <= 0:
            return []
        return random.sample(list(self.special_characters), k=k)
    
    def define_upper_letter(self):
        return random.sample(list(self.letters.upper()), k=self.qtd_letter_upper)

    def define_lower_letter(self):
        k = min(self.qtd_letter_lower, len(self.letters.lower()))
        if k <= 0:
            return []
        return random.sample(list(self.letters.lower()), k=k)

    def define_numbers(self):
        k = min(self.qtd_number, len(self.numbers))
        if k <= 0:
            return []
        return random.sample(list(self.numbers), k=k)

    def define_special_characters(self):
        return random.sample(list(self.special_characters), k=self.qtd_special_characters)


   

    def password(self, final_password):
        table_data = [
            ["Tamanho da senha", self.length_pass],
            ["Quantidade de letras minúsculas", self.qtd_letter_lower],
            ["Quantidade de letras maiúsculas", self.qtd_letter_upper],
            ["Quantidade de números", self.qtd_number],
            ["Quantidade de caracteres especiais", self.qtd_special_characters],
            ["Senha final", final_password],
        ]

        table = tabulate(table_data, headers=["Atributo", "Valor"], tablefmt="grid")
        
        pyperclip.copy(final_password)
        print(table)

    def add_password(self):
        while not self.calc_pass():
            difference_calc = self.length_pass - self.total_characters

            metodos = [
                (self.set_qtd_letter_upper, self.get_qtd_letter_upper),
                (self.set_qtd_letter_lower, self.get_qtd_letter_lower),
                (self.set_qtd_number, self.get_qtd_number),
                (self.set_qtd_special_characters, self.get_qtd_special_characters)
            ]

            set_escolhido, get_escolhido = random.choice(metodos)

            valor_atual = get_escolhido()
            
            set_escolhido(valor_atual + difference_calc)

        password_list = [
            *self.define_lower_letter(),
            *self.define_numbers(),
            *self.define_special_characters(),
            *self.define_upper_letter()
        ]

        random.shuffle(password_list)

        final_password = ''.join(password_list)

        self.password(final_password)

my_pass = PasswordGenerator(qtd_letter_lower=2, qtd_number=3)
my_pass.add_password()
