# Como funciona a diferença + Huffman no programa

Programa: `teste_compressao/teste_compressao.py`. No VS Code, aperte **Ctrl + G** e digite o número da linha para ir direto.

---

## Por que o exemplo mostra 6 leituras e depois 23 diferenças
- O dia tem 24 leituras, e o programa usa todas.
- Nos pontos 1 e 2, ele só **mostra** as 6 primeiras, para não encher a tela. É o `[:6]` nas linhas 312 e 315, que quer dizer "só as 6 primeiras".
- O ponto 3 mostra as 23 diferenças das 24 leituras. São 23 porque a primeira hora vai inteira: numa cerca com 24 postes, há 23 espaços entre eles.

## Por que precisa da diferença
A diferença já é o primeiro passo da compressão: troca números grandes por números pequenos.
- **Binário:** cada hora ocupa 3 bytes (2 para a temperatura e 1 para a umidade). O dia fica com 72 bytes.
- **Diferença:** depois da primeira hora, cada hora ocupa 2 bytes (1 para cada diferença), porque número pequeno cabe em 1 byte. O dia fica com 49 bytes.
- **Diferença + Huffman:** as diferenças mais comuns ganham códigos menores que 1 byte. O dia mais frio ficou com 37 bytes, e a média do ano é 35.

## A ideia do Huffman
É como o código Morse: a letra E, que é a mais comum, vira só um ponto, e as letras raras viram sinais longos. O Huffman faz o mesmo com as diferenças.

## São duas técnicas juntas
1. **A diferença** troca números grandes por pequenos. Leituras de 4,8, 3,5, 2,8 e 2,3 graus viram 48, -13, -7 e -5 (em décimos de grau). O receptor refaz as contas: 48 - 13 = 35, 35 - 7 = 28, 28 - 5 = 23. Mas cada diferença ainda ocupa 8 bits, mesmo quando é 0.
2. **O Huffman** acaba com esse desperdício: as diferenças comuns ganham códigos curtos, e as raras, códigos longos.

| Diferença | Só a diferença | Diferença + Huffman |
|---|---|---|
| Umidade não mudou (0) | 8 bits | 2 bits |
| Umidade subiu 1 | 8 bits | 3 bits |
| Temperatura caiu 0,1 grau (-1) | 8 bits | 4 bits |
| Temperatura subiu 9,2 graus (92), raro | 8 bits | 10 bits |

Uma técnica ajuda a outra: o Huffman funciona melhor quando alguns valores aparecem muito mais que os outros, e é exatamente isso que a diferença cria.

No teste, o "Huffman" sozinho foi usado no texto, e a tabela ia junto em cada pacote. Por isso ele deu só 112 bytes.

---

## Parte A: a tabela de códigos (feita uma vez, com janeiro)
Função `tabela_fixa`, linha 219.
1. Pega os 31 dias de janeiro e conta quantas vezes aparece cada diferença, separando a temperatura da umidade.
2. Antes de contar, dá 1 ponto para todo valor de -127 a 127, para nenhum ficar sem código. Também cria o "ESC", um aviso de que "o próximo número vem inteiro".
3. Com a contagem, o Huffman dá os códigos (`comprimentos_huffman`, linha 119, e `codigos_canonicos`, linha 135). O que aparece mais ganha o código mais curto.

Códigos que saíram de janeiro (1 byte = 8 bits). Na temperatura, a diferença é em décimos de grau: -1 quer dizer que caiu 0,1 grau.

| Diferença | Temperatura | Umidade |
|---|---|---|
| 0 | 5 bits | **2 bits** |
| +1 | 5 bits | 3 bits |
| -1 | 4 bits | 5 bits |
| -13 | 8 bits | — |
| +92 / -48 (saltos raros) | 10 bits | 10 bits |

A tabela fica guardada no nó e no receptor, então não viaja no pacote.

## Parte B: comprimir um dia
Função `dif_huffman_comprime`, linha 233.
1. Escreve a primeira hora inteira: a temperatura em 16 bits e a umidade em 8 bits.
2. Para cada uma das outras 23 horas, calcula a diferença da temperatura e escreve o código dela. Depois faz o mesmo com a umidade.
3. Se a diferença for grande demais (fora de -127 a 127), escreve o ESC e depois o valor inteiro.
4. O `Escritor` (linha 49) junta todos os bits em fila, sem sobrar espaço, e completa o último byte com zeros.

No dia mais frio: 24 bits da primeira hora + 159 bits da temperatura + 113 bits da umidade = 296 bits = **37 bytes**. Sem o Huffman, cada diferença ocupa 8 bits. Com ele, ocupa uns 6 em média.

## Parte C: descomprimir (o que o receptor faz)
Função `dif_huffman_descomprime`, linha 249.
1. Lê os 24 bits da primeira hora.
2. Para cada hora seguinte, lê bit por bit até formar um código da tabela (`decodifica_huffman`, linha 144). Assim descobre a diferença e soma com a hora anterior.
3. Se encontrar o ESC, lê o valor inteiro.
4. No fim, tem as 24 leituras exatamente iguais às originais.
