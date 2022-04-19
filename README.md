# Macaw o Web Crawler!

![Actions Status](https://github.com/Leinvedan/macaw/actions/workflows/python-app.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green)


<p align="center">
    <img src="./static/icon.svg" width="300" height="300" style="display:flex align-self: center">
</p>

> SVG de: https://www.svgrepo.com/svg/140753/macaw

# Índice
1. [Sobre](#sobre)
2. [Como funciona](#como-funciona)
3. [Executando o projeto](#executando-o-projeto)
    * [argumentos](#argumentos)
    * [com python](#com-python)
    * [com docker](#com-docker)
4. [Argumentos](#argumentos)


# Sobre

Macaw é um `webcrawler` que utiliza de seus extratores para extrair dados de páginas específicas.

# Como funciona

Para extrair os dados de uma página, é necessário definir uma configuração no arquivo `configs.py`, ex:
```python
MY_CONFIG = {
    'origin': 'Test Page',              # Nome / identificador
    'run_spider': parse_test_html,      # função python que vai extrair os dados
    'url': {                            # primeira URL que será acessada
        'domain': 'https://www.test.com',
        'path': '/products/',
    },
    'link_query': {                     # Consulta aplicada para buscar
                                        # outros links dentro da primeira página
        'keywords': ['/pricing', 'cloud'],# Palavras chave contidas no `link`
        'xpath': HREF_XPATH # Xpath do link, como por exemplo, um xpath para buscar:
                            # <a href=""> ou <script src="">
    }
}
```

Cada extrator é chamado individualmente de `spider` e seu código python fica na pasta `macaw/extractors/spiders`. 

A função de extração receberá uma string com todo o `html` ou `js` da página. ela(função) deve retornar uma lista de dicionários, que serão posteriormente processados pelo `normalizer`.

As chaves do dicionário precisam estar registradas no `normalizer`, caso contrário, elas serão ignoradas. Isso garante que a base de dados resultante estará sempre normalizada.

# Executando o projeto

**`Macaw`** pode ser executado tanto com argumentos de linha de comando, quanto de forma iterativa.

## Argumentos

| Argumento                    | Descrição                    |
|------------------------------|------------------------------|
| `--print`    | Imprime os resultados no terminal            |
| `--save_json`| Salva os resultados no arquivo  `plans.json` |
| `--save_csv` | Salva os resultados num arquivo  `plans.csv` |

## Com Python

- Instalar dependencias: `make setup`
- Executar os testes: `make test`
- Executar lint: `make lint`
- Executar o projeto:
  - Com argumentos: `python -m macaw [args]`
  - Forma iterativa: `python -m macaw` ou `make run`

### Exemplos:
```bash
python -m macaw --print
python -m macaw --save_csv
python -m macaw --save_json
```

> Obs: Docker e makefile só dão suporte à execução iterativa

## Com docker
- Build da imagem: `make docker-build`
- Executar a imagem: `make docker-run`
