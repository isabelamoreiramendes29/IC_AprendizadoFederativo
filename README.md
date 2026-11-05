# Aprendizado Federado com LoRa e Compressão de Dados para Sistemas IoT Embarcados

Iniciação Científica de Isabela Moreira no WAI-Lab (Inatel).

O foco da IC é o aprendizado federado em microcontroladores com rádio LoRa. Os dados dos sensores ficam em cada placa, e o que viaja pelo rádio são os parâmetros do modelo, que precisam ser comprimidos. As perguntas principais são a colisão de pacotes, o consumo de energia e a taxa de compressão.

Por enquanto, este repositório guarda o primeiro estudo da IC: um teste de compressão sem perda com dados reais de sensores (INMET), feito no computador.

## O que tem aqui

| Pasta ou arquivo | O que é |
|---|---|
| `teste_compressao/teste_compressao.py` | O programa do teste (Python 3, sem bibliotecas extras) |
| `teste_compressao/dados/` | Os dados do INMET usados no teste |
| `teste_compressao.md` | Como o teste foi feito e os resultados |
| `explicacao_algoritmos.md` | Como funciona cada método de compressão |
| `explicacao_diferenca_huffman.md` | Como a diferença + Huffman funciona no código |

## Como rodar o teste

Precisa do Python 3.

```
cd teste_compressao
python teste_compressao.py dados/INMET_SE_MG_A531_MARIA_DA_FE_2025.CSV exemplo
```

O `exemplo` mostra, passo a passo, o dia mais frio do ano. Sem essa palavra, o programa roda o teste completo, com blocos de 6, 12 e 24 horas.

## Resultado (blocos de 24 horas)

| Método | Bytes por dia | Redução em relação ao texto |
|---|---|---|
| Texto | 189 | 0% |
| LZW | 130 | 31% |
| Huffman | 112 | 40% |
| Binário | 72 | 62% |
| Diferença | 49 | 74% |
| Diferença + Huffman | 35 | 81% |

Todos os métodos são sem perda: o programa descomprime cada dia e confere se voltou igual.

O teste mede só o tamanho dos dados. Ele não usa rádio e não mede energia nem tempo.

## Dados

Dados históricos do INMET (Instituto Nacional de Meteorologia), estação automática A531, Maria da Fé (MG), 2025.
