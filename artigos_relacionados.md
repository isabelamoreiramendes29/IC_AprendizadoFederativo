# Artigos relacionados à IC

**Tema da IC:** Aprendizado Federado com LoRa e Compressão de Dados para Sistemas IoT Embarcados
**Orientador:** Prof. Rausley Adriano Amaral de Souza · **Coorientador:** Prof. Felipe Augusto Pereira de Figueiredo (WAI-Lab / Inatel)
**Fonte:** Google Acadêmico, busca feita em 30/09/2026

Legenda de proximidade com o tema:
- ★★★ muito parecido: FL + LoRa + compressão/embarcado
- ★★ parecido: FL + LoRa, ou FL + compressão em IoT
- ★ contexto: revisões e trabalhos de apoio

> ⚠️ Cuidado com o falso amigo: **LoRA** (Low-Rank Adaptation, técnica de ajuste fino de redes neurais) não tem nada a ver com **LoRa** (Long Range, tecnologia de rádio). Vários resultados de busca misturam os dois.

---

## ★★★ Muito parecidos com a IC

| # | Artigo | Autores | Ano / Veículo | Citações | Por que é relevante |
|---|--------|---------|---------------|----------|---------------------|
| 1 | The effects of weight quantization on online federated learning for the IoT: A case study | N. L. Giménez, J. Lee, F. Freitag et al. | 2024, IEEE Access | 19 | Aprendizado federado em dispositivos TinyML comunicando por LoRa, com quantização dos pesos para reduzir o que é transmitido. É o mais próximo do tema: FL + LoRa + compressão. Tem PDF aberto. |
| 2 | Embedded federated learning over a LoRa mesh network | N. L. Giménez, J. M. Solé, F. Freitag | 2023, Pervasive and Mobile Computing | 35 | FL rodando em microcontroladores ligados por uma rede mesh LoRa, sem servidor central. |
| 3 | Edge federated learning over a LoRa mesh network | N. L. Giménez, F. Freitag, L. Navarro et al. | 2024, IEEE/ACM | 5 | Continuação do anterior, com um protótipo de treino federado sobre LoRa. |
| 4 | CE-FedAvg: A Communication-Efficient Federated Learning Framework for LoRaWAN-Based Edge AI | S. Razaghi, A. Aral | 2026, IEEE ICC | – | FedAvg adaptado para LoRaWAN, usando esparsificação e quantização para respeitar os limites de banda. Tem PDF aberto (univie.ac.at). |
| 5 | XFL-Q: Communication-Efficient Federated Learning with Layer-Wise Quantization for IoT | R. El Mokadem, Y. B. Maissa | 2025, conferência IEEE | – | Quantização camada a camada pensada para os limites de banda e *duty cycle* de LoRaWAN e NB-IoT. |
| 6 | FedLoRa: IoT spectrum sensing through fast and energy-efficient federated learning in LoRa networks | F. Busacca, S. Mangione, G. Neglia et al. | 2024, IEEE | 13 | Esquema de FL projetado para redes LoRa, focado em rapidez e economia de energia. Tem PDF aberto (nsf.gov). |
| 7 | FL-LoRaMAC: A novel framework for enabling on-device learning for LoRa-based IoT applications | S. Aggarwal, A. Nasipuri | 2023, Future Internet (MDPI) | 10 | Framework de FL que ajusta a comunicação de subida e de descida no LoRa. É de acesso aberto. |
| 8 | Resource efficient federated LoRaWAN architecture for far-edge IoT applications | A. Triantafyllou, I. Siniosoglou, V. Argyriou et al. | 2025, IEEE | 16 | Arquitetura de FL hierárquico sobre LoRaWAN, focada em eficiência de recursos. |

## ★★ Parecidos

| # | Artigo | Autores | Ano / Veículo | Citações | Observação |
|---|--------|---------|---------------|----------|------------|
| 9 | Optimizing federated learning on TinyML devices for privacy protection and energy efficiency in IoT networks | W. Villegas-Ch et al. | 2024, IEEE Access | 24 | FL em TinyML, com LoRa para a transmissão e quantização do modelo. |
| 10 | UAV-assisted federated learning with hybrid LoRa P2P/LoRaWAN for sustainable biosphere | M. Behjati, H. A. H. Alobaidy, R. Nordin et al. | 2025, Frontiers | 17 | FL com LoRa P2P/LoRaWAN, usando drones para coletar os modelos. Tem PDF aberto. |
| 11 | Federated TinyML on ESP32: A Resource-Constrained Framework for IoT Health Monitoring | C. B. Ram et al. | 2025, conferência IEEE | – | FL em ESP32 com modelos quantizados. |
| 12 | Radio fingerprinting for anomaly detection using federated learning in LoRa-enabled IIoT | S. Halder, T. Newe | 2023, Future Generation Computer Systems | 45 | Aplicação: detecção de intrusão em redes LoRa industriais usando FL. |
| 13 | Privacy-preserving detection of tampered RF transmissions utilizing FL in LoRa networks | N. S. Senol et al. | 2024, Sensors (MDPI) | 15 | Aplicação de segurança em redes LoRa. É de acesso aberto. |
| 14 | DFLNet: Deep federated learning network with privacy preserving for vehicular LoRa nodes fingerprinting | T. Zhang et al. | 2023, IEEE Transactions | 16 | Aplicação veicular. |
| 15 | OptFiD-LoRa: Optimized FL with Differential Privacy for Anomaly Detection in LoRa-IoTs | M. P. Masele et al. | 2026, IEEE IoT | – | FL com privacidade diferencial em redes LoRa. |

