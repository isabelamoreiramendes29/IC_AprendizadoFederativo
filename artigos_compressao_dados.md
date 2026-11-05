# Artigos sobre compressão de dados de sensores

**Busca:** Google Acadêmico, 15/10/2026.

**Por que esta busca:** na IC, "compressão de dados" quer dizer comprimir os **dados dos sensores**. O professor pediu para pesquisar e comparar se é melhor comprimir com IA ou com um algoritmo simples, e a energia é prioridade.

**Buscas usadas:**
1. `"data compression" LoRa IoT sensor energy`
2. `federated learning "data compression" IoT sensor autoencoder energy`
3. `lightweight lossless compression sensor data microcontroller energy IoT` (de 2019 em diante)
4. `"compressão de dados" LoRa sensores energia` (em português)

**Status:** ainda não li os artigos inteiros. As descrições abaixo vêm do resumo do Google Acadêmico. A exceção é o **C1**, cujo resumo, introdução e método eu li no site da revista.

**Termos úteis:**
- **Sem perda:** os dados voltam exatamente iguais.
- **Com perda:** os dados voltam parecidos, mas a compressão é maior.

---

## ⭐ Destaque: artigo do seu próprio laboratório

### C1 — Dias, Vilas Boas, **Figueiredo**, Mafra e Ouameur (2026)
*Data Compression in LoRa Networks: Performance and Energy Trade-Offs of Classical and Cutting-Edge Compression Algorithms.* Sensors, v. 26, n. 5, art. 1414.

- **Autores do WAI-Lab / Inatel**, incluindo o **Prof. Felipe** (seu coorientador). Acesso aberto: https://doi.org/10.3390/s26051414
- **O que fizeram:** compararam 7 algoritmos de compressão **sem perda** em LoRa:
  - **clássicos (sem IA):** Huffman e LZW;
  - **modernos ou com IA:** CMIX, PAQ8PX, GMIX, LSTM-compress e BSC.
- **Como mediram:**
  - Raspberry Pi 5 + rádio LoRa RFM95W em **915 MHz** (a frequência do Brasil);
  - **energia medida com sensor INA219**;
  - SF7 e SF12;
  - **teste de campo no Inatel**, com 1,38 km entre transmissor e receptor;
  - 100 repetições por teste.
- **Resultados (do resumo):**
  - O **LZW** (clássico) teve a **melhor eficiência de energia**: até **7,41%** de economia na transmissão LoRa.
  - Os algoritmos **com IA** comprimem **mais**, mas gastam tanto processamento e memória que **o saldo de energia fica negativo**: gastam mais do que economizam.
  - Conclusão dos autores: **LZW no sensor**, e os algoritmos pesados (com IA) só no gateway ou num servidor.
- **O que ainda fica aberto para a sua IC:**
  1. Rodaram num **Raspberry Pi 5** (um computador), **não num microcontrolador**.
  2. Só testaram compressão **sem perda**.
  3. As IAs testadas são **pesadas**. Uma **IA pequena** (TinyML, por exemplo um autoencoder) ainda não foi comparada.
  4. **Não usaram aprendizado federado.**
  5. Os dados eram mensagens de texto e GPS, não séries de temperatura ou umidade.
- **Código aberto:** https://github.com/Rafa-Laureano/Aplicacao-de-Compressao-de-Dados-em-Redes-LoRa
- **Lido inteiro em 15/10/2026.** Resultados principais:
  - **Quanto comprime:**
    - as IAs (CMIX e PAQ8PX) comprimem mais de 80%;
    - o LZW comprime ~60%;
    - num pacote SF7 de 222 bytes cabem até 63 mensagens de GPS com CMIX, contra 25 com LZW.
  - **Tempo para comprimir:**
    - LZW: 0,0018 s;
    - CMIX: 11,75 s, ou seja, milhares de vezes mais lento.
  - **Energia:** quem decide o gasto é o **tempo de processamento**, mais do que o quanto comprime.
    - A melhor economia foi a do **LZW**: até **7,41%** (dados de logística, SF12, 7 s de espera).
    - O **CMIX teve saldo negativo** em todos os casos: chegou a −23,25%.
  - **Huffman:** com mensagens curtas, a tabela de símbolos (de 28 a 128 bytes) pode **aumentar** o tamanho em vez de diminuir.
  - **Teste de campo** (1,38 km): menos de 4% de perda de pacotes, sem corromper os dados.
