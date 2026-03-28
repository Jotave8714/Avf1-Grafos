import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algs4.graph import Graph


def inicializar_grafo_as():
    # Constrói o grafo de Sistemas Autônomos a partir do dataset AS-733 (SNAP)
    arquivo = Path(__file__).resolve().parent.parent / 'data' / 'entrada.txt'

    with open(arquivo, 'r', encoding='utf-8') as f:
        total_vertices = int(f.readline().strip())
        f.readline()  # linha com total de arestas — não utilizada na construção
        grafo = Graph(total_vertices)
        for registro in f:
            if registro.strip():
                a, b = map(int, registro.split())
                grafo.add_edge(a, b)

    return grafo


def calcular_metricas(grafo):
    # Retorna número de vértices, arestas, grau médio e densidade do grafo
    n = grafo.V() if callable(grafo.V) else grafo.V
    m = grafo.E() if callable(grafo.E) else grafo.E

    # Pelo handshaking lemma: soma de todos os graus = 2|E|
    media_grau = (2 * m) / n

    # Densidade: proporção de arestas presentes em relação ao máximo possível
    # Para grafo simples não-dirigido: max_arestas = n*(n-1)/2
    dens = m / (n * (n - 1) / 2)

    return n, m, media_grau, dens


if __name__ == "__main__":
    try:
        g = inicializar_grafo_as()
        n, m, media_grau, dens = calcular_metricas(g)

        print("=" * 40)
        print(f"  Vértices  |V| : {n}")
        print(f"  Arestas   |E| : {m}")
        print(f"  Grau médio    : {media_grau:.4f}")
        print(f"  Densidade     : {dens:.6f}")
        print("=" * 40)

    except Exception as ex:
        print(f"[ERRO] Falha ao processar o grafo: {ex}")
