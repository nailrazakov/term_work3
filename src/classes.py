import json
from datetime import datetime


class Operation:
    def __init__(self, id_transaction=None, date_of=None, state=None, amount=None, currency=None,
                 description=None, where_from=None, where_to=None, currency_code=None):
        self.id = id_transaction  # id транзакции
        self.date = date_of  # информация о дате совершения операции
        self.state = state  # статус перевода:`EXECUTED` — выполнена, `CANCELED`  — отменена.
        self.operation_amount = amount  # сумма операции
        self.currency = currency  # валюта операции
        self.currency_code = currency_code
        self.description = description  # описание типа перевода
        self.where_from = where_from  # откуда(может отсутствовать)
        self.where_to = where_to  # куда

    def __repr__(self):
        return f"Operation {self.description} {self.operation_amount}"

    def date_formating(self, date):
        """
        Преобразует дату в заданный формат ("2019-08-26T10:50:58.294041" -> 26-08-2019)
        """
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d-%m-%Y')

    def masking_information(self, value):
        """
        Маскирует поле класса ("Maestro 1596837868705199" -> Maestro 1596** **** 5199)
        """
        if value:
            if "Счет" in value:
                return "Счет **" + value[-4:]
            else:
                return value[:-12] + "** **** " + value[-4:]
        return self.currency_code

    def information_print(self):
        """
        Собирает данные для вывода в заданном формате
        """
        return (f'{self.date_formating(self.date)} {self.description}'
                f'\n{self.masking_information(self.where_from)} '
                f'-> {self.masking_information(self.where_to)}'
                f'\n{self.operation_amount} {self.currency}')


def reading_information(file_name):
    """
    Записывает обработанные данные в переменную
    """
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def select_state_executed(data):
    """Функция принимает список и возвращает новый если поле класса "state" - "EXECUTED" """
    new_data = []
    for items in data:
        if items.state == "EXECUTED":
            new_data.append(items)
    return new_data


def creating_class_instance(items: dict) -> object:
    """
    Создает экземпляр класса Operation
    """
    id_transaction = items["id"]
    date = items["date"]
    state = items["state"]
    amount = items["operationAmount"]["amount"]
    currency = items["operationAmount"]["currency"]["name"]
    currency_code = items["operationAmount"]["currency"]["code"]
    description = items["description"]
    where_from = items.get("from")
    where_to = items["to"]
    class_instance = Operation(id_transaction, date, state, amount, currency,
                               description, where_from, where_to, currency_code)
    return class_instance
