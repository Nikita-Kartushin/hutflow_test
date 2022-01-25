import pandas


class ExcelUtils:
    def __init__(self, path: str, config: dict):
        self._path = self._check_path(path)
        self._config = config

    def read_candidates(self, n_row: int, count: int = None):
        """
        Чтение из .xlsx файла данных о кандидатах

        Фунция является генератором, сделано это для того, чтобы не нагружать
            оперативную память

        :param count: количество прочитанных строк за одну итерацию
        :param n_row: номер строки, с которой начать чтение
        :return:
        """
        _start = True
        data_frame_of_recruits = None

        while _start or len(data_frame_of_recruits) > 0:
            _start = False
            data_frame_of_recruits = pandas.read_excel(self._path, nrows=count, skiprows=n_row)
            yield data_frame_of_recruits
            n_row += count if count else None

    def get_vacancies(self):
        """

        :return:
        """
        pass

    @staticmethod
    def _check_path(path):
        """
        Метод проверяет доступ к файлу

        :param path:
        :return:
        """

        return path

    @staticmethod
    def _check_config(config):
        """
        Метод проверяет валидность таблицы в соответствии со схемой config

        :param config:
        :return:
        """

        return config
