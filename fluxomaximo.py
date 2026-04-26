"""
Algoritmo de Fluxo Máximo - Ford-Fulkerson (BFS / Edmonds-Karp)
===============================================================
Grafo (capacidades totais das arestas):
    s → a : 60
    s → b : 40
    a → c : 50
    b → c : 20
    b → d : 30
    c → d : 20
    c → t : 80
    d → t : 40

Fluxo inicial já existente (pré-carregado):
    s → a → c → t  com fluxo 50
"""

from collections import deque


# ── Grafo de capacidades residuais ──────────────────────────────────────────
# Representado como dicionário de dicionários: graph[u][v] = capacidade residual

def build_graph():
    # Capacidades totais das arestas
    capacidades = [
        ('s', 'a', 60),
        ('s', 'b', 40),
        ('a', 'c', 50),
        ('b', 'c', 20),
        ('b', 'd', 30),
        ('c', 'd', 20),
        ('c', 't', 80),
        ('d', 't', 40),
    ]

    graph = {}
    for u, v, cap in capacidades:
        for no in (u, v):
            if no not in graph:
                graph[no] = {}
        graph[u][v] = graph[u].get(v, 0) + cap
        graph[v][u] = graph[v].get(u, 0)        # aresta reversa começa em 0

    return graph


def aplicar_fluxo_inicial(graph):
    """
    Aplica o fluxo inicial de 50 unidades no caminho s → a → c → t.
    Isso reduz a capacidade residual direta e aumenta a reversa.
    """
    fluxo_inicial = 50
    caminho_inicial = [('s', 'a'), ('a', 'c'), ('c', 't')]
    for u, v in caminho_inicial:
        graph[u][v] -= fluxo_inicial
        graph[v][u] += fluxo_inicial
    print(f"Fluxo pré-existente aplicado: s → a → c → t  |  fluxo = {fluxo_inicial}")
    return fluxo_inicial


# ── BFS para encontrar caminho aumentante ────────────────────────────────────

def bfs(graph, fonte, sumidouro, pai):
    """
    Busca em largura no grafo residual.
    Retorna True se existe caminho de fonte até sumidouro.
    Preenche 'pai' com o predecessor de cada nó no caminho encontrado.
    """
    visitados = {fonte}
    fila = deque([fonte])

    while fila:
        u = fila.popleft()
        for v, cap_residual in graph[u].items():
            if v not in visitados and cap_residual > 0:
                visitados.add(v)
                pai[v] = u
                if v == sumidouro:
                    return True
                fila.append(v)
    return False


# ── Ford-Fulkerson (Edmonds-Karp) ────────────────────────────────────────────

def ford_fulkerson(graph, fonte, sumidouro, fluxo_acumulado=0):
    fluxo_total = fluxo_acumulado
    iteracao = 0

    while True:
        pai = {}
        if not bfs(graph, fonte, sumidouro, pai):
            break  # Não há mais caminhos aumentantes

        # Determinar o gargalo (menor capacidade residual no caminho)
        gargalo = float('inf')
        v = sumidouro
        caminho = []
        while v != fonte:
            u = pai[v]
            caminho.append((u, v))
            gargalo = min(gargalo, graph[u][v])
            v = u
        caminho.reverse()

        # Atualizar capacidades residuais
        for u, v in caminho:
            graph[u][v] -= gargalo
            graph[v][u] += gargalo

        fluxo_total += gargalo
        iteracao += 1

        nos_caminho = [fonte] + [v for _, v in caminho]
        caminho_str = ' → '.join(nos_caminho)

        print(f"\nIteração {iteracao}:")
        print(f"  Caminho aumentante : {caminho_str}")
        print(f"  Gargalo            : {gargalo}")
        print(f"  Novo fluxo total   : {fluxo_total}")

    return fluxo_total


# ── Exibição do grafo residual final ────────────────────────────────────────

def exibir_fluxo_final(graph_original, graph_residual):
    print("\n" + "=" * 55)
    print("FLUXO NAS ARESTAS (fluxo utilizado / capacidade):")
    print("=" * 55)
    arestas = [
        ('s', 'a', 60),
        ('s', 'b', 40),
        ('a', 'c', 50),
        ('b', 'c', 20),
        ('b', 'd', 30),
        ('c', 'd', 20),
        ('c', 't', 80),
        ('d', 't', 40),
    ]
    for u, v, cap in arestas:
        fluxo_usado = cap - graph_residual[u][v]
        print(f"  {u} → {v} :  {fluxo_usado:>3} / {cap}")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  FLUXO MÁXIMO — Ford-Fulkerson (Edmonds-Karp / BFS)")
    print("=" * 55)

    graph = build_graph()

    # Salva cópia das capacidades originais para exibição final
    graph_original = {u: dict(vizinhos) for u, vizinhos in graph.items()}

    print("\n── Fase 1: Fluxo pré-existente ──")
    fluxo_inicial = aplicar_fluxo_inicial(graph)
    print(f"  Fluxo total até agora: {fluxo_inicial}")

    print("\n── Fase 2: Buscando caminhos aumentantes ──")
    fluxo_maximo = ford_fulkerson(graph, 's', 't', fluxo_acumulado=fluxo_inicial)

    print("\n" + "=" * 55)
    print(f"  FLUXO MÁXIMO TOTAL = {fluxo_maximo}")
    print("=" * 55)

    exibir_fluxo_final(graph_original, graph)