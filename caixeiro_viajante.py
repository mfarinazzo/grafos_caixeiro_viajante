import itertools
import matplotlib.pyplot as plt
import numpy as np

# Função para criar matriz de adjacência a partir da lista de arestas
# edges: lista de tuplas (u, v, peso)
def criar_matriz_adjacencia(edges, n):
    matriz = [[float('inf')] * (n+1) for _ in range(n+1)]  # n+1 para indexar de 1 a n
    for u, v, peso in edges:
        matriz[u][v] = peso
        matriz[v][u] = peso  # grafo não direcionado
    return matriz

# Gera ciclo Hamiltoniano inicial (ordem natural dos vértices)
def ciclo_inicial(n):
    ciclo = list(range(1, n+1))
    ciclo.append(1)  # volta ao início
    return ciclo

# Calcula o peso total de um ciclo
def peso_ciclo(ciclo, matriz):
    return sum(matriz[ciclo[i]][ciclo[i+1]] for i in range(len(ciclo)-1))

# Algoritmo Dois-Otimal (2-Opt)
def dois_opt(matriz, ciclo):
    n = len(ciclo) - 1  # ciclo inclui o retorno ao início
    w = peso_ciclo(ciclo, matriz)
    i = 0
    j = i + 2
    while i <= n - 2:
        if j > n - 1:
            i += 1
            if i <= n - 2:
                j = i + 2
            continue
        # Troca o segmento entre i+1 e j (inclusive)
        Cij = ciclo[:i+1] + ciclo[i+1:j+1][::-1] + ciclo[j+1:]
        # Cálculo incremental do novo peso
        w_ij = (
            w
            - matriz[ciclo[i]][ciclo[i+1]]
            - matriz[ciclo[j]][ciclo[(j+1)%n]]
            + matriz[ciclo[i]][ciclo[j]]
            + matriz[ciclo[i+1]][ciclo[(j+1)%n]]
        )
        print(f"Testando inversão entre {ciclo[i+1]} e {ciclo[j]}: ciclo = {Cij}")
        print(f"  Peso atual: {w} | Peso após inversão: {w_ij}")
        if w_ij < w:
            ciclo = Cij
            w = w_ij
            i = 0
            j = i + 2
        else:
            j += 1
    return ciclo

# Função para testar todas as permutações possíveis e encontrar o ciclo de menor peso
def brute_force_tsp(matriz, n):
    vertices = list(range(2, n+1))  # fixa o vértice 1 como início/fim
    melhor_ciclo = None
    melhor_peso = float('inf')
    for perm in itertools.permutations(vertices):
        ciclo = [1] + list(perm) + [1]
        peso = peso_ciclo(ciclo, matriz)
        if peso < melhor_peso:
            melhor_peso = peso
            melhor_ciclo = ciclo
    return melhor_ciclo, melhor_peso

# Função para plotar o grafo e o ciclo encontrado
# Os vértices serão posicionados em círculo para visualização
def plotar_ciclo(ciclo, matriz):
    n = len(matriz) - 1
    # Coordenadas dos vértices em círculo
    angulos = np.linspace(0, 2 * np.pi, n, endpoint=False)
    xs = np.cos(angulos)
    ys = np.sin(angulos)
    pos = {i+1: (xs[i], ys[i]) for i in range(n)}

    plt.figure(figsize=(7,7))
    # Desenha todas as arestas do grafo
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            x0, y0 = pos[i]
            x1, y1 = pos[j]
            plt.plot([x0, x1], [y0, y1], 'gray', alpha=0.3, zorder=1)
            # Mostra pesos
            mx, my = (x0+x1)/2, (y0+y1)/2
            if matriz[i][j] != float('inf'):
                plt.text(mx, my, str(matriz[i][j]), fontsize=9, color='gray', ha='center', va='center', zorder=5, bbox=dict(facecolor='white', edgecolor='none', alpha=0.6, boxstyle='round,pad=0.1'))

    # Destaca o ciclo encontrado
    for i in range(len(ciclo)-1):
        a, b = ciclo[i], ciclo[i+1]
        x0, y0 = pos[a]
        x1, y1 = pos[b]
        plt.plot([x0, x1], [y0, y1], 'b', linewidth=2.5, zorder=2)

    # Plota os vértices
    for i in range(1, n+1):
        x, y = pos[i]
        plt.scatter(x, y, s=300, color='orange', zorder=3)
        plt.text(x, y, str(i), fontsize=14, ha='center', va='center', zorder=4, color='black')

    plt.title('Melhor ciclo encontrado pelo 2-Opt')
    plt.axis('off')
    plt.show()

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo: grafo completo com 7 vértices (vértices de 1 a 7)
    edges = [
        (1, 2, 18), (1, 3, 17), (1, 4, 23), (1, 5, 12), (1, 6, 19), (1, 7, 11),
        (2, 3, 26), (2, 4, 31), (2, 5, 20), (2, 6, 30), (2, 7, 8),
        (3, 4, 16), (3, 5, 11), (3, 6, 9), (3, 7, 4),
        (4, 5, 17), (4, 6, 19), (4, 7, 9),
        (5, 6, 14), (5, 7, 10),
        (6, 7, 7)
    ]
    n = 7
    matriz = criar_matriz_adjacencia(edges, n)  # n em vez de n+1
    ciclo = list(range(1, n+1))
    ciclo.append(1)  # volta ao início
    print("Ciclo inicial:", ciclo)
    print("Peso inicial:", peso_ciclo(ciclo, matriz))
    ciclo_otimizado = dois_opt(matriz, ciclo)
    print("Ciclo otimizado:", ciclo_otimizado)
    print("Peso otimizado:", peso_ciclo(ciclo_otimizado, matriz))
    plotar_ciclo(ciclo_otimizado, matriz)

    print("\n--- Força Bruta (ótimo global) ---")
    ciclo_bruto, peso_bruto = brute_force_tsp(matriz, n)
    print("Melhor ciclo (força bruta):", ciclo_bruto)
    print("Peso ótimo global:", peso_bruto)
    plotar_ciclo(ciclo_bruto, matriz)
