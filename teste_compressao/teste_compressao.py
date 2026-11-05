# Primeiro teste de compressao sem IA com dados reais do INMET.
# Uso:
#   python teste_compressao.py dados/INMET_SE_MG_A531_MARIA_DA_FE_2025.CSV
#   python teste_compressao.py dados/INMET_SE_MG_A531_MARIA_DA_FE_2025.CSV exemplo
# O segundo jeito mostra, passo a passo, o dia mais frio do ano.
import sys, heapq, math
from collections import Counter

PAYLOAD_SF12 = 51
PAYLOAD_SF7 = 222


# ---------- leitura dos dados ----------
def num(s):
    s = s.strip().replace(",", ".")
    if s in ("", "-9999", "-9999.0"):
        return None
    if s.startswith("."):
        s = "0" + s
    if s.startswith("-."):
        s = "-0" + s[1:]
    return float(s)

def ler_estacao(caminho):
    with open(caminho, encoding="latin1") as f:
        linhas = f.read().splitlines()
    serie = []
    for l in linhas[9:]:
        if not l.strip():
            continue
        d = l.split(";")
        t, u = num(d[7]), num(d[15])
        serie.append((d[0], None if t is None else round(t * 10), None if u is None else round(u)))
    return serie

def blocos(serie, tamanho):
    out = []
    for i in range(0, len(serie) - tamanho + 1, tamanho):
        b = serie[i:i + tamanho]
        if all(t is not None and u is not None for _, t, u in b):
            out.append(b)
    return out

def texto(bloco):
    return "".join(f"{t / 10:.1f};{u}\n" for _, t, u in bloco).encode("ascii")


