# Macaw o Web Crawler!

## Executando o projeto

**`Macaw`** pode ser executado tanto com argumentos de linha de comando, quanto de forma iterativa.

### Com Python

- Instalar dependencias: `make setup`
- Executar os testes: `make test`
- Executar lint: `make lint`
- Executar o projeto: 
  - Com argumentos: `python -m macaw [args]`, ex: `python -m macaw --save_json`
  - Iterativa: `python -m macaw` ou `make run`

#### Exemplos:
```bash
python -m macaw --print
python -m macaw --save_csv
python -m macaw --save_json
```

> Obs: Docker e makefile só dão suporte à execução iterativa

### Com docker
- Build da imagem: `make docker-build`
- Executar a imagem: `make docker-run`

### Argumentos

| Argumento                    | Descrição                    |
|------------------------------|------------------------------|
| `--print`    | Imprime os resultados no terminal            |
| `--save_json`| Salva os resultados no arquivo  `plans.json` |
| `--save_csv` | Salva os resultados num arquivo  `plans.csv` |

## Aviso sobre commits antigos!

Os commits antigos estão organizados em tags para facilitar a consulta. Cada tag representa o `primeiro momento` em que a feature ficou pronta.

- e1 = 1 página-alvo, imprime na tela
- e2 = 1 página-alvo, imprime na tela, salva em json
- e3 = 1 página-alvo, imprime na tela, salva em json, salva em csv
- e4 = 2 páginas-alvo

A branch `master` é a **versão final**

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

### Commit Etapa 2: página-alvo, imprime na tela, salva em json

renomeei o `handle_cli` para `get_save_function` e o fiz retornar uma função responsável por tratar o output. Provavelmente vou renomear o `utils.py`.

Também corrigi um bug em que argumentos de linha de comando inválidos ainda eram processados, o `match` estava sem um caso padrão

### Commit Etapa 2: feat: update output format

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

### Commit Etapa 2: feat: normalize output keys

Para padronizar o nome das colunas, eu resolvi fazer uma função para fazer o `normalize` das chaves. Os maiores motivos disso foram:
- `CPU` e `vCPU` compartilham a mesma chave `CPU / VCPU`
- Outros campos podem variar de nome, mas com esse `normalize`, fica fácil mapeá-los
para um nome comum, deixando comparáveis os dados de futuras páginas.

essa função de `normalize` agora é aplicada antes do processo de escrita.

### Commit Etapa 3: página-alvo, imprime na tela, salva em json, salva em csv

Ter os dados normalizados facilitou bastante a conversão pra CSV.

Como o `FIELD_NAMES` estava sendo usado em 2 arquivos e não faz muito sentido o módulo de `normalize` importar o de escrita, resolvi criar um arquivo de constantes.

### Etapa 4

### Encontrando os preços

Acessando a segunda URL e interagindo com a página, eu notei que os dados de preço não estavam no HTML inicial. 

Resolvi escolher um item da lista de `droplets` pra pesquisar, no caso foi o custo por hora de `$0.01786`, já q é um número bem difícil de se repetir em outro contexto. Resolvi também tirar o `$` da pesquisa, já q pode estar sendo inserido dinamicamente.

Comecei então a analisar os requests da página, tanto os iniciais, pós refresh com cache limpo, quanto toda vez que eu clicava na opção de `droplets`. Não encontrei nada demais. (eu deixei passar um request importante que acabei encontrando depois no Head da página)

Resolvi olhar o head do arquivo para ver os links pre carregados, se os dados não estão vindo de uma `API` via `json` nem estão no `html`, possivelmente eles estão dentro de algum `js`:

```html
<script src="/_next/static/chunks/main-38654959628e7bb7.js" defer=""></script><script src="/_next/static/chunks/pages/_app-1b7ea0bebf2194a0.js" defer=""></script><script src="/_next/static/chunks/8335-15e46ce3a62e92d2.js" defer=""></script><script src="/_next/static/chunks/5833-a7426735b42baba1.js" defer=""></script><script src="/_next/static/chunks/1072-8dbe3b36acf0ad8b.js" defer=""></script><script src="/_next/static/chunks/4207-d29ab006d4ec8bad.js" defer=""></script><script src="/_next/static/chunks/3692-afc13f431a3d4757.js" defer=""></script><script src="/_next/static/chunks/8650-522fb7ab02905351.js" defer=""></script><script src="/_next/static/chunks/pages/pricing-1a7cdb1f9a255535.js" defer="">
```

Pesquisando por esse `/_next/static/chunks` parece ser algo do `Next.js` https://github.com/vercel/next.js/discussions/17431 para carregar blocos de JS de forma lazy.

