__author__ = 'Wesley Ruan'


import pymysql
from datetime import date
import curses
import time

        
class ListaTarefas:
    def __init__(self) -> None:
        try:
            HOST = 'HOST'
            USER = 'USERNAME'
            PASS = 'PASSWORD'
            DB = 'DATABASE'

            self.conn = pymysql.connect(
                host=HOST,
                user=USER,
                password=PASS,
                database=DB,
                autocommit=True
            )
            

            self.cursor = self.conn.cursor()
        except pymysql.err.OperationalError as e:
            print("Não é possível conectar-se ao servidor MySQL, por favor verifíque as configurações do servidor.")
            exit(1)



    def createList(self, titulo : str, descricao : str, prioridade : bool, categoria : str, data_vencimento : date = None):
        '''
        Criar lista
        '''

        if data_vencimento:
            sql_query = "INSERT INTO lista (titulo, descricao, priority, categoria, data_vencimento) VALUES (%s, %s, %s, %s, %s)"
            values_query = (titulo, descricao, prioridade, categoria, data_vencimento)
        else:
            sql_query = "INSERT INTO lista (titulo, descricao, priority, categoria) VALUES (%s, %s, %s, %s)"
            values_query = (titulo, descricao, prioridade, categoria)

        self.cursor.execute(sql_query, values_query)

        

    def readList(self, idLista : int = None, titulo : str = None) -> tuple:
        '''
        Ler/ver lista
        '''
        if idLista is None and titulo is None:
            erro = 'Favor digite o titulo ou o id de uma lista.'
            return erro
        
        sql_query = "SELECT * FROM lista WHERE id = %s OR titulo = %s"
        values_query = (idLista)
        self.cursor.execute(sql_query, values_query)
        
        data_list = self.cursor.fetchall()

        return data_list

    def updateList(self):
        '''
        Atualizar lista
        '''
        pass

    def deleteList(self, idLista : int = None):
        '''
        Excluir lista
        '''
        self.cursor.execute('DELETE * FROM lista WHERE id = %s', (idLista))
        data_list = self.cursor.fetchall()

        return data_list
    
    def getAllCategories(self) -> tuple:
        '''
        Listar todas as categorias
        '''
        self.cursor.execute('SELECT categoria FROM lista')
        data_list = self.cursor.fetchall()

        return data_list
        

    def getAllLists(self):
        '''
        Listar todas as listas
        '''

        self.cursor.execute(('SELECT * FROM lista'))
        data_list = self.cursor.fetchall()

        return data_list

    def getItemsByList(self, idList : int = None) -> tuple:
        '''
        Listar Items de uma lista específica
        '''
        self.cursor.execute("SELECT id, textItem, concluido FROM itens WHERE idLista = %s", (idList))
        data_list = self.cursor.fetchall()

        return data_list

    def toggleItemCompletedStatus(self, idItem):
        '''
        Marcar/Desmarcar Item como concluído
        '''
        self.cursor.execute('SELECT concluido FROM itens WHERE id = %s', (idItem))
        data_list = self.cursor.fetchall()


        sql_query = "UPDATE itens SET concluido = %s WHERE id = %s"
        values_query = (0 if data_list[0][0] == 1 else 1, idItem)

        self.cursor.execute(sql_query, values_query)

    def filterListsByCategory(self, categoria : str = None) -> tuple:
        '''
        Filtrar listas por Categoria
        '''

        self.cursor.execute('SELECT * FROM lista WHERE categoria = %s', (categoria))
        data_list = self.cursor.fetchall()

        return data_list
    
    def sortListsByDueDate(self) -> tuple:
        '''
        Ordenar listas por data de vencimento
        '''
        self.cursor.execute('SELECT * FROM lista ORDER BY data_vencimento')
        data_list = self.cursor.fetchall()

        return data_list

    def sortListsByPriority(self) -> tuple:
        '''
        Ordenar listas por prioridade
        '''
        self.cursor.execute('SELECT * FROM lista ORDER BY priority')
        data_list = self.cursor.fetchall()

        return data_list

    def deleteCompletedItems(self, idList : str = None):
        '''
        Excluir todos os itens concluídos de uma lista
        '''
        self.cursor.execute('DELETE * FROM itens WHERE idLista = %s', (idList))
        data_list = self.cursor.fetchall()
        
        return data_list

    def searchListsByKeyword(self, titleList : str = None, descriptionList : str = None) -> tuple:
        '''
        Buscar listas por título ou Descrição
        '''
        if titleList is None and descriptionList is None:
            erro = 'Favor digite o titulo ou a descrição de uma lista.'
            return erro

        self.cursor.execute("SELECT * FROM lisa WHERE titulo = %s OR descricao = %s", (titleList, descriptionList)) 

        data_list = self.cursor.fetchall()

        return data_list


