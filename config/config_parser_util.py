import configparser


class ConfigParserUtil(object):
    @staticmethod
    def get_config_parser(config_file):
        config_parser = configparser.RawConfigParser()
        config_parser.read(config_file)
        return config_parser
