# Como funciona cada jeito de comprimir e como vamos medir

Programa: `teste_compressao/teste_compressao.py`. No VS Code, aperte **Ctrl + G** e digite o número da linha para ir direto.
Os tamanhos são a média de um dia, de fevereiro a dezembro de 2025, com os dados do INMET de Maria da Fé.

---

## Parte 1: como funciona cada um

### 1. Texto, sem compressão: 189 bytes por dia
- Cada hora vira um texto, como `4.8;92`, mais a quebra de linha. Cada letra ou número ocupa 1 byte, então cada hora ocupa de 7 a 9 bytes.
- É o jeito como o WAI-Lab e o Oliveira Júnior mandavam as mensagens. É o ponto de partida.
- No código: função `texto`, linha 44.

### 2. LZW: 130 bytes (31% a menos)
- Vai lendo o texto e montando um **dicionário** com os pedaços que já apareceram. O dicionário começa com os 256 caracteres, e cada pedaço novo ganha um número.
- Quando um pedaço que já está no dicionário aparece de novo, como `;9` ou `99`, o programa manda só o número desse pedaço, em vez das letras.
- O receptor monta o mesmo dicionário enquanto lê, então o dicionário não viaja no pacote.
- **Por que ganhou pouco:** um dia tem só 189 bytes, e o dicionário ainda está "aprendendo" quando o dia acaba. Com textos longos e repetidos, como no WAI-Lab, ele vai melhor.
- No código: `lzw_comprime`, linha 78, e `lzw_descomprime`, linha 97.

### 3. Huffman sobre o texto: 112 bytes (40% a menos)
- Conta quantas vezes cada caractere aparece no dia. O ponto, o `;` e a quebra de linha aparecem em toda hora.
- Os caracteres mais comuns ganham códigos curtos, de poucos bits, e os raros ganham códigos longos, como no código Morse.
- A tabela de códigos é feita para cada dia, então ela vai junto no pacote, como no WAI-Lab. Num pacote pequeno, a tabela pesa.
- No código: `huffman_texto_comprime`, linha 156.

### 4. Binário: 72 bytes (62% a menos)
- Em vez de escrever `4.8;92` como texto, que ocupa 7 bytes, guarda os números direto: 48 (a temperatura em décimos de grau) em 2 bytes e 92 em 1 byte. São 3 bytes por hora.
- Não é compressão, é só não desperdiçar espaço. Mesmo assim, ganha do LZW e do Huffman.
- No código: `binario`, linha 175.

### 5. Diferença: 49 bytes (74% a menos)
- Manda a primeira hora inteira, em 3 bytes. Nas outras 23, manda só quanto mudou desde a hora anterior: 1 byte para a temperatura e 1 para a umidade. Dá 3 + 23 × 2 = 49 bytes.
- Exemplo: de 4,8 para 3,5 graus, manda -13, que quer dizer que caiu 1,3 grau.
- Se a mudança for grande demais para 1 byte, manda um aviso (o "ESC") e depois o valor inteiro.
- No código: `diferenca_comprime`, linha 189.

### 6. Diferença + Huffman: 35 bytes (81% a menos), o melhor
- Junta as duas técnicas. A diferença transforma as leituras em números pequenos, e o Huffman escreve os mais comuns com poucos bits. Por exemplo, a umidade que não mudou vira 2 bits, e um salto raro vira 10.
- A tabela é feita uma vez, com os dados de janeiro, e fica guardada no nó e no receptor.
- No código: `dif_huffman_comprime`, linha 233. A explicação completa está em `explicacao_diferenca_huffman.md`.

**Todos são sem perda.** O programa descomprime cada dia e confere se voltou exatamente igual. São as linhas com `assert`, dentro da função `roda`, que começa na linha 274.

---

## Parte 2: como medimos

### No computador (o que já foi feito)
- Medimos só o **tamanho**: quantos bytes cada jeito ocupa por dia.
- O número de pacotes é uma conta: o tamanho dividido por 51 bytes em SF12, ou por 222 bytes em SF7. Não teve rádio.
- Conferimos que todos são sem perda.
- **Não medimos energia nem tempo.**

### Na placa (o próximo passo)
- **O medidor:** o INA219 fica no caminho entre a bateria e a placa, como um relógio de luz. Ele mede a tensão (em volts) e a corrente (em ampères) muitas vezes por segundo.
- **A conta da energia:** energia = tensão × corrente × tempo. Por exemplo, se a placa gasta 0,1 A em 3,7 V durante 2 segundos, ela gastou 3,7 × 0,1 × 2 = 0,74 joule.
- **O que medir para cada jeito de comprimir**, um dia de dados por vez:
  1. o tempo e a energia para **comprimir**, com o processador trabalhando;
  2. o tempo e a energia para **enviar**, com o rádio ligado;
  3. a soma dos dois, que é o gasto do dia.
- **Comparar com o teste sem compressão:** economia = gasto sem compressão − gasto com compressão. Se der negativo, comprimir não valeu a pena, como aconteceu com as IAs pesadas no WAI-Lab.
- **Repetir várias vezes e usar a média**, porque cada medida varia um pouco. O WAI-Lab repetiu 100 vezes.
- **Medir em SF7 e em SF12**, porque o resultado muda muito: no Oliveira Júnior, a economia foi de 1 a 2% em SF7 e de cerca de 22% em SF12.
- **Cuidado:** o INA219 quase não vê a corrente da placa dormindo. Por isso a pergunta aos professores sobre um medidor mais preciso.
