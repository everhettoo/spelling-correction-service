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
        corpus_name = config.get('Corpus-Med', 'name')
        corpus_medical_dir = config.get('Corpus-Med', 'medical_dir')
        corpus_medical_name = config.get('Corpus-Med', 'medical_name')
        corpus_medical_freq_dir = config.get('Corpus-Med', 'medical_freq_dir')
        corpus_medical_freq_name = config.get('Corpus-Med', 'medical_freq_name')
        noisy_channel_edit_file = config.get('Noisy-Channel', 'edit_file')
        noisy_channel_word_file = config.get('Noisy-Channel', 'word_file')

        # Return a dictionary with the retrieved values
        self.config_values = {
            'app_name': app_name,
            'app_data': app_data,
            'corpus_name': corpus_name,
            'corpus_medical_dir': corpus_medical_dir,
            'corpus_medical_name': corpus_medical_name,
            'corpus_medical_freq_dir': corpus_medical_freq_dir,
            'corpus_medical_freq_name': corpus_medical_freq_name,
            'noisy_channel_edit_file': noisy_channel_edit_file,
            'noisy_channel_word_file': noisy_channel_word_file
        }
