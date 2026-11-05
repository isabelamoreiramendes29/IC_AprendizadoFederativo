# Aprendizado Federado com LoRa e Compressão de Dados para Sistemas IoT Embarcados

Iniciação Científica de Isabela Moreira no WAI-Lab (Inatel).

A ideia é juntar, num microcontrolador com rádio LoRa:
- o aprendizado federado, em que vários nós treinam um modelo juntos sem enviar os dados;
- a compressão dos dados dos sensores, comparando algoritmos clássicos com uma IA leve;
- a medição real da energia gasta.

## O que tem aqui

| Pasta ou arquivo | O que é |
|---|---|
| `teste_compressao/` | Primeiro teste de compressão sem perda, com dados reais do INMET |
| `teste_compressao.md` | Resultados do teste |
| `arquitetura.md` | Rascunho da arquitetura do protótipo |
| `artigos_relacionados.md` | Artigos sobre aprendizado federado com LoRa |
| `artigos_compressao_dados.md` | Artigos sobre compressão de dados de sensores |
| `aplicacoes.md` | Ideias de aplicação |
| `explicacao_algoritmos.md` | Como funciona cada jeito de comprimir |
| `explicacao_diferenca_huffman.md` | Como funciona a diferença + Huffman no código |
| `como_analisar_artigo.md` | Roteiro para analisar artigos |

## Como rodar o teste de compressão

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

## Dados

Dados históricos do INMET (Instituto Nacional de Meteorologia), estação automática A531, Maria da Fé (MG), 2025.
