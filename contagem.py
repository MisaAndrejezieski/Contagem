import tkinter as tk
from tkinter import ttk, messagebox

# Valores possíveis das cartas
valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Inicializa o baralho com 32 cartas de cada valor (8 baralhos × 4 naipes)
baralho = {valor: 32 for valor in valores}

def registrar_cartas(carta_casa, carta_visitante):
    """Atualiza o contador com as cartas que saíram"""
    for carta in [carta_casa, carta_visitante]:
        if carta in baralho and baralho[carta] > 0:
            baralho[carta] -= 1
        else:
            print(f"Aviso: carta '{carta}' já esgotada ou inválida.")

def calcular_probabilidades():
    """Calcula a probabilidade de cada valor aparecer na próxima rodada"""
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
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        ttk.Label(self.root, text="Registrar Cartas", font=("Segoe UI", 16)).pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=5)

        ttk.Label(frame, text="Casa:").grid(row=0, column=0, padx=5)
        self.casa_var = tk.StringVar()
        casa_menu = ttk.Combobox(frame, textvariable=self.casa_var, values=valores, state="readonly")
        casa_menu.grid(row=0, column=1)

        ttk.Label(frame, text="Visitante:").grid(row=0, column=2, padx=5)
        self.visitante_var = tk.StringVar()
        visitante_menu = ttk.Combobox(frame, textvariable=self.visitante_var, values=valores, state="readonly")
        visitante_menu.grid(row=0, column=3)

        ttk.Button(self.root, text="Registrar", command=self.registrar).pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Restantes", "Probabilidade"), show="headings", height=13)
        self.tree.heading("Restantes", text="Cartas Restantes")
        self.tree.heading("Probabilidade", text="Probabilidade (%)")
        self.tree.column("Restantes", width=150, anchor="center")
        self.tree.column("Probabilidade", width=150, anchor="center")
        self.tree.pack(pady=10)

        ttk.Button(self.root, text="Resetar Baralho", command=self.resetar).pack(pady=5)

    def registrar(self):
        casa = self.casa_var.get()
        visitante = self.visitante_var.get()
        if not casa or not visitante:
            messagebox.showwarning("Aviso", "Selecione ambas as cartas.")
            return
        registrar_cartas(casa, visitante)
        self.update_display()

    def update_display(self):
        self.tree.delete(*self.tree.get_children())
        probs = calcular_probabilidades()
        for valor in valores:
            restantes = baralho[valor]
            prob = probs.get(valor, 0.0)
            self.tree.insert("", "end", values=(f"{valor}: {restantes}", f"{prob:.2f}"))

    def resetar(self):
        for valor in valores:
            baralho[valor] = 32
        self.update_display()
        messagebox.showinfo("Baralho Resetado", "O baralho foi reiniciado com 32 cartas por valor.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContagemApp(root)
    root.mainloop()
