# Aplicação de Lista de Tarefas

## Descrição

Este script em Python implementa uma aplicação simples de lista de tarefas usando a biblioteca curses para a interface de linha de comando e MySQL para armazenamento de dados. Os usuários podem criar, ler, atualizar e excluir listas de tarefas, além de gerenciar itens individuais dentro de cada lista.

**Nota: Este código ainda está em desenvolvimento e pode não estar totalmente funcional. Contribuições são bem-vindas!**

## Recursos

- Criar uma lista de tarefas com título, descrição, prioridade, categoria e data de vencimento opcional.
- Visualizar todas as listas de tarefas, ordenadas por data de vencimento ou prioridade.
- Adicionar, atualizar e excluir itens dentro de uma lista de tarefas.
- Marcar itens como concluídos ou incompletos.
- Filtrar listas de tarefas por categoria.
- Excluir todos os itens concluídos em uma lista de tarefas.

## Requisitos

- Python 3.x
- Servidor MySQL

## Configuração

1. Instale os pacotes Python necessários:

    ```bash
    pip install pymysql
    ```

2. Configure os detalhes da conexão com o MySQL no script:

    ```python
    # Dentro do método __init__ da classe ListaTarefas
    HOST = 'HOST'
    USER = 'USERNAME'
    PASS = 'PASSWORD'
    DB = 'DATABASE'
    ```

3. Execute o script:

    ```bash
    python main.py
    ```

## Uso

- Use as teclas de seta para navegar entre as listas de tarefas e itens.
- Pressione 'c' para adicionar um novo item à lista de tarefas selecionada.
- Pressione 'enter' para modificar itens dentro de uma lista de tarefas.
- Pressione 'q' para sair da aplicação.

## Notas

- O script utiliza a biblioteca curses para a interface de linha de comando. Certifique-se de que seu terminal a suporta.
