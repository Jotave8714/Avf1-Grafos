# T1 — Caracterização de Redes de Escala Livre com Dados do SNAP

Investigação da hipótese de escala livre na rede de Sistemas Autônomos da Internet
utilizando o dataset **AS-733** do Stanford SNAP e a biblioteca **algs4** (Sedgewick & Wayne).

**Disciplina:** Resolução de Problemas em Grafos — Universidade de Fortaleza  
**Professor:** Prof. Me. Ricardo Carubbi

**Dataset:** [SNAP — AS-733](https://snap.stanford.edu/data/as-733.html)

---

## Como Executar

### Pré-requisitos
- Python 3.9 ou superior

### Passos

```bash
# 1. Clonar o repositório
git clone <url-do-seu-repositorio>
cd AVF1-GRAFOS

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Abrir o notebook principal
jupyter notebook notebook/redes_escala_livre_as.ipynb
```

> O dataset já está incluído em `data/entrada.txt` — nenhum download adicional é necessário.

Para executar os scripts individualmente:

```bash
python scripts/checkpoint1.py
python scripts/checkpoint2.py
python scripts/checkpoint2_sem_outliers.py
python scripts/GERAR_DOT.py
```

---

## Estrutura do Repositório

```
/
├── algs4/                                  # Biblioteca algs4-py (Sedgewick & Wayne)
├── data/
│   ├── entrada.txt                         # Dataset AS-733 (SNAP): 6.474 vértices, 13.895 arestas
│   └── as733.dot                           # Exportação do grafo para visualização no Gephi
├── notebook/
│   └── redes_escala_livre_as.ipynb         # Notebook principal — análise completa
├── scripts/
│   ├── checkpoint1.py                      # Modelagem e métricas estruturais básicas
│   ├── checkpoint2.py                      # Distribuição de graus e gráficos P(k)
│   ├── checkpoint2_sem_outliers.py         # Ajuste MLE via powerlaw (xmin automático)
│   └── GERAR_DOT.py                        # Exportação do grafo para Gephi (.dot)
└── requirements.txt                        # Dependências Python
```

---

## Resultados por Checkpoint

### Checkpoint 1 — Modelagem e Métricas Iniciais ✅
> Entrega: modelagem formal do grafo e métricas estruturais básicas.

O grafo AS-733 é uma **rede esparsa** — cada Sistema Autônomo estabelece peering
apenas com parceiros de interesse mútuo, refletindo acordos comerciais reais de roteamento BGP.

| Métrica | Valor |
|---|---|
| Vértices \|V\| | 6.474 |
| Arestas \|E\| | 13.895 |
| Grau médio | 4,2926 |
| Densidade | 0,000663 |
| Grau máximo | 2.390 |
| Grau mínimo | 1 |

---

### Checkpoint 2 — Distribuição de Graus ✅
> Entrega: gráficos P(k) em escala linear e log-log com interpretação.

Gerados três gráficos complementares via `checkpoint2.py`:

- **Histograma** — frequência absoluta por grau (escala linear)
- **PMF linear** — P(k) × k, evidenciando concentração nos graus baixos
- **PMF log-log** — revela o alinhamento linear característico de lei de potência

**Interpretação:** a escala log-log exibe comportamento aproximadamente linear na cauda,
compatível com P(k) ∝ k^(−γ) — assinatura matemática de redes scale-free.

Arquivos gerados:
- `histograma_graus.png`
- `pmf_linear.png`
- `pmf_loglog.png`

---

### Checkpoint 3 — Ajuste de Lei de Potência ✅
> Entrega: ajuste MLE, expoente γ, comparação com lognormal e conclusão.

Ajuste via **Maximum Likelihood Estimation** (Clauset et al., 2009) com `xmin`
determinado automaticamente por minimização da estatística KS (`checkpoint2_sem_outliers.py`):

| Parâmetro | Valor |
|---|---|
| Expoente γ (alpha) | 2,148 ± 0,056 |
| xmin (corte KS) | 8 |
| Vértices na cauda | 413 / 6.474 |
| Comparação (R) | > 0 — favorece power-law |

**Conclusão:** γ ≈ 2,15 situa-se no intervalo [2, 3] típico de redes scale-free reais.
Poucos ASes Tier-1 concentram a maioria das conexões — estrutura consistente com
o mecanismo de *preferential attachment* e com a topologia documentada da Internet.

Arquivo gerado:
- `ajuste_powerlaw.png`

---

### Notebook Principal — Análise Consolidada ✅
> `notebook/redes_escala_livre_as.ipynb` — segue o roteiro:

**problema → modelagem → métricas → resultados → conclusão**

| Seção | Conteúdo |
|---|---|
| 1. O Problema | Contexto da rede AS, dataset SNAP AS-733, questão central |
| 2. Configuração | Imports, algs4, configuração do ambiente |
| 3. Modelagem | Decisões de projeto, definição formal G = (V, E) |
| 4. Métricas | \|V\|, \|E\|, grau médio, densidade, máximo, mínimo, desvio |
| 5. Distribuição P(k) | Histograma, PMF linear, PMF log-log |
| 6. Ajuste MLE | powerlaw, γ, xmin, σ, comparação lognormal |
| 7. Painel Visual | 3 subplots consolidados — salvo em `painel_as733.png` |
| 8. Conclusão | Tabela de resultados, implicações práticas, referências |

---

## Referências

- Barabási, A.-L., & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509–512.
- Clauset, A., Shalizi, C. R., & Newman, M. E. J. (2009). Power-law distributions in empirical data. *SIAM Review*, 51(4), 661–703.
- Leskovec, J., Kleinberg, J., & Faloutsos, C. (2005). Graphs over time. *KDD '05*.
- SNAP — Stanford Network Analysis Project. AS-733. https://snap.stanford.edu/data/as-733.html
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.