from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from Validator import Validator
from Bind.Service import Service
import logging


class MenuWindow(BoxLayout):

    def get_checkboxes(self):
        text_checkbox = self.ids.text_checkbox
        browser_checkbox = self.ids.browser_checkbox
        photo_checkbox = self.ids.photo_checkbox
        keyword_checkbox = self.ids.keyword_checkbox
        return [text_checkbox, browser_checkbox, photo_checkbox, keyword_checkbox]

    def bind_checkboxes(self):
        to_display = []
        for checkbox in self.get_checkboxes():
            if checkbox.active:
                to_display.append(checkbox.text)
        Validator.validate_display(to_display)
        return to_display

    def get_spinners(self):
        spinner_algorithm = self.ids.algorithm
        Validator.validate_algorithm(spinner_algorithm.text)
        spinner_initialisation = self.ids.initialisation
        Validator.validate_initialisation(spinner_initialisation.text)
        spinner_heuristics = self.ids.heuristic
        Validator.validate_heuristic(spinner_initialisation.text, spinner_heuristics.text)
        if spinner_initialisation.text == 'RANDOM':
            text_heuristic = 'RANDOM'
        else:
            text_heuristic = spinner_heuristics.text
        spinner_features = self.ids.features
        Validator.validate_features(spinner_features.text)
        return [spinner_algorithm.text, text_heuristic, spinner_features.text]

    def get_url(self):
        url = self.ids.url
        Validator.validate_url(url.text)
        return url

    def get_fixed_values(self):
        nr_clusters = self.ids.nr_clusters
        if nr_clusters.text in ['The algorithm will find it', 'Number of clusters - Optional']:
            return None
        return int(nr_clusters.text)

    def show_pop_up(self):
        service = None
        try:
            url = self.get_url()
            display = self.bind_checkboxes()
            options = self.get_spinners()
            print(options[0])
            print(options[1])
            print(display)

            number_clusters = self.get_fixed_values()
            #options = ['K-Means', 'TEXT DENSITY']
            #display = ['TEXT', 'PHOTO']
            #https://www.bbc.com/news/world-europe-48600233
            # 'http://www.cs.ubbcluj.ro/en/'
            service = Service(url=url.text,
                              #'https://www.boldsky.com/health/wellness/2019/yoga-poses-to-lose-weight-128727.html?ref=60sec',
                              algorithm=options[0],
                              type_of_initialisation=options[1],
                              saving=display,
                              features_type=options[2],
                              results_to_show=["FINAL", "INTERMEDIARY"],
                              fixed_number_clusters=number_clusters)
            service.cluster()

            precision_recall = service.precision_recall
            self.ids.precision_recall.text = " Precision: " + str(precision_recall[0]) + \
                                             "\n Recall: " + str(precision_recall[1])
            service.data_and_elems['browser'].quit()
            #f = open(path, 'a')
            #f.write("Precision: {}; Recall: {} \n".format(precision_recall[0], precision_recall[1]))
            logging.info("The computing has finished.")
            #f.close()
            popup = Popup(title='Success',
                          content=Label(text='The computing has finished. You can now see your \n'
                                             '  results or start analysing a different url. \n'
                                             'A new computing will override the photos and text files.'
                                             '\n \n \n \n To exit press outside the box', font_size=18),
                          background_color=[0, 0, 128, 0.8],
                          size_hint=(None, None), size=(500, 500),
                          )
            popup.open()
            service = None
        except Exception as err:
            if service:
                service.data_and_elems['browser'].quit()
            popup = Popup(title='Error',
                          background_color=[255,0,0,1],
                          content=Label(text=str(err)+'\nTo exit press outside the box', font_size=18),
                          size_hint=(None, None), size=(500, 500))
            popup.open()


class MenuApp(App):

    def build(self):
        return MenuWindow()


