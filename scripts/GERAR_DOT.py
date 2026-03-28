import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algs4.graph import Graph


def exportar_dot():
    # Caminhos de entrada e saída
    arquivo_entrada = Path(__file__).resolve().parent.parent / "data" / "entrada.txt"
    arquivo_saida   = Path(__file__).resolve().parent.parent / "data" / "as733.dot"

    # Carrega o grafo a partir do dataset AS-733
    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        total_vertices = int(f.readline().strip())
        total_arestas  = int(f.readline().strip())
        grafo = Graph(total_vertices)

        for registro in f:
            if registro.strip():
                a, b = map(int, registro.split())
                grafo.add_edge(a, b)

    n = grafo.V
    print(f"Grafo montado: {n} vértices, {total_arestas} arestas.")

    # Exporta para formato DOT (compatível com Gephi / Graphviz)
    # Usa conjunto de pares já escritos para evitar arestas duplicadas
    pares_escritos = set()

    with open(arquivo_saida, "w", encoding="utf-8") as out:
        out.write("graph AS733 {\n")
        for i in range(n):
            for j in grafo.adj[i]:
                par = (min(i, j), max(i, j))
                if par not in pares_escritos:
                    out.write(f"    {i} -- {j};\n")
                    pares_escritos.add(par)
        out.write("}\n")

    print(f"Exportação concluída: '{arquivo_saida.name}' pronto para visualização no Gephi.")


if __name__ == "__main__":
    exportar_dot()
