# Macaw o Web Crawler!

## Executando o projeto

- Instalar dependencias: `pip install -r requirements.txt`
- Executar o projeto: `python -m macaw [output-type]`
- Executar os testes: `python -m unittest tests/*.py`

## Argumentos

### output-type
- `--print`: Imprime os resultados no terminal
- `--save_json`: Salva os resultados num arquivo `plans.json`

## Os pensamentos que tive enquanto construia o projeto (diferente por commit)

### Commit Etapa 1: página-alvo, imprime na tela
Minha ideia inicial foi fazer o mínimo pra imprimir na tela.
Uma das primeiras prioridades foi salvar o HTML da página
numa pasta local (chamei de cache) pra evitar ficar fazendo
vários requests.

Parte do meu tempo inicial foi pesquisando como que funciona
um web crawler, boas práticas e algumas dicas. Depois disso resolvi
começar a implementar.

Notei que a primeira página inicial (chamei de `landing_page` no código) não continha os dados necessários, mas ela tinha um link pra página de preços.
Resolvi então usar o `parsel` pra extrair todas as tags `<a>` com `cloud` e `pricing` no `href` (eu olhei antes pra escolher essas palavras chave iniciais)

Isso me deu a ideia de, futuramente, implementar o código de uma forma que, caso o HTML não tenha o conteúdo de preços, o crawler vai buscar os links com as palavras chave. Porém, pra essa primeira etapa, resolvi focar e só em pegar o primeiro link que aparecer.

Tendo a página com os dados que eu queria. Fiz uma função simples para
extrair os dados e armazená-los numa lista com a seguinte estrutura (pelo que eu li, listas são mais performáticas que dicionários para iterar em Python):


```python
[
    [
        {
            'type': 'Storage',
            'value': '500GB'
        },
        {
            'type': 'Bandwidth',
            'value': '5.00TB'
        }
    ],
    [
        {
            'type': 'Storage',
            'value': '700GB'
        },
        {
            'type': 'Bandwidth',
            'value': '5.00TB'
        }
    ]
]
```
em que:
- Cada item da lista é um `plano` que está sendo vendido. 
- Cada plano é composto de uma lista de `recursos` contendo:
    - `type` é o tipo do recurso
    - `value` é a unidade do recurso (GB, TB, $).

A maior dificuldade nessa primeira etapa foi a construção da regex... Coloquei um tempo limite para tentar criar uma regex geral que retornasse somente os dados necessários, mas como não consegui, optei por deixar as 3 regexes separadas.

Quando os dados já estavam sendo impressos na tela, resolvi escrever uns testes pra validar se os valores tavam corretos (não estavam >.>). Com os resultados dos testes fui refinando o código. 

### Commit Etapa 1: página-alvo, imprime na tela, salva em json

renomeei o `handle_cli` para `get_save_function` e o fiz retornar uma função responsável por tratar o output. Provavelmente vou renomear o `utils.py`.

Também corrigi um bug em que argumentos de linha de comando inválidos ainda eram processados, o `match` estava sem um caso padrão

### Commit Etapa 1: feat: update output format

Pensando melhor, resolvi alterar o formato que os dados estão sendo escritos,
até pra facilitar a escrita em CSV. Faz mais sentido os dados estarem todos dentro de um único objeto. O arquivo final também fica bem menor.

Novo formato:
```python
[ # list of plans
    {
        "vCPU": "1",
        "Memory": "1GB",
        "Bandwidth": "2.00TB",
        "Storage": "25GB",
        "/mo": "$6.00",
        "/hr": "$0.009"
    },
]
```

### Commit Etapa 1: feat: normalize output keys

Para padronizar o nome das colunas, eu resolvi fazer uma função para fazer o `normalize` das chaves. Os maiores motivos disso foram:
- `CPU` e `vCPU` compartilham a mesma chave `CPU / VCPU`
- Outros campos podem variar de nome, mas com esse `normalize`, fica fácil mapeá-los
para um nome comum, deixando comparáveis os dados de futuras páginas.

essa função de `normalize` agora é aplicada antes do processo de escrita.