## ★ Revisões e material de apoio (bons para começar)

| # | Artigo | Autores | Ano / Veículo | Observação |
|---|--------|---------|---------------|------------|
| 16 | Tiny federated learning for constrained sensors: A systematic literature review | C. N. da Silva, C. V. S. Prazeres | 2025, IEEE Sensors Reviews | Revisão sistemática de TinyFL (FL + TinyML) que cobre poda, quantização e LoRa. Os autores são brasileiros. **Ótimo ponto de partida.** |
| 17 | Federated learning on embedded devices (TCC/dissertação) | N. Llisterri Giménez | 2022, UPC | Trabalho de base dos artigos 1–3, bem didático, com implementação em LoRa. |
| 18 | Neural network compression in the context of federated learning and edge devices (tese) | L. G. Ribeiro | 2024, HAL | Tese sobre compressão de redes neurais em FL. Atenção: aqui "LoRA" é a técnica de adaptação de modelos, não o rádio. |
| 19 | Toward Sustainable Environmental Intelligence: A Survey of FL Applications | S. Yarham, M. Behjati et al. | 2026, IEEE Open Journal | Revisão que discute FL em redes LPWAN/LoRa. |

## Encontrados depois da busca de 30/09

| # | Artigo | Autores | Ano / Veículo | Observação |
|---|--------|---------|---------------|------------|
| 20 | A two-board design for interconnected intelligence in tiny IoT | N. L. Giménez, F. Freitag, L. Navarro, M. Selimi | 2025, conferência Experiment@ (IEEE) | Defende o nó com duas placas (Portenta treina, TTGO cuida do rádio). Achado em 02/11/2026 ao estudar a arquitetura. |

**#20 lido em 02/11/2026:** os autores defendem duas placas para cada uma fazer só uma tarefa. Mas eles mesmos dizem que duas placas gastam mais energia e que, se a energia for crítica, uma placa só pode ser melhor. Uma rodada de aprendizado federado levou cerca de 24 minutos, e a energia dos dois desenhos não foi medida.

---

## PDFs baixados (pasta `artigos/`)

Já baixados: #1, #2 (02/11/2026, cópia aberta em mm.aueb.gr), #3 (02/11/2026, cópia aberta em research.ac.upc.edu), #4, #6, #7, #8, #9, #10, #12 (03/11/2026, pela biblioteca do Inatel), #16, #19, #20 (02/11/2026, UPCommons).

**#12 lido em 03/11/2026:** usa aprendizado federado para descobrir aparelhos LoRa falsos pela "impressão digital" do rádio (um pequeno desvio de frequência de cada aparelho), com 60 aparelhos reais e acerto de ~97%. Mas o aprendizado federado foi simulado no computador, e o artigo não fala de compressão nem de energia. Interessa pouco à IC.

**#3 lido em 02/11/2026:** é uma demonstração de 2 páginas (conferência IEEE/ACM SEC 2024) do mesmo sistema do #2:
- 3 nós, cada um com um Arduino Portenta H7 e um TTGO LoRa32;
- reconhecimento de 4 palavras faladas;
- rodada de aprendizado federado a cada 40 amostras.
Não traz números de resultado, então não entrou na tabela.

Faltam baixar à mão (os sites bloquearam o download automático):
- #11 Federated TinyML on ESP32: https://www.researchgate.net/publication/400800364
- #13 Tampered RF transmissions FL LoRa: https://www.mdpi.com/1424-8220/24/22/7336
- #17 Federated learning on embedded devices (TCC): https://upcommons.upc.edu/bitstreams/eb366834-9380-49f3-b9bc-deb8df3ea5d6/download
- #18 Neural network compression in FL (tese): https://theses.hal.science/tel-04921692/document

## Buscas usadas (para repetir ou ampliar)

- `federated learning LoRa IoT`
- `federated learning LoRa model compression quantization TinyML`
- `communication-efficient federated learning LPWAN LoRaWAN gradient compression`

## Próximos passos sugeridos

1. Ler primeiro a revisão **#16** para ter uma visão geral.
2. Ler depois os artigos **#1, #2 e #4**, que são os mais próximos do tema.
3. Baixar os PDFs para a pasta `artigos/` e anotar os resumos de leitura.