- **Limitações que os próprios autores citam:**
  - não consideraram retransmissões, ADR nem duty cycle;
  - não mediram o tempo para descomprimir nem o tamanho do código no microcontrolador;
  - os testes foram num Raspberry Pi 5.
- **Trabalhos futuros que eles propõem (combinam com a IC!):**
  - validar em **microcontroladores (ESP32 e STM32)**;
  - deixar as IAs de compressão leves para dispositivos de baixo consumo;
  - criar esquemas **híbridos** (algoritmo clássico + IA);
  - usar **aprendizado no próprio dispositivo**;
  - recomprimir no gateway.

---

## C2 — lido inteiro em 02/11/2026
PDF: `artigos/C2_OliveiraJunior2023_CompressaoLoRa_ESP32.pdf`
- **Placa:** ESP32 (TTGO LoRa, rádio SX1276), LoRa no Brasil (AU915), SF7 e SF12.
- **Dados:** temperatura de blocos de concreto (mensagens de 28 bytes) e GPS (22 bytes), em texto.
- **Algoritmos (todos sem perda e sem IA):** Huffman, Aritmético, LZ77, LZ78 e LZW, adaptados para caber no microcontrolador (dicionário de 256 posições).
- **Quanto comprime:**
  - LZW: 70% (temperatura) e 63% (GPS);
  - Huffman: 61%;
  - Aritmético: 55%.
- **Mensagens por pacote:** em SF7, até 21 mensagens num pacote, contra 1 sem compressão.
- **Energia (INA219):**
  - em SF12, com a placa dormindo entre envios, economia de ~20–22%;
  - em **SF7**, só **~1–2%** (enviar já é barato, então comprimir quase não compensa).
- **Bateria (modelo de cálculo):** a duração passa de 21 para 26 dias.
- **Custo:** é preciso esperar juntar 21 leituras para enviar (315 s com uma leitura a cada 15 s). O LZW usa 3 a 4× mais memória que o Huffman.
- **Repetições:** 100 compressões por grupo de mensagens.
- **Não tem:** IA nem aprendizado federado; teste de campo com distância não descrito.

## C13 a C16 — lidos em 03/11/2026 (PDFs conseguidos pela biblioteca do Inatel)

**C13 — Hanumanthaiah et al. 2019** (`artigos/C13_Hanumanthaiah2019_DeltaRLE_SemPerda.pdf`)
- Comprime dados de um acelerômetro (sistema de alerta de deslizamento na Índia) com **diferença** e com **diferença + RLE** (troca valores repetidos por "valor + quantas vezes"), sem perda, num microcontrolador PSoC 5LP.
- A melhor redução foi de ~52% (diferença + RLE, conversor de 8 bits).
- **Cuidados:**
  - artigo curto (5 páginas), um teste só, sem rádio e sem medir energia;
  - alguns números da Tabela I não batem com a conta. Por exemplo, 860 de 1515 bytes dá 56,8%, não 53,86%.

**C14 — Idrees et al. 2025, SZ4IoT** (`artigos/C14_Idrees2025_SZ4IoT_ComPerda_ESP32.pdf`)
- Compressão **com perda controlada**: um "palpite sem IA" (a partir dos valores anteriores) e só o erro é guardado, desde que fique dentro de um limite escolhido.
- Rodou em microcontroladores: ESP32, Teensy 4.0 e RP2040. Comprimiu em menos de 0,1 s e comprimiu 2 a 3 vezes mais que outros métodos leves.
- **Energia:** medida com um medidor USB, enviando por Wi-Fi (ESP-NOW), **não por LoRa**, e sem a placa dormir. Comprimir antes de enviar gastou 58–65% menos do que enviar sem comprimir.
- **Interessa à IC:** é a mesma ideia da "IA que adivinha", só que com um palpite sem IA.

