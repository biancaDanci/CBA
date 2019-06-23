from Bind.Service import Service
class Test_results:
    def __init__(self):
        self.f1score = []
        self.keywords = []

    def compute(self, urls):
        for url in urls:
            self.compute_for_url(url)
        print(self.f1score)


    def compute_for_url(self, url):
        service =None
        print(url)
        try:
            service = Service(url=url,
                          algorithm='K-Means',
                          type_of_initialisation='DIMENSION',
                          saving='TEXT',
                          features_type='VISUAL',
                          results_to_show=["FINAL", "INTERMEDIARY"],
                          fixed_number_clusters=4)
            service.cluster()

            precision_recall = service.precision_recall
            pr = precision_recall[0]
            re = precision_recall[1]
            print(pr)
            print(re)
            self.f1score.append(2*float(pr*re)/(pr+re))
            self.keywords.append(service.keywords[1])
            service.data_and_elems['browser'].quit()
        except:
            service.data_and_elems['browser'].quit()
urls =['https://edition.cnn.com/2019/06/20/sport/nba-draft-preview-zion-williamson-spt-intl/index.html',
       'https://www.bbc.com/news/world-europe-48600233',
       'http://www.cs.ubbcluj.ro/en/',
       'https://climate.nasa.gov/news/2882/jakobshavn-glacier-grows-for-third-straight-year/',
       ]


Test_results().compute(urls)
# 3 entertainment
# 4 media
# 5 crime