class ItensList(ListaTarefas):
    def __init__(self, idList) -> None:
        super().__init__()

        self.idList = idList

    def createItem(self, idList : int, textItem: str, concluded: bool):
        sql_query = "INSERT INTO itens (idLista, textItem, concluido) VALUES (%s, %s, %s)"
        values_query = (idList, textItem, concluded)

        self.cursor.execute(sql_query, values_query)

    def readItem(self, idItem):
        self.cursor.execute("SELECT textItem, concluido FROM itens WHERE idLista = %s AND id = %s", (self.idList, idItem))
        data_list = self.cursor.fetchall()

        return data_list

    def updateItem(self, idItem):
        pass

    def deleteItem(self):
        pass

        
class Menu:
    def __init__(self) -> None:
        self.classLists = ListaTarefas()

        curses.wrapper(self.mostrarListas)
    

    def menu_create_list(self, stdscr):
        inputs_text = ['Titulo: ', 'Drescriçao: ', 'Prioridade(Sim ou Não): ', 'Categoria: ', 'Data de Vencimento(AAAA-MM-DD): ']
        list_answer = list()

        for i, input_text in enumerate(inputs_text):
            stdscr.clear()
            stdscr.addstr(0,0, input_text)
            if i == 2:
                k = True
                opcoes = [
                    'Sim',
                    'Não'
                ]
                cursor_y = 0

                while (k):
                    stdscr.clear()
                    stdscr.addstr(0,0, "Prioridade?")
                    for i, opcao in enumerate(opcoes):
                        x = 2
                        y = i + 2

                        stdscr.addstr(y, x, opcao)
                        if i == cursor_y:
                            stdscr.attron(curses.A_REVERSE)
                            stdscr.addstr(y,x, opcao)
                            stdscr.attroff(curses.A_REVERSE)
                    
                    k = stdscr.getch()

                    if k == curses.KEY_UP and cursor_y > 0:
                        cursor_y -= 1
                    elif k == curses.KEY_DOWN and cursor_y < len(opcoes) - 1:
                        cursor_y += 1
                    elif k == 10:
                        if cursor_y == 0:
                            list_answer.append(True)
                            k = False
                        elif cursor_y == 1:
                            list_answer.append(False)
                            k = False
            elif i == 3:
                k = True
                cursor_y = 0

                categorias = self.classLists.getAllCategories()
                opcoes = list(set(list(categorias)))

                opcoes.append(('[+] Criar Categoria',))

                while k:
                    stdscr.clear()
                    stdscr.addstr(0,0, 'Categorias:')
                    for i, opcao in enumerate(opcoes):
                        opcao = opcao[0]
                        x = 2
                        y = i + 2

                        stdscr.addstr(y, x, opcao)

                        if i == cursor_y:
                            stdscr.attron(curses.A_REVERSE)
                            stdscr.addstr(y,x, opcao)
                            stdscr.attroff(curses.A_REVERSE)
                    
                    k = stdscr.getch()

                    if k == curses.KEY_UP and cursor_y > 0:
                        cursor_y -= 1
                    elif k == curses.KEY_DOWN and cursor_y < len(opcoes) - 1:
                        cursor_y += 1
                    elif k == 10:
                        if cursor_y != len(opcoes) - 1:
                            list_answer.append(opcoes[cursor_y])
                            k = False
                        else:
                            stdscr.clear()
                            stdscr.addstr(0,0, 'Nome da nova categoria: ')
                            stdscr.refresh()
                            curses.echo()
                            list_answer.append(stdscr.getstr(0,len('Nome da nova categoria:')).decode('utf-8'))
                            curses.noecho()
                            k = False
            else:
                stdscr.refresh()
                curses.echo()
                list_answer.append(stdscr.getstr(0,len(input_text)).decode('utf-8'))
                curses.noecho()
        
        self.classLists.createList(*list_answer)
    
    def mostrarListas(self, stdscr):
            stdscr.erase()
            altura, largura = stdscr.getmaxyx()

            cabecalho = ['id', 'Titulo', 'Descrição', 'Prioridade', 'Categoria', 'Data Vencimento']

            linhas = self.classLists.getAllLists()
            itens_list = self.classLists.getItemsByList(linhas[0][0])

            largura_coluna = largura // len(cabecalho)

            for i, titulo in enumerate(cabecalho):
                stdscr.addstr(2, i * largura_coluna, f"{titulo:^{largura_coluna}}")

            # Área para mostrar os detalhes da lista.
            detalhes_area_y = len(linhas) + 5

            stdscr.refresh()
            curses.echo()

            cursor_y = 0
            k = 0
            checkUpdateList = False

            while k != ord("q"):  # 10 é o código ASCII para a tecla Enter.
                stdscr.clear()
                stdscr.refresh()                

                if k == curses.KEY_UP and cursor_y > 0:
                    cursor_y -= 1
                    itens_list = self.classLists.getItemsByList(linhas[cursor_y][0])
                elif k == curses.KEY_DOWN and cursor_y < len(linhas) - 1:
                    cursor_y += 1
                    itens_list = self.classLists.getItemsByList(linhas[cursor_y][0])
                elif k == ord('c'): # Tecla para chamar a função para adicionar item na lista.
                    self.criarItem(stdscr, linhas[cursor_y][0])
                elif k == 10:
                    checkUpdateList = True
                elif k == ord('l'):
                    self.menu_create_list(stdscr)
                elif k == ord('e'):
                    pass

                stdscr.clear()

                # Exibe as opções da lista
                for i, titulo in enumerate(cabecalho):
                    stdscr.addstr(2, i * largura_coluna, f"{titulo:^{largura_coluna}}")

                for j, linha in enumerate(linhas):
                    for i, valor in enumerate(linha):
                        if i == 5 and isinstance(valor, date):
                            valor = valor.strftime('%Y-%m-%d')
                        elif i == 5 and valor is None:
                            valor = 'NULL'

                        # Destaca a linha selecionada
                        if j == cursor_y:
                            stdscr.attron(curses.A_REVERSE)

                        stdscr.addstr(j + 3, i * largura_coluna, f"{valor:^{largura_coluna}}")

                        if j == cursor_y:
                            stdscr.attroff(curses.A_REVERSE)

                # Exibe os detalhes da lista selecionada abaixo da lista
                self.listItensUpdateConclued(stdscr, detalhes_area_y, itens_list, largura_coluna, linhas[cursor_y][0], checkUpdateList)
                
                

                opcoes = [
                    '[Q] Sair',
                    '[C] Adicionar Item',
                    '[ENTER] Modificar itens',
                    '[E] Excluir Lista',
                    '[L] Adicionar Lista'
                ]

                largura_total = sum(len(opcao) for opcao in opcoes) + len(opcoes) - 1

                x_pos = 0

                for opcao in opcoes:
                    stdscr.addstr(curses.LINES - 1, x_pos, opcao)
                    x_pos += len(opcao) + 2
                


                stdscr.refresh()
                k = stdscr.getch()

                checkUpdateList = False

            curses.noecho()
        
    def listItensUpdateConclued(self, stdscr, detalhes_area_y, itens_list, largura_coluna, idList, checkUpdateList = False):
        if not checkUpdateList:
            stdscr.addstr(detalhes_area_y, 0, "Itens da lista:")
            detalhes_lista = itens_list
            for i, valor in enumerate(detalhes_lista):
                stdscr.addstr(detalhes_area_y + i + 1, 0, f"{valor[1]} - {'Concluído' if valor[2] == 1 else 'Não concluído'}")
        
        else:
            k = 0
            cursor_y = 0

            while True:
                stdscr.refresh()                

                for j, valor in enumerate(itens_list):
                    if j == cursor_y:
                        stdscr.attron(curses.A_REVERSE)
                    
                    stdscr.addstr(detalhes_area_y + j + 1, 0, f"{valor[1]} - {'Concluído' if valor[2] == 1 else 'Não concluído'}")

                    if j == cursor_y:
                        stdscr.attroff(curses.A_REVERSE)

                
                k = stdscr.getch()


                if k == curses.KEY_UP and cursor_y > 0:
                    cursor_y -= 1
                elif k == curses.KEY_DOWN and cursor_y < len(itens_list) - 1:
                    cursor_y += 1
                elif k == ord('q'):
                    stdscr.attroff(curses.A_REVERSE)
                    break  # Saia do loop se 'q' for pressionado
                
                
                if k == 10: # marcar/desmarcar como concluido
                    self.classLists.toggleItemCompletedStatus(itens_list[cursor_y][0])

                    curses.curs_set(0)
                    stdscr.clear()
                    self.alert(stdscr,"Item alterado com sucesso.")
                    curses.curs_set(1)
                    stdscr.clear()
                    stdscr.refresh()
                    break

                opcoes = [
                    f'[Q] Voltar',
                    '[ENTER] Marcar/Desmarcar como concluído'
                ]

                stdscr.addstr(curses.LINES - 1, 0, opcoes[0])
                stdscr.addstr(curses.LINES - 1, len(opcoes[0]) + 2, opcoes[1])
        

    def criarItem(self, stdscr, idLista):
        stdscr.clear()

        k = 0
        cursor_y = 0

        stdscr.addstr(0,0, "Titulo do item: ")
        stdscr.refresh()
        curses.echo()
        titleItem = stdscr.getstr(0, len("Titulo do item:")).decode('utf-8')
        curses.noecho()

        classListItem = ItensList(idLista)

        classListItem.createItem(idLista, titleItem, False)

    def alert(self, stdscr, mensagem):
        stdscr.clear()
        stdscr.refresh()

        altura, largura = stdscr.getmaxyx()

        altura_alerta = 5
        largura_alerta = 30
        y = (altura - altura_alerta) // 2
        x = (largura - largura_alerta) // 2

        alerta_win = curses.newwin(altura_alerta, largura_alerta, y, x)

        alerta_win.addstr(2, 2, mensagem)

        stdscr.refresh()
        alerta_win.refresh()

        time.sleep(2)

        alerta_win.clear()
        alerta_win.refresh()

Menu()