Eu já li um pouco sobre `Next.js` e sei que ele possibilita `SSR` usando `React`, isso me fez chegar na seguinte hipótese:
- No momento de renderização (no `backend`) é feito um request pra API interna da digitalocean e os dados são populados.
- O arquivo `js` é então disponibilizado numa `cdn`, facilitando o cache e diminuindo o uso de infra da API interna.
- Eu imagino que os preços não variam muito de um dia pro outro, então deixar os preços cacheados é um alto ganho de performance

Um detalhe interessante é que um dos `chunks` tem `pricing` escrito nele:
`"/_next/static/chunks/pages/pricing-1a7cdb1f9a255535.js"`

acessando esse endpoint e procurando pelo preço do droplet `0.01786` finalmente encontrei 4 ocorrências! (descobri que tinha outro produto com o mesmo preço)

```js
{app_job:{size_slug:"professional-xs",tier_slug:"professional",item_price:{usd_rate_per_month:"12.00",usd_rate_per_hour:"0.01786",usd_rate_per_second:"0.000004960317",rate_type:"UNIT_TIME",unit_type:"ITEM",time_unit:"SECOND",monthly_limits:{min_seconds:"60",max_seconds:"2419200",min_usd_amount:"0.01"}}}}
```

```js
{droplet:{size_id:"192",bandwidth_quota_gib:"2000",item_price:{usd_rate_per_month:"12.00",usd_rate_per_hour:"0.01786",usd_rate_per_second:"0.000004960317",rate_type:"UNIT_TIME",unit_type:"ITEM",time_unit:"HOUR",monthly_limits:{min_seconds:"3600",max_seconds:"2419200",min_usd_amount:"0.01"}}}}
```

Porém, as outras informações como número de CPUs, SSD, etc... estão separadas. Pesquisando por `1 intel CPU` encontrei 2 ocorrências:

```js
{priceMo:"".concat(Vt("droplet","185","usd_rate_per_month","size_id")),priceHr:"$".concat(Vt("droplet","185","usd_rate_per_hour","size_id")),cpuAmount:"1GB",cpuType:"1 Intel CPU",ssdAmount:"25GB",ssdType:"NVMe SSDs",transferAmount:"1000GB",link:"s-1vcpu-1gb-intel"}
```

Esse `Vt` é algum tipo de construtor, usando o ctrl+click do vscode, encontrei a definição.

```js
Vt = function (e, t, _, n) {
  var i = "",
    o = [],
    a = e;
  switch (e) {
    case "app_starter":
      i = "static_site_price";
      break;
    case "droplet":
      i = "item_price";
      break;
    case "dbaas":
      i = "primary_node_price";
      break;
    case "dbaasTwo":
      (a = "dbaas"), (i = "standby_node_price");
      break;
    case "dbaasThree":
      (a = "dbaas"), (i = "replica_node_price");
      break;
    default:
      (a = e), (i = "item_price");
  }
  return (
    Wt.priceData.product_prices.map(function (e) {
      return e[a] ? o.push(e[a]) : null;
    }),
    o
      .filter(function (e) {
        return t ? e[n] === t : e;
      })
      .map(function (e) {
        return e[i][_];
      })
      .reduce(function (e, t) {
        return e + t;
      })
  );
};
```
fiz uns paralelos pra facilitar o entendimento do código minificado:

Exemplo de chamada:
```js
Vt("droplet","185","usd_rate_per_month","size_id")
Vt(e, t, _, n)
```
- e = tipo do recurso
- t = ?? algum identificador, vou renomear pra value
- _ = preço por mês
- n = size_id

Traduzindo:

```js
Vt = function (resource_type, value, monthly_price, size_id) {
  var price_str = "",
    result = [],
    local_type = resource_type;
  switch (resource_type) {
    case "app_starter":
      price_str = "static_site_price";
      break;
    case "droplet":
      price_str = "item_price";
      break;
    case "dbaas":
      price_str = "primary_node_price";
      break;
    case "dbaasTwo":
      (local_type = "dbaas"), (price_str = "standby_node_price");
      break;
    case "dbaasThree":
      (local_type = "dbaas"), (price_str = "replica_node_price");
      break;
    default:
      (local_type = resource_type), (price_str = "item_price");
  }
  return (
    Wt.priceData.product_prices.map(function (price_list) {
      return price_list[local_type] ? result.push(price_list[local_type]) : null;
    }), // Mapeia a lista de preços pra uma lista que parece não usar, 
       // também dando push no array de results

    result
      .filter(function (price) {
        // se value existe (no caso, sim, 185), retorna 
        // apenas os casos que: price[size_id] === 185
        return value ? price[size_id] === value : price;
      })
      .map(function (price) {
        // mapeia pra price['item_price']['monthly_price']
        return price[price_str][monthly_price];
      })
      .reduce(function (e, t) {
        // ;-; alguma concatenação de strings
        return e + t;
      })
  );
};
```

