import json
from datetime import datetime


class Operation:
    def __init__(self, id_transaction, date_of, state, amount, currency, description, where_from,
                 where_to, currency_code):
        self.id = id_transaction  # id транзакции
        self.date = date_of  # информация о дате совершения операции
        self.state = state  # статус перевода:`EXECUTED` — выполнена, `CANCELED`  — отменена.
        self.operationAmount = amount  # сумма операции
        self.currency = currency  # валюта операции
        self.currency_code = currency_code
        self.description = description  # описание типа перевода
        self.where_from = where_from  # откуда(может отсутствовать)
        self.where_to = where_to  # куда

    def __repr__(self):
        return "Operation"

    def date_formating(self, date):
        """
        Преобразует дату в заданный формат ("2019-08-26T10:50:58.294041" -> 26-08-2019)
        """
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d-%m-%Y')

    def where_from_mask(self, where_from):
        """
        Маскирует поля класса ("Maestro 1596837868705199" -> Maestro 1596** **** 5199)
        """
        if where_from:
            if "Счет" in where_from:
                return "Счет **" + where_from[-4:]
            else:
                return where_from[:-12] + "** **** " + where_from[-4:]
        return self.currency_code

    def where_to_mask(self, where_to):
        """
        Маскирует поле класса ("Maestro 1596837868705199" -> Maestro 1596** **** 5199)
        """
        if "Счет" in where_to:
            return "Cчет **" + where_to[-4:]
        else:
            return where_to[:-12] + "** **** " + where_to[-4:]

    def information_print(self):
        """
        Собирает данные для вывода в заданном формате
        """
        return (f'{self.date_formating(self.date)} {self.description}'
                f'\n{self.where_from_mask(self.where_from)} '
                f'-> {self.where_to_mask(self.where_to)}'
                f'\n{self.operationAmount} {self.currency}')


def creating_class_instance(data):
    """
    Создает список экземпляров класса Operation
    """
    list_transactions = []
    for items in data:
        if items.get("from", ""):
            id_transaction = items["id"]
            date = items["date"]
            state = items["state"]
            amount = items["operationAmount"]["amount"]
            currency = items["operationAmount"]["currency"]["name"]
            currency_code = items["operationAmount"]["currency"]["code"]
            description = items["description"]
            where_from = items["from"]
            where_to = items["to"]
            transaction = Operation(id_transaction, date, state, amount, currency,
                                    description, where_from, where_to, currency_code)
            list_transactions.append(transaction)
        else:
            if items != {}:  # учитываем пустую запись и если отсутствует "from"
                id_transaction = items["id"]
                date = items["date"]
                state = items["state"]
                amount = items["operationAmount"]["amount"]
                currency = items["operationAmount"]["currency"]["name"]
                currency_code = items["operationAmount"]["currency"]["code"]
                description = items["description"]
                where_from = ""
                where_to = items["to"]
                transaction = Operation(id_transaction, date, state, amount, currency,
                                        description, where_from, where_to, currency_code)
                list_transactions.append(transaction)
    return list_transactions


def reading_information(file_name):
    """
    Записывает обработанные данные в переменную
    """
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def select_state_executed(data):
    """Функция принимает список и по определенным параметрам и значениям возвращает список"""
    new_data = []
    for items in data:
        if items.state == "EXECUTED":
            new_data.append(items)
    return new_data
