# Ideias de aplicação real da IC

**Data:** 15/10/2026.

**Frase-resumo da IC:** juntar tudo (microcontrolador, LoRa de verdade e compressão dos dados dos sensores) e medir a energia de verdade, comparando se é melhor comprimir com IA ou com um algoritmo simples.

Em todas as aplicações abaixo, o sistema funciona assim:
- **Nos dias normais:** os sensores treinam a IA e trocam os modelos pelo LoRa, com calma (isso leva horas).
- **Na hora do perigo:** o modelo já está pronto e só **prevê**. Pelo LoRa vai só um **alerta curto**, que cabe num pacote.

---

## 1. Prever geada em lavouras de café (Sul de Minas)

**Problema:** a geada pode destruir uma safra numa noite. Com algumas horas de aviso, o produtor consegue se proteger.

**Como funcionaria:**
- Sensores no cafezal (bateria ou painel solar) medem temperatura e umidade.
- Cada sensor comprime os dados e treina uma IA para prever geada.
- O modelo vai pelo LoRa até uma antena que alcança várias fazendas.
- O servidor junta os modelos da região inteira, sem ninguém mostrar os próprios dados, e manda um alerta quando houver risco de geada.

**O que o produtor faz com o alerta:** irrigar, deixar o solo úmido e limpo entre as fileiras e cobrir as mudas. A proteção é com o produtor e o agrônomo; para detalhes, consultar a Embrapa Café ou a EPAMIG.

**Bônus:** com sensores espalhados, dá para fazer um mapa dos pontos da fazenda que gelam primeiro.

---

## 2. Alerta de enchente em rios (chuva forte)

**Problema:** em chuvas fortes, rios sobem rápido e alagam bairros e estradas.

**Como funcionaria:**
- Sensores ao longo do rio medem o nível da água e a chuva (pluviômetro).
- Cada ponto aprende o próprio comportamento. Exemplo: "aqui o rio sobe 1 metro duas horas depois de uma chuva forte".
- Os modelos se juntam numa previsão para o rio inteiro.

---

## 3. Risco de deslizamento em encostas (chuva forte)

**Problema:** chuva demais encharca o solo das encostas e pode causar deslizamentos.

**Como funcionaria:**
- Sensores na encosta medem a umidade do solo, a chuva acumulada e a inclinação do terreno.
- A IA aprende quando o solo daquela encosta fica perigoso e avisa antes.

---

## Por que chuva forte combina muito com a IC

| Parte da IC | Na chuva forte |
|---|---|
| **Energia** | Muito crítica. O painel solar quase não carrega e muitas vezes falta luz, então o sensor precisa durar só com a bateria. |
| **LoRa** | A internet e o celular costumam cair. O LoRa funciona com bateria, alcança longe e sofre pouco com a chuva. |
| **Compressão dos dados** | Na tempestade os sensores medem com mais frequência, e comprimir evita encher a memória e gastar energia enviando. |
| **Aprendizado federado** | Cada ponto se comporta de um jeito, e os modelos juntos aprendem com todos. |

---

## Outras ideias (mais curtas)

- **Concreto em obras:** sensores dentro do concreto medindo a temperatura durante a cura, em obras sem internet. É o mesmo tipo de dado do projeto Cemtinel (FETIN).
- **Criação de animais:** sensores em galpões medindo temperatura e gases.

---

## Para falar ao professor

> "Uma aplicação real seria prever geada no café ou avisar enchentes e deslizamentos. Os sensores ficam no campo, sem internet e funcionando com bateria, então a compressão dos dados e a economia de energia são essenciais. O LoRa leva as informações por quilômetros, e o aprendizado federado deixa cada lugar aprender sem expor os próprios dados."

Na IC não é preciso instalar tudo no campo. Dá para testar com algumas placas no laboratório, usando dados reais de clima ou de rios.
