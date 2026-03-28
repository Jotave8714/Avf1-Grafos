import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from algs4.graph import Graph


def inicializar_grafo_as():
    # Lê o dataset AS-733 no formato SNAP:
    #   linha 1 : total de vértices
    #   linha 2 : total de arestas (ignorada)
    #   demais  : pares "a b" representando cada aresta
    arquivo = Path(__file__).resolve().parent.parent / "data" / "entrada.txt"

    with open(arquivo, "r", encoding="utf-8") as f:
        total_vertices = int(f.readline().strip())
        f.readline()  # descarta contagem de arestas
        grafo = Graph(total_vertices)
        for registro in f:
            registro = registro.strip()
            if not registro:
                continue
            a, b = map(int, registro.split())
            grafo.add_edge(a, b)

    return grafo


def obter_sequencia_graus(grafo):
    # Retorna lista onde a posição i contém o grau do vértice i
    n = grafo.V if not callable(grafo.V) else grafo.V()
    return [grafo.degree(i) for i in range(n)]


def distribuicao_probabilidade(sequencia):
    # Calcula P(k) = contagem(k) / N para cada grau k distinto
    freq = Counter(sequencia)
    ks = np.array(sorted(freq.keys()), dtype=int)
    n_total = len(sequencia)
    pk = np.array([freq[k] / n_total for k in ks], dtype=float)
    return ks, pk


def gerar_histograma(sequencia, destino="histograma_graus.png"):
    # Histograma de frequências absolutas em escala linear
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(sequencia, bins=50, color="#4878CF", edgecolor="white", alpha=0.88)
    ax.set_title("Histograma de Graus — Rede AS-733", fontweight="bold")
    ax.set_xlabel("Grau k")
    ax.set_ylabel("Número de vértices")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(destino, dpi=300, bbox_inches="tight")
    plt.close(fig)


def gerar_pmf_linear(ks, pk, destino="pmf_linear.png"):
    # Gráfico de dispersão P(k) x k em escala linear
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(ks, pk, s=30, color="#6ACC65", alpha=0.78)
    ax.set_title("Função de Massa de Probabilidade P(k) — Escala Linear", fontweight="bold")
    ax.set_xlabel("Grau k")
    ax.set_ylabel("P(k)")
    ax.grid(linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(destino, dpi=300, bbox_inches="tight")
    plt.close(fig)


def gerar_pmf_loglog(ks, pk, destino="pmf_loglog.png"):
    # Gráfico log-log sem ajuste — apenas pontos observados com k > 0 e P(k) > 0
    mascara = (ks > 0) & (pk > 0)

    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(ks[mascara], pk[mascara], s=30, color="#D65F5F", alpha=0.78,
               label="P(k) observado")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Função de Massa de Probabilidade P(k) — Escala Log-Log", fontweight="bold")
    ax.set_xlabel("Grau k (escala logarítmica)")
    ax.set_ylabel("P(k) (escala logarítmica)")
    ax.grid(True, which="both", linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    grafo = inicializar_grafo_as()
    sequencia = obter_sequencia_graus(grafo)

    n = grafo.V if not callable(grafo.V) else grafo.V()
    m = grafo.E if not callable(grafo.E) else grafo.E()

    ks, pk = distribuicao_probabilidade(sequencia)

    gerar_histograma(sequencia,   "histograma_graus.png")
    gerar_pmf_linear(ks, pk,      "pmf_linear.png")
    gerar_pmf_loglog(ks, pk,      "pmf_loglog.png")

    arr = np.array(sequencia, dtype=float)
    arr = arr[arr > 0]

    print("\n--- Métricas — Checkpoint 2 (sem ajuste de lei de potência) ---")
    print(f"  Vértices  |V|  : {n}")
    print(f"  Arestas   |E|  : {m}")
    print(f"  Grau mínimo    : {int(arr.min())}")
    print(f"  Grau máximo    : {int(arr.max())}")
    print(f"  Grau médio     : {arr.mean():.4f}")
    print(f"  Desvio padrão  : {arr.std():.4f}")
    print(f"  Mediana        : {np.median(arr):.1f}")
    print("\nArquivos gerados:")
    print("  histograma_graus.png")
    print("  pmf_linear.png")
    print("  pmf_loglog.png")


if __name__ == "__main__":
    main()
