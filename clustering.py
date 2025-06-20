from sklearn.cluster import KMeans

def aplicar_kmeans(dados, n_clusters=2, random_state=42):
    """Aplica KMeans ao conjunto de dados escalados."""
    modelo = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    modelo.fit(dados)
    return modelo.labels_, modelo.cluster_centers_
