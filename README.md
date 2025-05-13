# Algoritmo Dois-Otimal (2-Opt) para o Caixeiro Viajante

Este projeto implementa o algoritmo Dois-Otimal (2-Opt) para encontrar um ciclo Hamiltoniano de peso mínimo em um grafo completo ponderado.

## Como funciona o algoritmo?

O algoritmo começa com um ciclo Hamiltoniano inicial e, iterativamente, tenta melhorar o ciclo trocando segmentos de vértices, até não ser possível reduzir mais o peso total do ciclo.

---

## Passo a passo do código

### 1. Criação da matriz de adjacência

```python
def criar_matriz_adjacencia(edges, n):
    matriz = [[float('inf')] * n for _ in range(n)]
    for u, v, peso in edges:
        matriz[u][v] = peso
        matriz[v][u] = peso  # grafo não direcionado
    return matriz
```

A função `criar_matriz_adjacencia` transforma a lista de arestas em uma matriz para acesso rápido aos pesos entre vértices.

### 2. Geração do ciclo Hamiltoniano inicial

```python
def ciclo_inicial(n):
    ciclo = list(range(1, n+1))
    ciclo.append(1)  # volta ao início
    return ciclo
```

O ciclo inicial é simplesmente a ordem natural dos vértices (de 1 a 7), retornando ao ponto de partida.

### 3. Cálculo do peso do ciclo

```python
def peso_ciclo(ciclo, matriz):
    return sum(matriz[ciclo[i]][ciclo[i+1]] for i in range(len(ciclo)-1))
```

A função `peso_ciclo` soma os pesos das arestas do ciclo.

### 4. Algoritmo Dois-Otimal (2-Opt)

```python
def dois_opt(matriz, ciclo):
    n = len(ciclo) - 1
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(1, n-1):
            for j in range(i+1, n):
                if j - i == 1:
                    continue  # não faz sentido inverter arestas adjacentes
                novo_ciclo = ciclo[:i] + ciclo[i:j][::-1] + ciclo[j:]
                if peso_ciclo(novo_ciclo, matriz) < peso_ciclo(ciclo, matriz):
                    ciclo = novo_ciclo
                    melhorou = True
    return ciclo
```

O algoritmo tenta inverter segmentos do ciclo para encontrar uma configuração de menor peso, repetindo até não haver mais melhorias.

### 5. Visualização do ciclo ótimo com Matplotlib

O código agora plota o grafo e destaca o melhor ciclo encontrado, mostrando os vértices em círculo, o caminho ótimo em azul e os pesos das arestas.

```python
import numpy as np
import matplotlib.pyplot as plt

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
```

### 6. Exemplo de uso

```python
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
    matriz = criar_matriz_adjacencia(edges, n+1)  # n+1 para incluir o vértice 7
    ciclo = list(range(1, n+1))
    ciclo.append(1)  # volta ao início
    print("Ciclo inicial:", ciclo)
    print("Peso inicial:", peso_ciclo(ciclo, matriz))
    ciclo_otimizado = dois_opt(matriz, ciclo)
    print("Ciclo otimizado:", ciclo_otimizado)
    print("Peso otimizado:", peso_ciclo(ciclo_otimizado, matriz))
    plotar_ciclo(ciclo_otimizado, matriz)
```

O exemplo utiliza um grafo com 7 vértices, mostrando o ciclo inicial, o ciclo otimizado e o gráfico do melhor caminho.

---

## Como executar

1. Certifique-se de ter o matplotlib e numpy instalados:

```
pip install matplotlib numpy
```

2. Execute o arquivo `caxeiro_viajante.py`:

```
python caxeiro_viajante.py
```

---