# ---------- bits ----------
class Escritor:
    def __init__(self):
        self.acc, self.n = 0, 0
    def escreve(self, valor, largura):
        self.acc = (self.acc << largura) | valor
        self.n += largura
    def bytes(self):
        pad = (-self.n) % 8
        return (self.acc << pad).to_bytes((self.n + pad) // 8, "big") if self.n else b""

class Leitor:
    def __init__(self, dados):
        self.acc = int.from_bytes(dados, "big") if dados else 0
        self.total = len(dados) * 8
        self.pos = 0
    def resta(self):
        return self.total - self.pos
    def le(self, largura):
        v = (self.acc >> (self.total - self.pos - largura)) & ((1 << largura) - 1)
        self.pos += largura
        return v


# ---------- LZW (como em Dias et al. 2026 e Oliveira Junior et al. 2023) ----------
MAX_DIC = 4096

def largura_lzw(k):
    return min(12, max(9, (254 + k).bit_length()))

def lzw_comprime(dados):
    dic = {bytes([i]): i for i in range(256)}
    prox, w, k, e = 256, b"", 0, Escritor()
    for c in dados:
        wc = w + bytes([c])
        if wc in dic:
            w = wc
            continue
        k += 1
        e.escreve(dic[w], largura_lzw(k))
        if prox < MAX_DIC:
            dic[wc] = prox
            prox += 1
        w = bytes([c])
    if w:
        k += 1
        e.escreve(dic[w], largura_lzw(k))
    return e.bytes()

def lzw_descomprime(dados):
    dic = {i: bytes([i]) for i in range(256)}
    prox, r = 256, Leitor(dados)
    if r.resta() < largura_lzw(1):
        return b""
    w = dic[r.le(largura_lzw(1))]
    out, k = [w], 1
    while True:
        k += 1
        if r.resta() < largura_lzw(k):
            break
        cod = r.le(largura_lzw(k))
        entrada = dic[cod] if cod in dic else w + w[:1]
        out.append(entrada)
        if prox < MAX_DIC:
            dic[prox] = w + entrada[:1]
            prox += 1
        w = entrada
    return b"".join(out)


# ---------- Huffman ----------
def comprimentos_huffman(freq):
    if len(freq) == 1:
        return {next(iter(freq)): 1}
    heap = [(f, i, (s,)) for i, (s, f) in enumerate(freq.items())]
    heapq.heapify(heap)
    comp = Counter()
    cont = len(heap)
    while len(heap) > 1:
        f1, _, s1 = heapq.heappop(heap)
        f2, _, s2 = heapq.heappop(heap)
        for s in s1 + s2:
            comp[s] += 1
        heapq.heappush(heap, (f1 + f2, cont, s1 + s2))
        cont += 1
    return dict(comp)

def codigos_canonicos(comp):
    codigos, cod, ant = {}, 0, 0
    for s, l in sorted(comp.items(), key=lambda x: (x[1], x[0])):
        cod <<= (l - ant)
        codigos[s] = (cod, l)
        cod += 1
        ant = l
    return codigos

def decodifica_huffman(r, codigos, n):
    inv = {v: s for s, v in codigos.items()}
    out = []
    for _ in range(n):
        cod, l = 0, 0
        while (cod, l) not in inv:
            cod = (cod << 1) | r.le(1)
            l += 1
        out.append(inv[(cod, l)])
    return out

# Huffman sobre o texto, mandando a tabela junto (como no WAI-Lab)
def huffman_texto_comprime(dados):
    comp = comprimentos_huffman(Counter(dados))
    codigos = codigos_canonicos(comp)
    cab = bytes([len(comp)]) + b"".join(bytes([s, l]) for s, l in sorted(comp.items()))
    cab += len(dados).to_bytes(2, "big")
    e = Escritor()
    for c in dados:
        e.escreve(*codigos[c])
    return cab + e.bytes()

def huffman_texto_descomprime(pacote):
    n_simb = pacote[0]
    comp = {pacote[1 + 2 * i]: pacote[2 + 2 * i] for i in range(n_simb)}
    p = 1 + 2 * n_simb
    n = int.from_bytes(pacote[p:p + 2], "big")
    return bytes(decodifica_huffman(Leitor(pacote[p + 2:]), codigos_canonicos(comp), n))


# ---------- binario simples (sem compressao) ----------
def binario(bloco):
    return b"".join(t.to_bytes(2, "big", signed=True) + bytes([u]) for _, t, u in bloco)


# ---------- codificacao por diferenca ----------
ESC = -128

def diferencas(bloco):
    dt, du = [], []
    for i in range(1, len(bloco)):
        dt.append(bloco[i][1] - bloco[i - 1][1])
        du.append(bloco[i][2] - bloco[i - 1][2])
    return dt, du

def diferenca_comprime(bloco):
    _, t0, u0 = bloco[0]
    out = bytearray(t0.to_bytes(2, "big", signed=True) + bytes([u0]))
    for i in range(1, len(bloco)):
        for j, tam in ((1, 2), (2, 1)):
            d = bloco[i][j] - bloco[i - 1][j]
            if -127 <= d <= 127:
                out += d.to_bytes(1, "big", signed=True)
            else:
                out += ESC.to_bytes(1, "big", signed=True) + bloco[i][j].to_bytes(tam, "big", signed=(j == 1))
    return bytes(out)

def diferenca_descomprime(pacote, n):
    t = int.from_bytes(pacote[0:2], "big", signed=True)
    u = pacote[2]
    out, p = [(t, u)], 3
    for _ in range(n - 1):
        vals = []
        for j, tam, ant in ((1, 2, out[-1][0]), (2, 1, out[-1][1])):
            d = int.from_bytes(pacote[p:p + 1], "big", signed=True)
            p += 1
            if d == ESC:
                vals.append(int.from_bytes(pacote[p:p + tam], "big", signed=(j == 1)))
                p += tam
            else:
                vals.append(ant + d)
        out.append(tuple(vals))
    return out

# Diferenca + Huffman com tabela fixa (calculada com os dados de janeiro; nao viaja no pacote)
def tabela_fixa(blocos_treino):
    ft, fu = Counter(range(-127, 128)), Counter(range(-127, 128))  # +1 para todo valor possivel
    ft["ESC"] += 1
    fu["ESC"] += 1
    for b in blocos_treino:
        dt, du = diferencas(b)
        ft.update(d if -127 <= d <= 127 else "ESC" for d in dt)
        fu.update(d if -127 <= d <= 127 else "ESC" for d in du)
    chave = lambda s: 999 if s == "ESC" else s
    def canon(freq):
        comp = comprimentos_huffman({chave(s): f for s, f in freq.items()})
        return codigos_canonicos(comp)
    return canon(ft), canon(fu)

def dif_huffman_comprime(bloco, tabelas):
    ct, cu = tabelas
    _, t0, u0 = bloco[0]
    e = Escritor()
    e.escreve(t0 & 0xFFFF, 16)
    e.escreve(u0, 8)
    for i in range(1, len(bloco)):
        for j, cod, larg in ((1, ct, 16), (2, cu, 8)):
            d = bloco[i][j] - bloco[i - 1][j]
            if -127 <= d <= 127:
                e.escreve(*cod[d])
            else:
                e.escreve(*cod[999])
                e.escreve(bloco[i][j] & ((1 << larg) - 1), larg)
    return e.bytes()

def dif_huffman_descomprime(pacote, n, tabelas):
    ct, cu = tabelas
    r = Leitor(pacote)
    t = r.le(16)
    t = t - 65536 if t >= 32768 else t
    out = [(t, r.le(8))]
    for _ in range(n - 1):
        vals = []
        for cod, larg, ant in ((ct, 16, out[-1][0]), (cu, 8, out[-1][1])):
            s = decodifica_huffman(r, cod, 1)[0]
            if s == 999:
                v = r.le(larg)
                if larg == 16 and v >= 32768:
                    v -= 65536
                vals.append(v)
            else:
                vals.append(ant + s)
        out.append(tuple(vals))
    return out


# ---------- teste ----------
def pacotes(tam, payload):
    return math.ceil(tam / payload)

def roda(serie, tamanho):
    todos = blocos(serie, tamanho)
    treino = [b for b in todos if b[0][0].startswith("2025/01")]
    teste = [b for b in todos if not b[0][0].startswith("2025/01")]
    tabelas = tabela_fixa(treino)
    soma = Counter()
    for b in teste:
        txt = texto(b)
        tn = [(t, u) for _, t, u in b]
        c_lzw = lzw_comprime(txt)
        c_huf = huffman_texto_comprime(txt)
        c_dif = diferenca_comprime(b)
        c_dh = dif_huffman_comprime(b, tabelas)
        assert lzw_descomprime(c_lzw) == txt
        assert huffman_texto_descomprime(c_huf) == txt
        assert diferenca_descomprime(c_dif, len(b)) == tn
        assert dif_huffman_descomprime(c_dh, len(b), tabelas) == tn
        for nome, tam in (("texto", len(txt)), ("binario", len(binario(b))), ("lzw", len(c_lzw)),
                          ("huffman", len(c_huf)), ("diferenca", len(c_dif)), ("dif_huffman", len(c_dh))):
            soma[nome] += tam
            soma[nome + "_sf12"] += pacotes(tam, PAYLOAD_SF12)
            soma[nome + "_sf7"] += pacotes(tam, PAYLOAD_SF7)
    n = len(teste)
    print(f"\n=== bloco de {tamanho} horas | blocos de teste: {n} (fev-dez), blocos de janeiro para a tabela fixa: {len(treino)} ===")
    print(f"{'metodo':<12}{'bytes/bloco':>12}{'vs texto':>10}{'vs binario':>12}{'pacotes SF12':>14}{'pacotes SF7':>13}")
    for nome in ("texto", "binario", "lzw", "huffman", "diferenca", "dif_huffman"):
        m = soma[nome] / n
        print(f"{nome:<12}{m:>12.1f}{100 * (1 - m / (soma['texto'] / n)):>9.1f}%{100 * (1 - m / (soma['binario'] / n)):>11.1f}%"
              f"{soma[nome + '_sf12'] / n:>14.2f}{soma[nome + '_sf7'] / n:>13.2f}")

def exemplo(serie):
    todos = blocos(serie, 24)
    tabelas = tabela_fixa([b for b in todos if b[0][0].startswith("2025/01")])
    teste = [b for b in todos if not b[0][0].startswith("2025/01")]
    b = min(teste, key=lambda b: min(t for _, t, _ in b))
    txt = texto(b)
    print(f"Dia mais frio (de fevereiro a dezembro): começa em {b[0][0]}, 24 leituras seguidas\n")
    print("1) As 6 primeiras leituras:")
    for i, (_, t, u) in enumerate(b[:6], 1):
        print(f"   hora {i}: {t / 10:.1f} graus e {u}% de umidade")
    print("\n2) Escritas como texto (cada letra ou número ocupa 1 byte):")
    for linha in txt.decode().splitlines()[:6]:
        print(f"   {linha:<10}  ({len(linha) + 1} bytes, contando a quebra de linha)")
    dt, du = diferencas(b)
    print("\n3) Diferença para a hora anterior, nas 23 horas seguintes:")
    print("   temperatura (em décimos de grau):", dt)
    print("   umidade (em pontos de %):        ", du)
    print("\n4) Tamanho do dia inteiro em cada método:")
    for nome, pacote in (("Texto", txt), ("LZW", lzw_comprime(txt)), ("Huffman", huffman_texto_comprime(txt)),
                         ("Binário", binario(b)), ("Diferença", diferenca_comprime(b)),
                         ("Diferença + Huffman", dif_huffman_comprime(b, tabelas))):
        print(f"   {nome:<20} {len(pacote):>4} bytes  ->  {pacotes(len(pacote), PAYLOAD_SF12)} pacote(s) em SF12")
    tn = [(t, u) for _, t, u in b]
    ok = (lzw_descomprime(lzw_comprime(txt)) == txt and huffman_texto_descomprime(huffman_texto_comprime(txt)) == txt
          and diferenca_descomprime(diferenca_comprime(b), 24) == tn
          and dif_huffman_descomprime(dif_huffman_comprime(b, tabelas), 24, tabelas) == tn)
    print("\n5) Descomprimindo de volta:", "todos voltaram exatamente iguais." if ok else "ERRO: algum não voltou igual!")


if __name__ == "__main__":
    serie = ler_estacao(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == "exemplo":
        exemplo(serie)
    else:
        print("horas no ano:", len(serie))
        for tamanho in (6, 12, 24):
            roda(serie, tamanho)
        print("\nTodos os blocos foram descomprimidos e conferidos: voltaram exatamente iguais.")
