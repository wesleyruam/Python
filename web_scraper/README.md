# Web Scraper Python

Este é um script em Python que realiza web scraping para extrair links válidos de uma página web inicial e de seus subdiretórios. 

## Funcionamento

1. **Inicialização:**
   - A classe `ExtractLinks` é inicializada com uma URL fornecida.
   - As listas `find_directories` e `processed_links` são criadas para armazenar subdiretórios encontrados e links processados, respectivamente.

2. **Requisição HTTP:**
   - O método `_getHTMLfromURL` realiza uma requisição HTTP para a URL inicial.
   - Se a requisição é bem-sucedida (código 200), o HTML é analisado usando BeautifulSoup, e os links são extraídos chamando `_getLinksFromHTML`.
   - Caso contrário, o método `_requestNewsLink` é chamado para processar um novo link.

3. **Processamento de Novos Links:**
   - `_requestNewsLink` processa os links encontrados nos subdiretórios, evitando duplicatas.
   - Se existem subdiretórios não processados, o próximo é retirado da lista, e o processo é repetido.
   - Caso contrário, a mensagem 'Todos os links foram processados' é exibida.

4. **Extração de Links:**
   - `_getLinksFromHTML` percorre os links da página HTML.
   - A validação de URLs é realizada, e subdiretórios válidos são adicionados à lista `find_directories`.

5. **Execução:**
   - O método `start` inicia o processo chamando `_getHTMLfromURL` e exibe a lista final de subdiretórios.

## Utilização

- Crie uma instância da classe `ExtractLinks` com a URL desejada.
- Chame o método `start` para iniciar o processo de extração.
- A lista resultante de subdiretórios pode ser acessada através do atributo `find_directories`.
