import tkinter as tk
from tkinter import ttk, messagebox
import random

valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
baralho = {valor: 32 for valor in valores}

def registrar_cartas(carta_casa, carta_visitante):
    for carta in [carta_casa, carta_visitante]:
        if carta in baralho and baralho[carta] > 0:
            baralho[carta] -= 1
        else:
            print(f"Aviso: carta '{carta}' já esgotada ou inválida.")

def calcular_probabilidades():
    total_restante = sum(baralho.values())
    if total_restante == 0:
        return {valor: 0.0 for valor in valores}
    return {
        valor: round((baralho[valor] / total_restante) * 100, 2)
        for valor in valores
    }

class ContagemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador de Cartas")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        ttk.Label(self.root, text="Registrar Cartas", font=("Segoe UI", 16)).pack(pady=10)

        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(pady=5)

        ttk.Label(entry_frame, text="Casa:").grid(row=0, column=0, padx=5)
        self.casa_entry = ttk.Entry(entry_frame, width=10)
        self.casa_entry.grid(row=0, column=1)

        ttk.Label(entry_frame, text="Visitante:").grid(row=0, column=2, padx=5)
        self.visitante_entry = ttk.Entry(entry_frame, width=10)
        self.visitante_entry.grid(row=0, column=3)

        self.root.bind("<Return>", lambda e: self.registrar())
        self.root.bind("<space>", lambda e: self.registrar())

        ttk.Button(self.root, text="Registrar", command=self.registrar).pack(pady=10)

        ttk.Label(self.root, text="Ou clique nas cartas que saíram:", font=("Segoe UI", 12)).pack(pady=5)

        self.botao_frame = ttk.Frame(self.root)
        self.botao_frame.pack(pady=5)

        for i, valor in enumerate(valores):
            btn = ttk.Button(self.botao_frame, text=valor, width=5,
                             command=lambda v=valor: self.selecionar_carta(v))
            btn.grid(row=i // 7, column=i % 7, padx=3, pady=3)

        self.tree = ttk.Treeview(self.root, columns=("Valor", "Restantes", "Probabilidade"), show="headings", height=13)
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Restantes", text="Cartas Restantes")
        self.tree.heading("Probabilidade", text="Probabilidade (%)")
        self.tree.column("Valor", width=80, anchor="center")
        self.tree.column("Restantes", width=150, anchor="center")
        self.tree.column("Probabilidade", width=150, anchor="center")
        self.tree.pack(pady=10)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Simular Próxima Rodada", command=self.simular_rodada).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Resetar Baralho", command=self.resetar).grid(row=0, column=1, padx=10)

    def selecionar_carta(self, valor):
        if not self.casa_entry.get():
            self.casa_entry.insert(0, valor)
        elif not self.visitante_entry.get():
            self.visitante_entry.insert(0, valor)
        else:
            self.registrar()

    def registrar(self):
        casa = self.casa_entry.get().strip().upper()
        visitante = self.visitante_entry.get().strip().upper()
        if casa not in valores or visitante not in valores:
            messagebox.showerror("Erro", "Digite ou selecione valores válidos (2–10, J, Q, K, A).")
            return
        registrar_cartas(casa, visitante)
        self.casa_entry.delete(0, tk.END)
        self.visitante_entry.delete(0, tk.END)
        self.update_display()

    def update_display(self):
        self.tree.delete(*self.tree.get_children())
        probs = calcular_probabilidades()
        for valor in valores:
            restantes = baralho[valor]
            prob = probs.get(valor, 0.0)
            self.tree.insert("", "end", values=(valor, restantes, f"{prob:.2f}"))

    def resetar(self):
        for valor in valores:
            baralho[valor] = 32
        self.update_display()
        messagebox.showinfo("Baralho Resetado", "O baralho foi reiniciado com 32 cartas por valor.")

    def simular_rodada(self):
        cartas_disponiveis = []
        for valor in valores:
            cartas_disponiveis.extend([valor] * baralho[valor])

        if len(cartas_disponiveis) < 2:
            messagebox.showwarning("Aviso", "Não há cartas suficientes para simular.")
            return

        casa = random.choice(cartas_disponiveis)
        cartas_disponiveis.remove(casa)
        visitante = random.choice(cartas_disponiveis)

        ordem = {v: i for i, v in enumerate(valores)}
        if ordem[casa] > ordem[visitante]:
            resultado = f"Carta Casa ({casa}) vence sobre Visitante ({visitante})"
        elif ordem[casa] < ordem[visitante]:
            resultado = f"Carta Visitante ({visitante}) vence sobre Casa ({casa})"
        else:
            resultado = f"Empate com carta {casa}"

        registrar_cartas(casa, visitante)
        self.update_display()
        messagebox.showinfo("Simulação", f"Casa: {casa}\nVisitante: {visitante}\n\n{resultado}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContagemApp(root)
    root.mainloop()