Assim fica bem melhor de entender o que está acontecendo. Basicamente o ponto mais importante dessa função é que o misterioso `size_id` de `Vt("droplet","185","usd_rate_per_month","size_id")` é na realidade o `185`. Eu suspeitava, já q é o único número nessa chamada, mas queria ter certeza.

Esse `185` é o que vai conectar preço mensal com o resto dos preços! Inclusive o preço mensal desse `185` está aqui (pesquisando por `size_id:"185"`):

```js
{droplet:{size_id:"185",bandwidth_quota_gib:"1000",item_price:{usd_rate_per_month:"6.00",usd_rate_per_hour:"0.00893",usd_rate_per_second:"0.000002480159",rate_type:"UNIT_TIME",unit_type:"ITEM",time_unit:"HOUR",monthly_limits:{min_seconds:"3600",max_seconds:"2419200",min_usd_amount:"0.01"}}}}
```

---

Agora o problema é, essa hash `1a7cdb1f9a255535` do `chunk` `pricing-1a7cdb1f9a255535.js`. Eu não tenho garantias de que ela é única. Possívelmente com alguma alteração no JS, ou renovação do cache ela será alterada...

Pegar diretamente desses endpoints pode funcionar hoje, mas futuramente pode parar de funcionar. Então o ideal seria tirar esse link direto do Head da página.

### Modificando o código

Pensando no código que eu escrevi até aqui, seria modificar o `link_extractor` pra pegar o link de pricing do Head. Possivelmente vai ter algo bloqueando o request para o `chunk`, mas eu gostaria de testar primeiro.

depois de ter baixado o `JS`, extrair todo o conteúdo em 2 partes:
1. `{droplet:{size_id:"NUMERO"..}}`
2. `{priceMo:"".concat(Vt("droplet","NUMERO",...)...)}`

Pegar de uma `{` a outra `}` pra facilitar a conversão pra json.

Fazer o `merge` das 2 partes pelo `NUMERO`:
`Vt("droplet","NUMERO",...)...)` => `usd_rate_per_month:"6.00"`

Passar o json pelo `normalizer` atualizado e seguir o processo normal.

---

Como o código está usando o Parsel pra extrair os dados do HTML, eu vou ter que refatorar toda a parte de renderização para fora e separar os tipos de extração HTML e JS.

### Etapa 4 - feat: add xpath parameter

O número de parâmetros está ficando muito grande, agora é um bom momento pra começar a agrupar os dados num objeto de configuração:
```
domain = 'https://www.vultr.com'
path = '/products/cloud-compute/#pricing'
keywords = ['/pricing', 'cloud']
xpath = HREF_XPATH
```

### Etapa 4 - refactor: rearrange extractor and constants

Agora que a lógica de extrair os planos vai ser dividida em `js` e `html`, pensei em separar as extrações na seguinte forma:
- extractors.links => Funções para extração de links num `html`
- extractors.plans => Funções para extração de planos em `js` ou `html`

A existência do `constants` e `configs` estava ambígua, resolvi juntar ambos no `configs`.

### Etapa 4 - 2 páginas-alvo

Tirando o processo de extração dos dados do JS, todo o resto do código foi reaproveitado(leitura das configurações, normalização e gravação em arquivos).

os resultados das duas páginas são armazenados juntos nos arquivos de saída, aproveitei e adicionei mais uma coluna `source` pra dizer de onde vieram os dados.

Alguns detalhes que ainda dão pra melhorar:
1. revisar os regexes das 2 páginas
2. A parte de juntar 2 blocos de informação ficou complexa
4. Fiquei pensando se não seria melhor usar uma forma de executar o javascript e coletar os dados, mas a complexidade do projeto poderia crescer muito.

como o objeto javascript não é um json válido, tive de fazer a conversão. As bibliotecas que encontrei online `json5` e `pyjson5` tinham poucos usuários, então optei por fazer uma função de conversão simples.

O enum de js e html(PageType) já não faz mais muito sentido existir, já que as extrações são muito específicas para as páginas. Vou optar por separar os métodos de extração por tipo de página, futuramente.


## Etapa 4 - refactor: separate page extracting logic into 'spider' files

Lembrei que o Scrappy tinha uma lógica em que, cada extrator era uma `spider`. Resolvi trazer a mesma abstração para esse projeto. Cada função que possui uma lógica relacionada à extração de uma página será uma `spider`.

# Extras

Coloquei um docker para facilitar quem não usa um virtualenv. Também adicionei uma versão iterativa, em vez do programa fechar quando ele não recebe nenhum argumento.