import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

nodes = ['Термінал 1', 'Термінал 2', 'Склад 1', 'Склад 2', 'Склад 3', 'Склад 4', 'Магазин 1', 'Магазин 2',
             'Магазин 3', 'Магазин 4', 'Магазин 5', 'Магазин 6', 'Магазин 7', 'Магазин 8', 'Магазин 9',
             'Магазин 10', 'Магазин 11', 'Магазин 12', 'Магазин 13', 'Магазин 14']

def draw_logistics_graph():
    # Создаем граф
    G = nx.DiGraph()

    # Узлы
   
    G.add_nodes_from(nodes)

    # Ребра
    edges = [
        ('Термінал 1', 'Склад 1', {'capacity': 25}),
        ('Термінал 1', 'Склад 2', {'capacity': 20}),
        ('Термінал 1', 'Склад 3', {'capacity': 15}),
        ('Термінал 2', 'Склад 3', {'capacity': 15}),
        ('Термінал 2', 'Склад 4', {'capacity': 30}),
        ('Термінал 2', 'Склад 2', {'capacity': 10}),
        ('Склад 1', 'Магазин 1', {'capacity': 15}),
        ('Склад 1', 'Магазин 2', {'capacity': 10}),
        ('Склад 1', 'Магазин 3', {'capacity': 20}),
        ('Склад 2', 'Магазин 4', {'capacity': 15}),
        ('Склад 2', 'Магазин 5', {'capacity': 10}),
        ('Склад 2', 'Магазин 6', {'capacity': 25}),
        ('Склад 3', 'Магазин 7', {'capacity': 20}),
        ('Склад 3', 'Магазин 8', {'capacity': 15}),
        ('Склад 3', 'Магазин 9', {'capacity': 10}),
        ('Склад 4', 'Магазин 10', {'capacity': 20}),
        ('Склад 4', 'Магазин 11', {'capacity': 10}),
        ('Склад 4', 'Магазин 12', {'capacity': 15}),
        ('Склад 4', 'Магазин 13', {'capacity': 5}),
        ('Склад 4', 'Магазин 14', {'capacity': 10}),
    ]

    G.add_edges_from(edges)

    # Позиции узлов для отрисовки
    pos = {
        'Термінал 1': (2, 2),
        'Термінал 2': (6, 2),
        'Склад 1': (3, 3),
        'Склад 2': (5, 3),
        'Склад 3': (3, 1),
        'Склад 4': (5, 1),
        'Магазин 1': (1, 4),
        'Магазин 2': (2, 4),
        'Магазин 3': (3, 4),
        'Магазин 4': (4, 4),
        'Магазин 5': (5, 4),
        'Магазин 6': (6, 4),
        'Магазин 7': (1, 0),
        'Магазин 8': (2, 0),
        'Магазин 9': (3, 0),
        'Магазин 10': (4, 0),
        'Магазин 11': (5, 0),
        'Магазин 12': (6, 0),
        'Магазин 13': (7, 0),
        'Магазин 14': (8, 0),
    }

    # Отрисовка графа
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue",
            font_size=10, font_weight="bold", arrowsize=15)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Логістична мережа")
    plt.show()


def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    # Ініціалізуємо матрицю потоку нулем
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node

        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        max_flow += path_flow

    return max_flow


def main():
    draw_logistics_graph()

    capacity_matrix = [
        [0,  0, 25, 20, 15,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0, 10, 15, 30,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0, 15, 10, 20,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0, 15, 10,
            25,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0, 20, 15, 10,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0, 20, 10, 15,  5, 10],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]


    sources = [0, 1]  # Джерела
    sinks = range(6, 20)  # Споживачі

    for source in sources:
        for sink in sinks:
          max_flow = edmonds_karp(capacity_matrix, source, sink)
          print(f"Максимальний потік ( {nodes[source]} -> {nodes[sink]}): {max_flow}")


if __name__ == "__main__":
    main()
