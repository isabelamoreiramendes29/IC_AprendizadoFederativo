# Arquitetura da IC

Rascunho de 02/11/2026, atualizado em 04/11/2026, para mostrar aos professores na reunião de quinta (05/11/2026).

**Vamos levar dois planos: o Plano 1 (uma placa por nó) e o Plano 2 (duas placas por nó). O professor escolhe.**

---

## 1. As peças do sistema

```
[ Nó sensor ]  --LoRa-->  [ Receptor ]  --cabo/internet-->  [ Computador ou servidor ]
 placa + rádio LoRa        recebe os pacotes                  faz a média dos modelos,
 + bateria                 e devolve o modelo                 guarda e mostra os dados
```

- **Nó sensor** (começamos com 1 e depois passamos para 3; ver a seção 10): mede, comprime, treina e envia. Funciona a bateria, então é onde a energia mais importa.
- **Receptor** (1): recebe os pacotes de todos os nós e manda de volta o modelo com a média. Fica na tomada.
- **Computador ou Raspberry Pi**: ligado ao receptor por cabo. Faz a média dos modelos e guarda os dados.

## 2. Quando cada coisa acontece

O nó faz três tarefas, cada uma no seu ritmo:

| De quanto em quanto tempo | O que o nó faz | Gasto |
|---|---|---|
| A cada 1 hora | Mede a temperatura e a umidade, guarda e volta a dormir | Quase nada |
| A cada bloco (por exemplo, 1 dia) | Comprime as leituras do bloco e envia | Pouco: alguns pacotes |
| De vez em quando (por exemplo, 1 vez por dia ou por semana) | Rodada do aprendizado federado: treina um pouco, envia o modelo e recebe a média | O mais caro |

- A rodada fica para de vez em quando porque é a parte que mais gasta. No Giménez, uma rodada levou cerca de 24 minutos, quase todos com o rádio ligado.
- Entre uma tarefa e outra, o nó dorme.
- De quanto em quanto tempo fazer a rodada se decide nos testes: rodadas raras gastam menos, mas a IA aprende mais devagar.
- A IC quer medir a energia de **cada tarefa**. Nenhum artigo lido fez isso.

## 3. O que viaja pelo rádio

- **Os dados dos sensores, comprimidos:** vão do nó para o receptor.
- **O modelo do aprendizado federado:** viaja em **duas direções**. O nó manda o seu modelo, o receptor faz a média e manda o modelo com a média de volta para todos os nós.

Por isso o nó também **recebe** bastante, e um rádio que gasta pouco para receber economiza energia.

### Quem fala quando
Com 3 nós e 1 receptor, se dois nós enviarem ao mesmo tempo, os pacotes se chocam e se perdem. Por isso **cada nó tem o seu horário** para enviar:
- por exemplo, o nó 1 no minuto 0, o nó 2 no minuto 5 e o nó 3 no minuto 10. A folga de 5 minutos é porque o relógio da placa não é perfeito;
- na rodada do aprendizado federado é igual: cada nó envia o modelo no seu horário, e depois todos acordam num horário combinado para receber a média;
- o receptor manda a hora certa junto com a média, e o nó acerta o relógio.

Outra opção seria o receptor chamar um nó de cada vez. Mas aí o nó teria que ficar escutando, esperando ser chamado, e escutar gasta bateria.

---

## 4. Os dois planos

### Plano 1: uma placa por nó

Uma placa só faz tudo. Ela tem **dois núcleos** (dois "cérebros" no mesmo chip): um cuida do rádio e o outro treina a IA.

- **Placa:** TTGO LoRa32 **ou** Heltec WiFi LoRa 32 V3 (comparação na seção 5).
- **A favor:** gasta menos energia, é mais barato e mais simples.
- **Contra:** o rádio e o treino dividem a mesma memória e o mesmo processador. É preciso organizar bem as tarefas para não perder um pacote LoRa enquanto a placa treina. Quase não há artigos testando aprendizado federado com uma placa só.

### Plano 2: duas placas por nó (como o Giménez)

Uma placa treina a IA e a outra cuida do rádio. As duas se ligam por um fio (comunicação serial).

