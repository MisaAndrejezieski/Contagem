import tkinter as tk
from tkinter import ttk, messagebox

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
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        ttk.Label(self.root, text="Registrar Cartas", font=("Segoe UI", 16)).pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=5)

        ttk.Label(frame, text="Casa:").grid(row=0, column=0, padx=5)
        self.casa_entry = ttk.Entry(frame, width=10)
        self.casa_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Visitante:").grid(row=0, column=2, padx=5)
        self.visitante_entry = ttk.Entry(frame, width=10)
        self.visitante_entry.grid(row=0, column=3)

        ttk.Button(self.root, text="Registrar", command=self.registrar).pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Restantes", "Probabilidade"), show="headings", height=13)
        self.tree.heading("Restantes", text="Cartas Restantes")
        self.tree.heading("Probabilidade", text="Probabilidade (%)")
        self.tree.column("Restantes", width=150, anchor="center")
        self.tree.column("Probabilidade", width=150, anchor="center")
        self.tree.pack(pady=10)

        ttk.Button(self.root, text="Resetar Baralho", command=self.resetar).pack(pady=5)

    def registrar(self):
        casa = self.casa_entry.get().strip().upper()
        visitante = self.visitante_entry.get().strip().upper()
        if casa not in valores or visitante not in valores:
            messagebox.showerror("Erro", "Digite valores válidos (2–10, J, Q, K, A).")
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
