import snap

# Définition d'une fonction pour charger les données de la communauté DBLP à partir de l'ensemble de données standard de SNAP
def load_dblp_community():
    # Téléchargement et chargement de l'ensemble de données du réseau social académique DBLP
    dblp_graph = snap.LoadEdgeList(snap.PUNGraph, path_dblp_file, 0, 1)
    return dblp_graph

# Fonction pour sauvegarder les nœuds et les arêtes dans des fichiers CSV
def save_graph_to_csv(graph, node_file, edge_file):
    # Sauvegarde des nœuds
    with open(node_file, 'w') as f:
        f.write("id\n")
        for NI in graph.Nodes():
            f.write(f"{NI.GetId()}\n")
    
    # Sauvegarde des relations
    with open(edge_file, 'w') as f:
        f.write("source,target\n")
        for EI in graph.Edges():
            f.write(f"{EI.GetSrcNId()},{EI.GetDstNId()}\n")

# Fonction principale
if __name__ == "__main__":
    # Chargement des données de la communauté DBLP
    load_dblp_file = "dataset/name/of/your/file"# Choisissez dblp fichier dans le dossier dataset
    path_dblp_file = f"dataset\{load_dblp_file}"
    dblp_graph = load_dblp_community()
    
    # Sauvegarde des nœuds et des arêtes dans des fichiers CSV
    noeds_export = f"{load_dblp_file}_noeds.csv"
    relations_export = f"{load_dblp_file}_relations.csv"
    save_graph_to_csv(dblp_graph, f"noeds_edge/{noeds_export}",
        f"noeds_edge/{relations_export}")

    print("Les données de la communauté DBLP ont été sauvegardées sous forme de fichiers CSV")
