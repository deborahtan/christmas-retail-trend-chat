from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_keywords(posts, n_clusters=3):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(posts)
    km = KMeans(n_clusters=n_clusters, random_state=42)
    km.fit(X)
    return km.labels_
