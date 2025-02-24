import configparser


def __read_config():
    pass


class Configuration:
    def __init__(self):
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read('config.ini')

        # App
        app_name = config.get('App', 'name')
        app_data = config.get('App', 'data')

        # Corpus
        corpus_name = config.get('Corpus', 'name')

        # Return a dictionary with the retrieved values
        self.config_values = {
            'app_name': app_name,
            'app_data': app_data,
            'corpus_name': corpus_name,
        }