- **Placa de treino:** Arduino Portenta H7, a mesma do Giménez.
- **Placa de rádio:** TTGO LoRa32 **ou** Heltec WiFi LoRa 32 V3.
- **A favor:** cada placa faz só uma tarefa. Já existe artigo defendendo esse desenho (#20, Giménez 2025) e o código dele é aberto.
- **Contra:** gasta mais energia (no Giménez, o rádio gastava de 52 a 141 mA e o Portenta de 128 a 165 mA, ou seja, o nó podia chegar a cerca de 300 mA). O Portenta é mais caro e o sistema fica mais complicado.

### O que o artigo #20 (Giménez 2025) diz sobre isso

- Os próprios autores dizem que duas placas gastam mais e que, **se a energia for crítica, uma placa só pode ser melhor**. Na IC, a energia é prioridade.
- A **acurácia** e a **velocidade do treino** seriam as **mesmas** nos dois desenhos.
- A vantagem das duas placas é não perder pacotes LoRa nem leituras do sensor enquanto a placa treina.
- Uma rodada de aprendizado federado levou cerca de **24 minutos**, quase tudo por causa do rádio. Passar o modelo de uma placa para a outra pelo fio levou só cerca de 0,4 segundo.
- O artigo **não mediu a energia** dos dois desenhos.

**Ideia:** como a placa de rádio pode ser a mesma nos dois planos, a IC pode testar os dois e medir **quanto custa, em energia, a segunda placa**. Ninguém mediu isso ainda.

### O que é igual nos dois planos

| Peça | Escolha | Por quê |
|---|---|---|
| Receptor | Uma placa de rádio igual à dos nós, ligada por cabo a um computador ou Raspberry Pi | Mesmo rádio dos dois lados, e é barato |
| Rede | LoRa ponto a ponto: as placas falam direto pelo rádio, sem a rede LoRaWAN | A LoRaWAN foi feita para o sensor mandar dados; mandar o modelo de volta para o nó é limitado nela (o Giménez diz isso no #3 e no #20) |
| Frequência | 915 MHz | É a faixa usada no Brasil, a mesma do WAI-Lab |
| Medidor de energia | INA219, entre a bateria e a placa | O WAI-Lab e o Oliveira Júnior usaram o mesmo, então os números ficam comparáveis |
| Quem lê o medidor | Outra placa ou o computador | Para a medição não entrar na conta de energia do nó |
| Bateria | Bateria de lítio de 3,7 V, como a de celular | As placas de rádio já têm conector e carregador |
| Antena | A de 915 MHz que vem com a placa | **Nunca ligar o envio do rádio sem a antena**, porque pode queimar o rádio |
| Dados na primeira fase | Dados reais do INMET, gravados na memória de cada placa, uma estação por nó | O nó fica só na bateria, e a medição de energia fica certa. A IA e o algoritmo comprimem exatamente os mesmos dados |
| Sensor | Fica para depois, quando a aplicação for escolhida | Ver a seção 7 |

**Limite do INA219:** ele quase não enxerga correntes muito pequenas, como a da placa "dormindo" (menos de 0,1 mA). Um medidor mais preciso ajudaria.

---

## 5. Placa de rádio: TTGO ou Heltec?

As duas servem para os dois planos.

| | **TTGO LoRa32** | **Heltec WiFi LoRa 32 V3** |
|---|---|---|
| Processador | ESP32 (2 núcleos) | ESP32-S3 (2 núcleos, mais novo, com instruções que aceleram as contas de IA) |
| Chip de rádio | SX1276, o mesmo do Giménez, do Oliveira Júnior e do WAI-Lab | SX1262, mais novo: segundo o fabricante do chip, gasta cerca de **metade** da corrente para **receber** |
| Já foi usada em artigos? | Sim: #2, #3, #20 (Giménez) e C2 (Oliveira Júnior) | Quase não: só uma dissertação de 2025 (bloqueada até 2028) e um texto ainda não revisado |
| A favor | Fácil comparar com os artigos; o código aberto do Giménez já roda nela | Gasta menos para receber, o que importa no aprendizado federado |
| Contra | Rádio mais antigo, gasta mais para receber | Poucos resultados publicados para comparar |
| Na loja | Versão de 915 MHz | Versão "863–928 MHz" |

**Cuidado:** um artigo de 2021 (Ould e Bennett, revista Sensors) mediu 4 placas LoRa e viu que placas vendidas como "de baixo consumo" gastam quantidades bem diferentes. Seja qual for a placa, **vamos medir o gasto dela nós mesmos**.

---

## 6. Quantas placas

- **Plano 1:** 3 nós + 1 receptor = **4 placas de rádio** (melhor 5, com uma de reserva).
- **Plano 2:** as mesmas 4 ou 5 placas de rádio + **3 Arduino Portenta H7** (o receptor não precisa de Portenta).
- Para medir a energia: pelo menos 1 INA219 (o ideal é 1 por nó).
- Se o professor quiser comparar TTGO e Heltec, é preciso comprar as duas.
- O laboratório compra o que não tiver.

---

## 7. E o sensor?

Na primeira fase **não precisa de sensor**. Os dados do INMET ficam **gravados na memória de cada placa**, junto com o programa. A placa lê uma hora de cada vez, como se fosse o sensor. (Decidido em 04/11/2026.)
- Cada nó usa uma estação diferente, como se fossem três fazendas: **Maria da Fé, Machado e Varginha**.
- Um ano de temperatura e umidade ocupa uns 26 kB. A placa tem 4 MB (TTGO) ou 8 MB (Heltec), então cabe com folga.
- Assim o nó fica só na bateria. Com o cabo USB ligado, a placa receberia energia do computador, e o medidor na bateria não veria o gasto de verdade.
- Para não esperar um ano inteiro, no laboratório dá para acelerar o tempo, com uma "hora" a cada poucos segundos. O gasto de cada tarefa (comprimir, enviar) não muda com isso. O gasto da placa dormindo se mede à parte.

- A placa tem pinos para ligar sensores, então qualquer sensor entra depois.
- O sensor depende da aplicação:
  - geada no café: temperatura e umidade (por exemplo, o SHT31);
  - enchente: nível da água e chuva;
  - deslizamento: umidade do solo.
- O INMET tem vários tipos de dado (temperatura, umidade, chuva, pressão e vento). Dá para testar a compressão em mais de um tipo sem escolher a aplicação agora.
- Isso importa porque a compressão muda com o tipo de dado: no C2, o LZW comprimiu 70% da temperatura e 63% do GPS.

---

## 8. O que o aprendizado federado vai treinar? (decisão em aberto)

- **Opção A, duas coisas separadas:** o nó envia os dados comprimidos, e o aprendizado federado treina **outra IA**, por exemplo uma que prevê geada.
- **Opção B, o aprendizado federado treina o compressor:** a IA que comprime os dados é o próprio modelo do aprendizado federado. O mesmo dado também é comprimido pelo algoritmo (LZW), para comparar. É a opção que melhor junta as duas partes da IC.

Isso está ligado à pergunta principal para os professores: em que momento os dados dos sensores são comprimidos e por quê?

### O modelo cabe na placa? (conta aproximada, Opção B)

- A IA recebe 24 horas de temperatura e umidade (48 números) e resume tudo em 8.
- Ela teria cerca de 2 mil pesos. Com 1 byte por peso, como no Giménez, o modelo fica com uns **2 kB**.
- As placas de rádio têm cerca de 500 kB de memória de trabalho, então cabe com folga, mesmo com o espaço extra que o treino usa.
- Pelo rádio, seriam uns **10 pacotes em SF7** ou uns **40 em SF12**. O modelo de 70 neurônios do Giménez precisava de 432.
- O tempo real de cada troca só vamos saber medindo.

---

## 9. Algoritmo e IA: como vamos comparar

**Vamos usar os dois.** O professor decidiu "vamos fazer das duas formas". A IC comprime os mesmos dados com algoritmo e com IA e compara qual é melhor.

### Um protótipo só, três rodadas

O protótipo é o mesmo (3 nós + o receptor). Só muda o programa gravado nas placas:
1. **Rodada 1:** comprime com o **algoritmo**.
2. **Rodada 2:** comprime com a **IA**.
3. **Rodada 3:** envia **sem comprimir**, para saber quanto cada um economizou.

A placa, o rádio e os dados são os mesmos. Assim, a diferença no resultado só pode vir do jeito de comprimir.

### Os algoritmos (sem IA)

- **LZW:** foi o melhor no WAI-Lab e no C2. Fica para dar para comparar com eles.
- **Diferença + Huffman:** foi o melhor no teste de 02/11/2026 (`teste_compressao.md`). Reduziu 81% em relação ao texto, contra 31% do LZW.

### O que a IA precisa ter (Plano 1)

1. **Caber na placa e treinar nela**, porque o aprendizado federado treina no nó (cerca de 500 kB de memória).
2. **Ser pequena**, porque o modelo viaja pelo rádio.
3. **Ser rápida.** No WAI-Lab, quem decidiu a energia foi o tempo de processamento: o CMIX levou 11,75 s e gastou mais do que economizou.

Por isso as IAs do WAI-Lab (CMIX, PAQ8PX) não servem: são pesadas demais para um microcontrolador.

### As duas candidatas de IA (o professor escolhe)

**IA 1, a "IA que resume" (autoencoder), com perda**
- Pega as 24 leituras do dia e resume em 8 números. O receptor "infla" de volta, quase igual.
- A favor: comprime bastante; é muito usada em trabalhos de aprendizado federado com sensores (por exemplo, o C19).
- Contra: é com perda, então a comparação com o LZW não é direta.

**IA 2, a "IA que adivinha" (previsor), sem perda** (a preferida)
- Tenta adivinhar a próxima leitura, e o nó envia só o erro do palpite.
  - Exemplo: às 8h fez 18,0 °C, a IA prevê 19,9 °C para as 9h, e às 9h fez 20,1 °C. O nó envia só +0,2.
  - O receptor tem a mesma IA, faz o mesmo palpite e soma o erro. O dado volta exatamente igual.
- A favor:
  - é sem perda, então a comparação com o LZW é justa;
  - é a versão leve do que o CMIX e o PAQ8PX fazem;
  - combina com os trabalhos futuros do WAI-Lab: IA leve, mistura de IA com algoritmo e aprender na própria placa.
- Contra: comprime menos que a IA que resume.

As duas podem ser treinadas pelo aprendizado federado (Opção B). O receptor precisa usar **exatamente o mesmo modelo** que o nó usou para comprimir, senão o dado não volta igual. É como dois amigos usando o mesmo dicionário: se um troca de dicionário sem avisar, o outro não entende mais nada. Por isso:
- o nó comprime com o **modelo da média**, que o receptor também tem, e não com o modelo que ele ainda está treinando;
- cada pacote leva o **número da versão** do modelo usado (1 byte basta), caso algum nó não tenha recebido a média nova;
- antes de existir o primeiro modelo, o nó usa a diferença (o palpite sem IA).

### A meta da IA

- A **diferença** é um "palpite sem IA": ela chuta que a próxima leitura vai ser igual à anterior.
- A IA que adivinha precisa chutar melhor que isso.
- No teste com Maria da Fé, a meta é ficar **abaixo de 35 bytes por dia** (o resultado da diferença + Huffman), gastando pouca energia.

### E o resultado final?

- **O resultado da IC é a comparação:** qual é melhor e em que situação. Se o algoritmo ganhar, também é um bom resultado.
- **Numa aplicação de verdade, usa-se o que ganhou.**
- **O vencedor pode mudar com a situação.** No C2, comprimir economizou 1 a 2% de energia em SF7 (perto) e cerca de 22% em SF12 (longe).
- **Pode ser uma mistura:** a IA faz o palpite e o Huffman comprime o erro.
- **Quem decide é a energia.** Se a IA comprimir mais, mas gastar mais energia do que economiza, ela não é a melhor para a IC.

## 10. Por onde começar

1. **Fase 1: 1 nó e o receptor.** Só a compressão, ainda sem aprendizado federado.
   - O nó faz as três rodadas (algoritmo, IA e sem comprimir) com os dados de Maria da Fé, e o INA219 mede a energia de cada tarefa.
   - É o teste de compressão de 02/11 (`teste_compressao.md`) levado para a placa.
   - Nesta fase, a IA aprende só com os dados desse nó.
2. **Fase 2: 3 nós e o receptor.** Entra o aprendizado federado, com uma estação do INMET em cada nó.
3. **Fase 3: o sensor de verdade,** quando a aplicação for escolhida.

Começar pequeno ajuda a achar os problemas de montagem e de medição antes de ter três placas funcionando ao mesmo tempo.

## 11. Para decidir com os professores

As perguntas estão em `perguntas_professor.md`:
1. Plano 1 ou Plano 2?
2. TTGO, Heltec ou as duas?
3. Podemos usar um medidor mais preciso que o INA219?
4. Qual será a aplicação?
5. Opção A ou Opção B?
6. Qual IA: a que resume ou a que adivinha?

## Referências usadas aqui

- #2 Giménez, Solé e Freitag 2023, *Embedded federated learning over a LoRa mesh network*.
- #3 Giménez et al. 2024, *Demo: Edge federated learning over a LoRa mesh network*.
- #20 Giménez, Freitag, Navarro e Selimi 2025, *A two-board design for interconnected intelligence in tiny IoT* (`artigos/20_Gimenez2025_DuasPlacas_TinyIoT.pdf`).
- C1 Dias et al. 2026 (WAI-Lab) e C2 de Oliveira Júnior et al. 2023.
- Ould e Bennett 2021, *Energy Performance Analysis and Modelling of LoRa Prototyping Boards*, Sensors 21(23):7992. https://pmc.ncbi.nlm.nih.gov/articles/PMC8659754/
- Dissertação com a Heltec V3: *LoRa protocol for decentralized federated learning on resource-constrained devices*, Nazarbayev University, 2025. https://nur.nu.edu.kz/handle/123456789/8511
