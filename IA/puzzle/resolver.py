from collections import deque
from estado_quebra_cabeca import EstadoQuebraCabeca

def resolver_bfs(quebra_cabeca):
    fronteira = deque()
    fronteira.append((quebra_cabeca.estado, []))

    explorado = set()

    while fronteira:
        estado, caminho = fronteira.popleft()

        if estado.foi_resolvido():
            print("Resolvido com BFS!")
            return caminho

        if estado not in explorado:
            explorado.add(estado)
            for proximo_estado in estado.estados_possiveis():
                movimento = estado.obter_movimento_para(proximo_estado)
                fronteira.append((proximo_estado, caminho + [movimento]))

    return None


def resolver_dfs(quebra_cabeca):
    pilha = []
    pilha.append((quebra_cabeca.estado, []))

    explorado = set()

    while pilha:
        estado, caminho = pilha.pop()

        if estado.foi_resolvido():
            print("Resolvido com DFS!")
            return caminho

        if estado not in explorado:
            explorado.add(estado)
            for proximo_estado in estado.estados_possiveis():
                movimento = estado.obter_movimento_para(proximo_estado)
                pilha.append((proximo_estado, caminho + [movimento]))

    return None


def resolver_a_estrela(quebra_cabeca, heuristica):
    from queue import PriorityQueue

    funcao_heuristica = heuristica_manhattan
    if heuristica == "euclidean":
        funcao_heuristica = heuristica_euclidiana

    fronteira = PriorityQueue()
    fronteira.put((0, quebra_cabeca.estado, []))

    explorado = set()

    while not fronteira.empty():
        _, estado, caminho = fronteira.get()

        if estado.foi_resolvido():
            print("Resolvido com A*!")
            return caminho

        if estado not in explorado:
            explorado.add(estado)
            for proximo_estado in estado.estados_possiveis():
                movimento = estado.obter_movimento_para(proximo_estado)
                prioridade = len(caminho) + funcao_heuristica(proximo_estado)
                fronteira.put((prioridade, proximo_estado, caminho + [movimento]))

    return None


def heuristica_manhattan(estado: EstadoQuebraCabeca):
    distancia = 0

    for i in range(3):
        for j in range(3):
            valor = estado.estado[i][j]
            if valor != 0:
                objetivo_i = (valor - 1) // 3
                objetivo_j = (valor - 1) % 3
                distancia += abs(i - objetivo_i) + abs(j - objetivo_j)

    return distancia


def heuristica_euclidiana(estado: EstadoQuebraCabeca):
    distancia = 0

    for i in range(3):
        for j in range(3):
            valor = estado.estado[i][j]
            if valor != 0:
                objetivo_i = (valor - 1) // 3
                objetivo_j = (valor - 1) % 3
                distancia += ((i - objetivo_i) ** 2 + (j - objetivo_j) ** 2) ** 0.5

    return distancia
