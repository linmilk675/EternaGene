import networkx as nx
import matplotlib.pyplot as plt
from loaders.string_loader import fetch_string_interactions

def build_interaction_graph(gene_name, score_threshold=0.7):
    """
    Загружает взаимодействия гена и строит граф.

    Parameters:
        gene_name (str): название центрального гена
        score_threshold (float): порог уверенности взаимодействия (0–1)

    Returns:
        networkx.Graph: объект графа
    """
    interactions = fetch_string_interactions(gene_name)
    G = nx.Graph()

    for i in interactions:
        gene1 = gene_name
        gene2 = i["partner"]
        score = i["score"]

        if score >= score_threshold:
            G.add_edge(gene1, gene2, weight=score)

    return G

def plot_interaction_graph(G, central_gene=None, save_path=None):
    """
    Визуализирует граф взаимодействий.

    Parameters:
        G (networkx.Graph): граф взаимодействий
        central_gene (str): имя центрального гена для выделения
        save_path (str): путь к файлу для сохранения картинки (если None, показать)
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)

    node_colors = ['red' if node == central_gene else 'skyblue' for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.6)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        return save_path
        #plt.savefig(save_path, bbox_inches='tight')
        #plt.close()
    else:
        plt.title(f"Gene Interaction Network: {central_gene}")
        plt.axis('off')
        plt.show()
        
