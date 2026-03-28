import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import powerlaw
from algs4.graph import Graph


def inicializar_grafo_as():
    # Carrega o dataset AS-733 e monta o grafo não-dirigido via algs4
    arquivo = Path(__file__).resolve().parent.parent / "data" / "entrada.txt"

    with open(arquivo, "r", encoding="utf-8") as f:
        total_vertices = int(f.readline().strip())
        f.readline()  # descarta linha de contagem de arestas
        grafo = Graph(total_vertices)
        for registro in f:
            registro = registro.strip()
            if not registro:
                continue
            a, b = map(int, registro.split())
            grafo.add_edge(a, b)

    return grafo


def obter_sequencia_graus(grafo):
    # Coleta o grau de cada vértice em uma lista indexada por vértice
    n = grafo.V if not callable(grafo.V) else grafo.V()
    return [grafo.degree(i) for i in range(n)]


def estimar_lei_de_potencia(sequencia):
    # Ajusta lei de potência via MLE (Clauset et al., 2009)
    # xmin é determinado automaticamente por minimização da estatística KS
    arr = np.array(sequencia, dtype=float)
    arr = arr[arr > 0]  # remove grau zero antes do ajuste

    ajuste = powerlaw.Fit(arr, discrete=True, verbose=False)

    gamma = ajuste.power_law.alpha
    xmin  = ajuste.power_law.xmin

    # Likelihood ratio: R > 0 favorece power-law; R < 0 favorece lognormal
    R, p_valor = ajuste.distribution_compare("power_law", "lognormal")

    return ajuste, gamma, xmin, R, p_valor


def gerar_grafico_ajuste(ajuste, destino="ajuste_powerlaw.png"):
    # Plota P(k) observado e curva do ajuste MLE em escala log-log
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    ajuste.plot_pdf(ax=ax, marker="o", ls="", alpha=0.65,
                    color="#4878CF", label="P(k) observado")
    ajuste.power_law.plot_pdf(
        ax=ax,
        linestyle="--",
        linewidth=2,
        color="#D65F5F",
        label=f"Ajuste MLE — γ = {ajuste.power_law.alpha:.3f}, xmin = {ajuste.power_law.xmin:.0f}"
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Ajuste Lei de Potência — Log-Log (MLE)", fontweight="bold")
    ax.set_xlabel("Grau k (escala logarítmica)")
    ax.set_ylabel("P(k) (escala logarítmica)")
    ax.grid(True, which="both", linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    grafo     = inicializar_grafo_as()
    sequencia = obter_sequencia_graus(grafo)

    n = grafo.V if not callable(grafo.V) else grafo.V()
    m = grafo.E if not callable(grafo.E) else grafo.E()

    ajuste, gamma, xmin, R, p_valor = estimar_lei_de_potencia(sequencia)
    gerar_grafico_ajuste(ajuste, "ajuste_powerlaw.png")

    n_cauda = int((np.array(sequencia) >= xmin).sum())

    print("\n--- Ajuste Lei de Potência (MLE / Clauset et al., 2009) ---")
    print(f"  Expoente γ (alpha)  : {gamma:.4f}")
    print(f"  xmin (corte KS)     : {xmin:.1f}")
    print(f"  Vértices na cauda   : {n_cauda} / {n}")

    print("\n--- Comparação: power-law vs lognormal ---")
    print(f"  R = {R:.4f}  ({'favorece power-law' if R > 0 else 'favorece lognormal'})")
    print(f"  p = {p_valor:.4f}")

    print("\n--- Informações do grafo ---")
    print(f"  Vértices |V| : {n}")
    print(f"  Arestas  |E| : {m}")

    print("\nArquivo gerado:")
    print("  ajuste_powerlaw.png")


if __name__ == "__main__":
    main()
