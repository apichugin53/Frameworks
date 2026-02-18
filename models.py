import csv


class CsvReader:
    """Класс для чтения данных из CSV-файлов"""

    def __init__(self, filename):
        """
        Конструктор класса.

        :param filename: Имя файла CSV
        """
        self.filename = filename

    def read_data(self):
        """
        Метод для чтения данных из CSV-файла.

        :return: Список словарей, представляющих каждую строку CSV
        """
        try:
            with open(self.filename, newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print(f'Файл {self.filename} не найден.')
            return []