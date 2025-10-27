# contagem.py
# Sistema de contagem de cartas para o jogo Futebol ao Vivo

valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
baralho = {valor: 32 for valor in valores}  # 8 baralhos × 4 naipes

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
        print("Todas as cartas foram usadas.")
        return {}
    probabilidades = {
        valor: round((baralho[valor] / total_restante) * 100, 2)
        for valor in valores
    }
    return probabilidades

def mostrar_status():
    """Exibe o status atual do baralho"""
    print("\nCartas restantes:")
    for valor in valores:
        print(f"{valor}: {baralho[valor]} cartas")
    print("\nProbabilidades de saída na próxima rodada:")
    probs = calcular_probabilidades()
    for valor, prob in probs.items():
        print(f"{valor}: {prob}%")

# Exemplo de uso
if __name__ == "__main__":
    print("Sistema de contagem iniciado.")
    while True:
        entrada = input("\nDigite as cartas (Casa,Visitante) ou 'sair': ").strip()
        if entrada.lower() == 'sair':
            break
        try:
            casa, visitante = entrada.split(',')
            registrar_cartas(casa.strip().upper(), visitante.strip().upper())
            mostrar_status()
        except ValueError:
            print("Entrada inválida. Use o formato: 7,K ou digite 'sair'.")
