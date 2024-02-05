**Gerador de Senhas**

Este script Python implementa um gerador de senhas seguro, permitindo a personalização de critérios específicos. Embora funcional, é importante notar que o código pode conter alguns bugs, os quais estão atualmente em processo de correção.

### Classe: PasswordGenerator

#### Atributos:
- `length_pass`: Comprimento da senha gerada.
- `qtd_letter_upper`: Número de letras maiúsculas na senha.
- `qtd_letter_lower`: Número de letras minúsculas na senha.
- `qtd_number`: Número de caracteres numéricos na senha.
- `qtd_special_characters`: Número de caracteres especiais na senha.

#### Métodos:
1. `auto_mode()`: Determina automaticamente os critérios da senha se não forem fornecidos explicitamente.
2. `calc_pass()`: Verifica se os critérios fornecidos resultam em um comprimento de senha válido.
3. `define_special_characters()`, `define_upper_letter()`, `define_lower_letter()`, `define_numbers()`: Métodos para definir tipos específicos de caracteres com base em suas quantidades respectivas.
4. `password(final_password)`: Exibe a senha gerada juntamente com os critérios especificados em um formato de tabela usando a biblioteca `tabulate` e copia a senha para a área de transferência.
5. `add_password()`: Ajusta iterativamente os critérios para criar uma senha válida e, em seguida, gera e exibe a senha.

### Exemplo de Uso:
```python
my_pass = PasswordGenerator(qtd_letter_lower=2, qtd_number=3)
my_pass.add_password()
```

**Observação:** Os bugs do código ainda estão sendo arrumados.
