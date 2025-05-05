from estado_quebra_cabeca import EstadoQuebraCabeca

class QuebraCabeca:
    def __init__(self):
        self.estado_inicial = EstadoQuebraCabeca(objetivo=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.estado = EstadoQuebraCabeca(objetivo=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.embaralhar()

    def foi_resolvido(self):
        return self.estado.foi_resolvido()

    def mover(self, linha, coluna):
        if (linha < 0 or linha > 2 or coluna < 0 or coluna > 2):
            print("Movimento inválido!")
            return
        self.estado.mover(linha, coluna)

    def embaralhar(self):
        self.estado_inicial.embaralhar()
        self.resetar()

    def resetar(self):
        self.estado.definir_estado(self.estado_inicial)

    def resolver(self, algoritmo, heuristica=None):
        from resolver import resolver_bfs, resolver_dfs, resolver_a_estrela

        if algoritmo == "BFS":
            return resolver_bfs(self)
        elif algoritmo == "DFS":
            return resolver_dfs(self)
        elif algoritmo == "A*":
            return resolver_a_estrela(self, heuristica)
        else:
            print("Algoritmo inválido!")
            return None
