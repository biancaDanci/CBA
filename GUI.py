from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from Validator import Validator
from Bind.Service import Service

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
        return [spinner_algorithm.text, spinner_initialisation.text]

    def get_url(self):
        url = self.ids.url
        Validator.validate_url(url.text)
        return url

    def show_pop_up(self):
        service = None
        try:
            #url = self.get_url()
            #display = self.bind_checkboxes()
            #options = self.get_spinners()
            #print(options[0])
            #print(options[1])
            #print(display)
            options = ['K-Means', 'HEURISTIC']
            display = ['']
            service = Service(url='http://www.cs.ubbcluj.ro/en/', algorithm=options[0], type_of_initialisation=options[1], saving=display)
            service.cluster()

            precision_recall = service.precision_recall
            self.ids.precision_recall.text = " Precision: " + str(precision_recall[0]) + \
                                             "\n Recall: " + str(precision_recall[1])
            service.data_and_elems['browser'].quit()
            print("Gata de tooooot")
            service = None
        except Exception as err:
            service.data_and_elems['browser'].quit()
            popup = Popup(title='Error',
                          content=Label(text=str(err)+'\nTo exit press outside the box', font_size=18),
                          size_hint=(None, None), size=(400, 400))
            popup.open()


class MenuApp(App):

    def build(self):
        return MenuWindow()


MenuApp().run()
