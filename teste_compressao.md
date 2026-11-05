# Primeiro teste de compressão (sem IA)

Feito em 02/11/2026, no computador, com dados reais do INMET.

## Como foi o teste

- **Dados:** estação do INMET em **Maria da Fé (MG)**, código A531, ano de 2025, de hora em hora.
  - Medidas usadas: **temperatura** (com uma casa decimal) e **umidade** (número inteiro).
  - Escolhi essa estação porque é a mais completa do Sul de Minas: faltam só 12 horas de temperatura no ano. Ela também tem clima de geada: a mínima foi −2,2 °C, com 81 horas abaixo de 3 °C.
- **Bloco:** o nó junta as leituras e manda de uma vez. Testei blocos de **6, 12 e 24 horas**.
- **Janeiro** foi usado só para montar a tabela fixa do Huffman. O teste foi de **fevereiro a dezembro**.
- Cada bloco é comprimido sozinho, porque cada pacote precisa ser entendido mesmo se outro se perder.
- **Todos os blocos foram descomprimidos e conferidos: voltaram exatamente iguais.** Ou seja, todos os métodos são sem perda.

## Os métodos

| Método | O que faz |
|---|---|
| Texto | As leituras escritas como letras, por exemplo `17.2;99`. É o ponto de partida, sem compressão, como as mensagens do WAI-Lab e do C2 |
| Binário | Os números guardados do jeito que o computador guarda: 2 bytes para a temperatura e 1 para a umidade. Também não comprime nada |
| LZW | O algoritmo que foi melhor no WAI-Lab e no C2, aplicado ao texto |
| Huffman | Aplicado ao texto, mandando a tabela junto no pacote (como no WAI-Lab) |
| Diferença | Manda a primeira leitura inteira e depois só a diferença para a leitura anterior |
| Diferença + Huffman | A diferença, comprimida com um Huffman de tabela fixa. A tabela é calculada com os dados de janeiro e fica guardada nos dois lados, então não viaja no pacote |

## Resultado com blocos de 24 horas (1 dia)

| Método | Bytes por dia | Redução em relação ao texto | Pacotes por dia em SF12 |
|---|---|---|---|
| Texto | 189 | — | 4 |
| LZW | 130 | 31% | 3 |
| Huffman | 112 | 40% | 3 |
| Binário | 72 | 62% | 2 |
| Diferença | 49 | 74% | 1 |
| **Diferença + Huffman** | **35** | **81%** | **1** |

Em SF7, todos cabem em 1 pacote por dia, porque o pacote é maior (222 bytes). Em SF12, o pacote é de 51 bytes.

## Efeito do tamanho do bloco

| Método | 6 horas | 12 horas | 24 horas |
|---|---|---|---|
| LZW | 14% | 25% | 31% |
| Huffman | 2% | 27% | 40% |
| Diferença | 73% | 74% | 74% |
| Diferença + Huffman | 78% | 81% | 81% |

(Redução em relação ao texto.)

## O que aprendemos

1. **Só escrever os números em binário, em vez de texto, já reduz 62%.** É mais do que o LZW (31%) e o Huffman (40%) conseguiram. Ou seja, o resultado depende muito de **com o que se compara**. O WAI-Lab e o C2 compararam com texto.
2. **O LZW comprimiu bem menos aqui** (31%) do que no WAI-Lab (cerca de 60%) e no C2 (70%). O LZW precisa de trechos repetidos, e um bloco curto só de números tem pouca repetição. Com blocos maiores ele melhora.
3. **A diferença ganhou de todos**, porque a temperatura e a umidade mudam devagar de uma hora para outra. A diferença + Huffman reduziu 81% e coube em **1 pacote por dia em SF12**, contra 4 do texto. Em SF12, menos pacotes significa menos energia.
4. **Bloco maior comprime mais, mas o dado demora mais para chegar.** Com bloco de 24 horas, o nó espera um dia inteiro para enviar. A diferença funciona bem até com blocos de 6 horas.

## O que isso significa para a IA

- A diferença é um **"palpite sem IA"**: ela chuta que a próxima leitura vai ser igual à anterior.
- A **"IA que adivinha"** precisa fazer palpites melhores do que esse para valer a pena.
- Então a meta da IA é ficar **abaixo de 35 bytes por dia**, gastando pouca energia para isso.

## Limites deste teste

- Foi feito **no computador**. Ele mostra quanto cada método comprime, mas **não mede energia nem tempo na placa**.
- Usei uma estação e um ano. Os números podem mudar com outros dados.
- O formato do texto foi escolhido por mim. O WAI-Lab e o C2 usaram mensagens diferentes, então as porcentagens não são diretamente comparáveis.

## Exemplo: o dia mais frio (noite de 29 para 30/07/2025)

O dia começa às 21h de 29/07, porque o INMET marca as horas no horário universal, 3 horas à frente de Brasília.

- **As leituras:** 4,8 °C e 92%; 3,5 °C e 96%; 2,8 °C e 97%... A temperatura chegou a **−2,2 °C** às 7h.
- **Texto:** cada hora vira algo como `4.8;92` mais a quebra de linha, ou seja, 7 bytes. O dia inteiro: **187 bytes**.
- **Binário:** 3 bytes por hora (2 da temperatura e 1 da umidade). O dia inteiro: **72 bytes**.
- **LZW:** procura pedaços que se repetem no texto (como `;99`, que aparece em várias horas) e troca cada um por um código curto: **131 bytes**.
- **Huffman:** dá códigos curtos para os caracteres que aparecem muito (como `;` e `9`) e mais longos para os raros, mas precisa mandar a tabela junto: **114 bytes**.
- **Diferença:** manda a primeira leitura inteira e depois só quanto mudou. De 4,8 para 3,5 vira −1,3; de 3,5 para 2,8 vira −0,7. Cada diferença cabe em 1 byte: **49 bytes**.
- **Diferença + Huffman:** as diferenças pequenas aparecem muito e ganham códigos bem curtos: **37 bytes**.
- **Conferência:** todos voltaram exatamente iguais.

**Onde a IA pode ajudar:** às 8h fazia 1,0 °C e às 9h já fazia 10,2 °C, porque o sol esquentou rápido depois da geada. A diferença teve que mandar +9,2, um número grande. Uma IA que aprendeu que de manhã esquenta poderia chutar perto disso e mandar um número pequeno.

## Onde está o programa

- Programa: `teste_compressao/teste_compressao.py` (em Python, sem nenhuma biblioteca extra).
- Dados: `teste_compressao/dados/INMET_SE_MG_A531_MARIA_DA_FE_2025.CSV` (cópia do arquivo do INMET).
- Para rodar, dentro da pasta `teste_compressao`:
  - resultado completo: `python teste_compressao.py dados/INMET_SE_MG_A531_MARIA_DA_FE_2025.CSV`
  - passo a passo do dia mais frio: `python teste_compressao.py dados/INMET_SE_MG_A531_MARIA_DA_FE_2025.CSV exemplo`

## Próximos passos

1. Testar a "IA que adivinha" no computador e ver se ela ganha da diferença + Huffman.
2. Repetir com outras estações (por exemplo, Machado e Varginha) e outros tipos de dado (chuva, vento).
3. Depois, rodar na placa e medir a energia com o INA219.
