import copy
import random

class EstadoQuebraCabeca:
    def __init__(self, estado=None, objetivo=None):
        self.estado = estado or [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.objetivo = objetivo or [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __eq__(self, outro):
        return self.estado == outro.estado

    def __hash__(self):
        return hash(str(self.estado))

    def __lt__(self, outro):
        return True  # Necessário para a fila de prioridade

    def foi_resolvido(self):
        return self.estado == self.objetivo

    def mover(self, linha, coluna):
        linha_zero, coluna_zero = self._posicao_zero()
        if abs(linha_zero - linha) + abs(coluna_zero - coluna) == 1:
            self.estado[linha_zero][coluna_zero], self.estado[linha][coluna] = \
                self.estado[linha][coluna], self.estado[linha_zero][coluna_zero]

    def embaralhar(self):
        for _ in range(100):
            linha, coluna = self._posicao_zero()
            movimentos = []

            if linha > 0: movimentos.append((linha - 1, coluna))
            if linha < 2: movimentos.append((linha + 1, coluna))
            if coluna > 0: movimentos.append((linha, coluna - 1))
            if coluna < 2: movimentos.append((linha, coluna + 1))

            destino = random.choice(movimentos)
            self.mover(destino[0], destino[1])

    def definir_estado(self, outro_estado):
        self.estado = copy.deepcopy(outro_estado.estado)

    def _posicao_zero(self):
        for i in range(3):
            for j in range(3):
                if self.estado[i][j] == 0:
                    return i, j

    def estados_possiveis(self):
        estados = []
        linha_zero, coluna_zero = self._posicao_zero()

        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in movimentos:
            nova_linha, nova_coluna = linha_zero + dx, coluna_zero + dy
            if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
                novo_estado = copy.deepcopy(self)
                novo_estado.mover(nova_linha, nova_coluna)
                estados.append(novo_estado)

        return estados

    def obter_movimento_para(self, outro_estado):
        for i in range(3):
            for j in range(3):
                if self.estado[i][j] != outro_estado.estado[i][j]:
                    if self.estado[i][j] == 0:
                        return (i, j)
                    else:
                        return (i, j)
