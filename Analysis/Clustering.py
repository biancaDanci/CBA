from Feature_for_block import FeatureBlockLevel
from Css_properties_block_lvl import CSSFeatureBlockLevel
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.metrics.pairwise import euclidean_distances

from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler


def color_blocks(browser, color, blocks):
    for block in blocks:
        browser.execute_script("arguments[0].setAttribute('style', 'background-color:arguments[1];');", block, color)


def check_interconnection(clusters_text):
    list_of_interconnection = []

    for elem in clusters_text:
        found = 0
        for text_elem in elem:
            for i in range(0, len(clusters_text)):
                if not clusters_text.index(elem) == i and text_elem in clusters_text[i]:
                    found = found+1
        list_of_interconnection.append(found)

    return list_of_interconnection.index(max(list_of_interconnection))


def show_clusters(cluster_labels, bloks, cl_nu, browser, url):
    browser.set_window_size(2200, 1800)
    path = '/home/bia/PycharmProjects/CBA/Outputs'+url.split('.')[1]+'.png'
    browser.save_screenshot(path)
    for block in bloks:
        browser.execute_script("arguments[0].setAttribute('style', 'background-color:red;');", block)
    import pdb
    pdb.set_trace()
    list_of_cluters = []
    for i in range(0, cl_nu):
        print(" \n \n \n cluster {}".format(i))
        color_blocks(browser, 'red', bloks)
        cluster_blocks = [block for (label, block) in zip(cluster_labels, bloks) if label == i]
        text_list = []
        for block in cluster_blocks:
            print(block.text)
            text_list.append(block.text)
            browser.execute_script("arguments[0].setAttribute('style', 'background-color:green;');", block)
        path = '/home/bia/PycharmProjects/CBA/Outputs' + url.split('.')[1]+'_'+str(i) + '.png'

        list_of_cluters.append(text_list)
    # cl_to_be_removed = check_interconnection(list_of_cluters)
        browser.save_screenshot(path)


def compute_and_show_results(num_clusters, data_and_elems):

    data = data_and_elems['data']
    elems = data_and_elems['blocks']
    min_max_scaler = MinMaxScaler()
    #   feed in a numpy array
    X_train_norm = min_max_scaler.fit_transform(data)
    X = np.array(X_train_norm)

    clusterer = KMeans(n_clusters=num_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(X)
    dists = euclidean_distances(clusterer.cluster_centers_)
    sum_of_distances = []
    for centroid_list in dists:
        sum = 0
        for elem in centroid_list:
            sum = sum + elem
        sum_of_distances.append(sum)

    #show_clusters(cluster_labels, elems, num_clusters, data_and_elems['browser'], "https://adevarul.ro/locale/cluj-napoca/a-fost-prins-suporterul-universitatii-cluj-era-ucida-jandarm-lovindu-l-scaun-cap-acuzatii-i-aduc-1_5cff4a93892c0bb0c63d4544/index.html")

    show_clusters(cluster_labels, elems, num_clusters, data_and_elems['browser'], "http://www.cs.ubbcluj.ro/en/")


def find_best_clustering():
    feature = FeatureBlockLevel("http://www.cs.ubbcluj.ro/en/")

    #feature = CSSFeatureBlockLevel('http://www.cs.ubbcluj.ro/en/')
    data_and_elems = feature.fetchHtmlForThePage()
    data = data_and_elems['data']
    elems = data_and_elems['blocks']
    from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler

    min_max_scaler = MinMaxScaler()
    # feed in a numpy array
    import pdb
    pdb.set_trace()
    X_train_norm = min_max_scaler.fit_transform(np.array(data))
    X = np.array(X_train_norm)
    silhouette_list = []
    for n_clusters in range(2, 6):
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        silhouette_list.append(silhouette_avg)
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)

    number_of_clusters = silhouette_list.index(max(silhouette_list)) + 2

    print(number_of_clusters)
    compute_and_show_results(number_of_clusters, data_and_elems)
    data_and_elems['browser'].quit()


def x_means_compute():
    from pyclustering.cluster.xmeans import xmeans

    from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
    feature = FeatureBlockLevel("http://www.cs.ubbcluj.ro/en/")
    data_and_elems = feature.fetchHtmlForThePage()
    data = data_and_elems['data']
    elems = data_and_elems['blocks']
    from sklearn.preprocessing import MinMaxScaler
    min_max_scaler = MinMaxScaler()
    # feed in a numpy array
    X_train_norm = min_max_scaler.fit_transform(data)
    X = np.array(X_train_norm)

    amount_initial_centers = 2
    initial_centers = kmeans_plusplus_initializer(X, amount_initial_centers).initialize()

    xmeans_instance = xmeans(X, initial_centers, 10)
    xmeans_instance.process()
    # Extract clustering results: clusters and their centers
    clusters = xmeans_instance.get_clusters()
    centers = xmeans_instance.get_centers()

    clusters_minus_L = []
    for elem in clusters:
        if isinstance(elem, list):
            aux = []
            for el in elem:
                aux.append(int(el))
        clusters_minus_L.append(aux)


    for elem in clusters_minus_L:
        print("\n \n \n new Cluster")
        for el in elem:
            print(elems[el].text)
    data_and_elems['browser'].quit()

    import pdb
    pdb.set_trace()


find_best_clustering()
#x_means_compute()
import pdb
pdb.set_trace()
