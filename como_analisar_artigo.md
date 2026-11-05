# Como analisar um artigo

Roteiro criado em 03/11/2026. A ideia é responder 7 perguntas, sempre com frases curtas.

## Em que ordem ler

Não precisa ler do começo ao fim.
1. **Título e resumo** (abstract): do que trata.
2. **Figuras e tabelas**: muitas vezes mostram o resultado mais rápido que o texto.
3. **Conclusão**: o que os autores acham que provaram e o que admitem que falta.
4. **Só depois**, a parte de "como foi feito" (método, *methodology*, *experimental setup*) e a de resultados.

## As 7 perguntas

| # | Pergunta | Dica |
|---|---|---|
| 1 | **Qual é o problema?** | Uma frase. Se não der para dizer em uma frase, releia o resumo. |
| 2 | **O que eles propõem ou comparam?** | O "jeito novo" deles, ou o que está sendo comparado com o quê. |
| 3 | **Como testaram?** | Foi em placa de verdade ou só simulado no computador? Que placa, que rádio, que dados? |
| 4 | **O que mediram e como?** | A energia foi **medida** com sensor de corrente ou **estimada** por fórmula? Quantas vezes repetiram? |
| 5 | **Quais são os resultados principais?** | 2 ou 3 números. **Confira pelo menos uma conta**: às vezes os números não batem. |
| 6 | **O que falta?** | O que os próprios autores admitem e o que você percebeu. |
| 7 | **O que isso muda para a IC?** | Usar a ideia, comparar com ele ou evitar o erro dele. |

## Sinais de que o artigo é confiável

- Testou em **placa e rádio de verdade**, não só em simulação.
- **Mediu** a energia com sensor, em vez de calcular por fórmula.
- **Repetiu** os testes várias vezes e mostrou a média.
- Os dados ou o código estão **abertos**, então dá para conferir.
- Os números **batem** quando você refaz uma conta.
- Os autores **admitem os limites** do trabalho.

Quanto mais desses sinais, mais dá para confiar.

## Exemplo: o artigo do WAI-Lab (C1, Dias et al. 2026)

| # | Pergunta | Resposta |
|---|---|---|
| 1 | Problema | O rádio é o que mais gasta energia num aparelho LoRa. Comprimir os dados pode diminuir esse gasto. |
| 2 | O que comparam | 7 compressores sem perda: clássicos (Huffman, LZW, BSC) e com IA (CMIX, PAQ8PX, GMIX, LSTM-compress). |
| 3 | Como testaram | Raspberry Pi 5 com rádio RFM95W (o mesmo chip SX1276 da TTGO), em 915 MHz, SF7 e SF12. Dados em texto: GPS (de um repositório público) e duas listas de mensagens criadas pelos autores. Também fizeram um teste ao ar livre, a 1,38 km. |
| 4 | O que mediram | Energia **medida** com INA219, lido por um Arduino separado. Cada teste foi repetido **100 vezes**. |
| 5 | Resultados | O LZW foi o mais eficiente: economizou até **7,41%** de energia. As IAs comprimiram mais, mas demoraram tanto que **gastaram mais do que economizaram**. |
| 6 | O que falta | Os próprios autores dizem que: não usaram microcontrolador (o Raspberry é bem mais forte); não consideraram reenvios de pacote; não mediram a descompressão. Também não há aprendizado federado, e parte dos dados foi criada por eles. |
| 7 | O que muda para a IC | É o ponto de partida. A IC faz o que eles pedem como trabalho futuro: levar para microcontrolador (eles citam o ESP32), usar IA leve e misturar IA com algoritmo. |

Sinais de confiança: placa real ✔, energia medida ✔, 100 repetições ✔, código aberto ✔, admite limites ✔.

## Para treinar

Faça as 7 perguntas com o **C13** (`artigos/C13_Hanumanthaiah2019_DeltaRLE_SemPerda.pdf`). Ele tem só 5 páginas.

Dica para a pergunta 5: na Tabela I, divida "Compressed Data" por "Original Data" e compare com o "CR(%)" que eles escreveram.