**C15 — Bisio et al. 2026** (`artigos/C15_Bisio2026_EnergiaQualidade_LoRa_Simulacao.pdf`)
- Usa *compressive sensing* (envia só parte das medidas e reconstrói o sinal no receptor, com perda) em LoRa e procura o melhor equilíbrio entre qualidade e energia.
- Conclusão: **comprimir nem sempre é o que mais pesa**. A escolha do SF e da taxa de código pesa tanto quanto.
- **Cuidado:** é **tudo simulado**. A energia vem de uma fórmula e não foi medida, e não há placa.

**C16 — Kumari et al. 2022** (IEEE Transactions on Sustainable Computing, vol. 7) (`artigos/C16_Kumari2022_SmartMetering_LSTM_LoRa.pdf`)
- Uma **IA (LSTM, com perda)** comprime o consumo de energia de eletrodomésticos num Raspberry Pi 3 e envia por LoRa (simulação no NS-3 + protótipo numa universidade da Índia).
- A IA acertou ~92% na reconstrução.
- **Dado importante:** na simulação, **comprimir gastou mais energia (48 J) do que enviar (33 J)**. Bate com o WAI-Lab: IA pesada pode gastar mais do que economiza.
- **Cuidado:** a energia foi estimada, não medida com sensor de corrente.

## ★★★ Muito parecidos (compressão de dados + LoRa + energia)

| # | Artigo | Ano / Veículo | Do que trata (pelo resumo) | PDF |
|---|---|---|---|---|
| C2 | de Oliveira Júnior, de Camargo et al. — *Data compression in LoRa networks: a compromise between performance and energy consumption* | 2023, Journal of Internet Services and Applications (SBC) | Autores brasileiros. Compara algoritmos clássicos (Huffman, LZ, LZW) em ESP32 com LoRa e mede energia. O C1 cita: LZW comprimiu 69% (temperatura) e economizou ~22% de energia. | Aberto (sbc.org.br) |
| C3 | Väänänen e Hämäläinen — *LoRa-based sensor node energy consumption with data compression* | 2021, IEEE MetroInd4.0&IoT | Algoritmos simples de compressão num nó LoRa, com energia **medida** com e sem compressão. | Aberto (theseus.fi) |
| C4 | Väänänen e Hämäläinen — *Efficiency of temporal sensor data compression methods to reduce LoRa-based sensor node energy consumption* | 2022, Sensor Review | Métodos para comprimir **séries de dados de sensores** e reduzir a energia do nó LoRa. | Aberto (emerald) |
| C5 | Wielandt et al. — *TDD LoRa and delta encoding in low-power networks of environmental sensor arrays* | 2023, Journal of Signal Processing Systems | **Codificação por diferença** (delta) em sensores ambientais com LoRa, e o efeito na energia. | Aberto (Springer) |
| C6 | de Oliveira Júnior e Oyamada — *Avaliando o impacto da compressão de dados no desempenho e energia em redes LoRa* | 2020, SBESC (em português) | Versão inicial do C2: S-LZW e variações em LoRa. | Aberto (sbc.org.br) |
| C7 | Oliveira Júnior — *Compressão de dados em redes LoRa: um compromisso entre desempenho e consumo de energia* | 2021, dissertação Unioeste (em português) | Dissertação que deu origem ao C2 e ao C6. Deve ser didática. | Aberto (tede.unioeste.br) |

## ★★ Parecidos (compressão de dados de sensores e energia, sem LoRa ou com IA)

