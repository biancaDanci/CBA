import validators


class Validator:

    @staticmethod
    def validate_url(url):
        if not validators.url(url):

            raise Exception("Not a valid URL")

    @staticmethod
    def validate_algorithm(algorithm):
        if algorithm == 'Algorithm':
            raise Exception("You must specify the algorithm")

    @staticmethod
    def validate_initialisation(initialisation):
        if initialisation == "Initialisation":
            raise Exception("You must specify the initialisation")

    @staticmethod
    def validate_display(display):
        if len(display) <= 0:
            raise Exception("You must select the type of initialisation")

    @staticmethod
    def validate_heuristic(initialization, heuristic):
        if initialization != 'RANDOM' and heuristic == 'Choose heuristics':
            raise Exception("Heuristic mode was requested but an heuristic was not provided")

    @staticmethod
    def validate_features(features):
        if features == 'Type of features':
            raise Exception("Type of features not specified ")
