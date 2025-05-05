import tkinter as tk
from tkinter import messagebox
from quebra_cabeca import QuebraCabeca

class InterfaceQuebraCabeca:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Quebra-Cabeça 8 Peças")

        self.quebra_cabeca = QuebraCabeca()

        self.botoes = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                botao = tk.Button(self.janela, text="", font=("Helvetica", 32), width=4, height=2,
                                  command=lambda linha=i, coluna=j: self.mover(linha, coluna))
                botao.grid(row=i, column=j)
                self.botoes[i][j] = botao

        self.botao_embaralhar = tk.Button(self.janela, text="Embaralhar", command=self.embaralhar)
        self.botao_embaralhar.grid(row=3, column=0)

        self.botao_resetar = tk.Button(self.janela, text="Resetar", command=self.resetar)
        self.botao_resetar.grid(row=3, column=1)

        self.botao_resolver = tk.Button(self.janela, text="Resolver", command=self.resolver)
        self.botao_resolver.grid(row=3, column=2)

        self.algoritmo_var = tk.StringVar(self.janela)
        self.algoritmo_var.set("BFS")

        self.menu_algoritmo = tk.OptionMenu(self.janela, self.algoritmo_var, "BFS", "DFS", "A*")
        self.menu_algoritmo.grid(row=4, column=0, columnspan=3)

        self.atualizar_interface()

    def atualizar_interface(self):
        for i in range(3):
            for j in range(3):
                valor = self.quebra_cabeca.estado.estado[i][j]
                self.botoes[i][j]["text"] = "" if valor == 0 else str(valor)

    def mover(self, linha, coluna):
        self.quebra_cabeca.mover(linha, coluna)
        self.atualizar_interface()

        if self.quebra_cabeca.foi_resolvido():
            messagebox.showinfo("Parabéns!", "Você resolveu o quebra-cabeça!")

    def embaralhar(self):
        self.quebra_cabeca.embaralhar()
        self.atualizar_interface()

    def resetar(self):
        self.quebra_cabeca.resetar()
        self.atualizar_interface()

    def resolver(self):
        algoritmo = self.algoritmo_var.get()
        heuristica = "manhattan"

        if algoritmo == "A*":
            heuristica = "euclidean"

        caminho = self.quebra_cabeca.resolver(algoritmo, heuristica)

        if caminho:
            for movimento in caminho:
                self.quebra_cabeca.mover(*movimento)
                self.atualizar_interface()
                self.janela.update()
                self.janela.after(200)
        else:
            messagebox.showinfo("Falha", "Não foi possível resolver o quebra-cabeça.")

    def executar(self):
        self.janela.mainloop()