| # | Artigo | Ano / Veículo | Do que trata (pelo resumo) | PDF |
|---|---|---|---|---|
| C8 | Azar et al. — *Efficient lossy compression for IoT using SZ and reconstruction with 1D U-Net* | 2022, Mobile Networks and Applications | Compressão **com perda** (SZ) no sensor e uma **IA reconstrói** os dados depois. Compara a energia com Wi-Fi e com LoRa. | Aberto (hal.science) |
| C9 | Azar et al. — *An energy efficient IoT data compression approach for edge machine learning* | 2019, Future Generation Computer Systems | Compressão leve de dados de sensores para economizar energia. **Muito citado (327 citações).** | Aberto (hal.science) |
| C10 | Piątkowski et al. — *Study of the impact of data compression on the energy consumption required for data transmission in a microcontroller-based system* | 2023, Sensors | Mede quanto a compressão economiza de energia num **microcontrolador**. | Aberto (MDPI) |
| C11 | Mishra et al. — *Investigation of energy cost of data compression algorithms in WSN for IoT applications* | 2022, Sensors | O **custo de energia** dos algoritmos de compressão num microcontrolador (MSP430). | Aberto (MDPI) |
| C12 | Al-Qurabat — *A lightweight Huffman-based differential encoding lossless compression technique in IoT for smart agriculture* | 2021 | Compressão leve (diferença + Huffman) para **agricultura inteligente**. | Aberto |
| C13 | Hanumanthaiah et al. — *Comparison of lossless data compression techniques in low-cost low-power IoT systems* | 2019, conferência IEEE | Compara técnicas sem perda em sistemas IoT baratos e de baixo consumo. | **Baixado e lido em 03/11/2026** |
| C14 | Idrees et al. — *SZ4IoT: an adaptive lightweight lossy compression algorithm for diverse IoT devices and data types* | 2025, Journal of Supercomputing | Compressão **com perda**, leve e adaptável a vários dispositivos. | **Baixado e lido em 03/11/2026** |
| C15 | Bisio et al. — *Learning the Energy-Accuracy Frontier: Data-Driven Optimization in LoRa IoT Networks* | 2026, IEEE Internet of Things Journal | *Compressive sensing* em LoRa: equilíbrio entre qualidade da reconstrução e energia. | **Baixado e lido em 03/11/2026** |
| C16 | Kumari et al. — *An energy efficient smart metering system using edge computing in LoRa network* | 2022, IEEE Transactions on Sustainable Computing | Medidores inteligentes com compressão de dados em LoRa e foco em energia. | **Baixado e lido em 03/11/2026** |
| C17 | Misahlidou et al. — *Optimizing Data Transmission in LoRa-Based IoT Systems: A Performance Evaluation of Compression Algorithms* | 2025, capítulo Springer | Avalia algoritmos de compressão em LoRa e o efeito na energia. | Fechado |

## ★ Compressão de dados com IA e aprendizado federado

| # | Artigo | Ano / Veículo | Do que trata (pelo resumo) | PDF |
|---|---|---|---|---|
| C18 | Kovtun — *Adaptive information-constrained mapping for feature compression in edge AI and federated systems* | 2025, Scientific Reports | **Autoencoder** treinado com **aprendizado federado** para comprimir dados. | Aberto (nature.com) |
| C19 | Abdalla — *Federated Learning for Cyber-Physical Systems in Smart Environmental Monitoring* | 2024, tese (Khalifa University) | Aprendizado federado em **monitoramento ambiental**, com autoencoders e economia de energia nos sensores. | Aberto |
| C20 | Amaizu — *Edge-enhanced learning and analytics in distributed IoT systems* | 2023, tese (Univ. Leicester) | Compressão de dados aprendida na borda da rede, comparada com aprendizado federado. | Aberto |
| C21 | Sravani et al. — *Data Reduction and Compression Techniques for Energy Optimization in IoT: From PCA to Deep Autoencoders* | 2026, conferência IEEE | Compara técnicas, de PCA até autoencoders, pensando em energia. | Fechado |
| C22 | Nguyen et al. — *HCFL: A high compression approach for communication-efficient federated learning in very large scale IoT networks* | 2022, IEEE Transactions | **Atenção:** comprime o **modelo** com autoencoder, não os dados do sensor. | Aberto (arXiv) |

---

## O que esta busca já mostra
1. **Existe um trabalho do próprio WAI-Lab (C1)** que compara compressão com IA × algoritmo em LoRa, medindo energia. A IC provavelmente deve partir dele.
2. Nos testes do C1 (e no C2), **o algoritmo clássico LZW gastou menos energia** que as IAs pesadas. Mas ainda **ninguém comparou com uma IA pequena rodando num microcontrolador**.
3. **Medir energia com INA219** é o padrão do laboratório (C1). É bom usar o mesmo método.
4. Quase ninguém junta **compressão de dados + aprendizado federado + LoRa**. O C18 e o C19 chegam perto, mas sem LoRa.

## Próximos passos sugeridos
1. **Ler o C1 inteiro primeiro** e conversar com o Prof. Felipe sobre ele.
2. Depois ler o **C2 e o C7** (brasileiros) e o **C3 e o C4** (energia medida em LoRa).
3. Para a parte "com IA": ler o **C8** e o **C18**.
