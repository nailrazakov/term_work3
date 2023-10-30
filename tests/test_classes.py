from src.classes import (Operation, select_state_executed, reading_information,
                         creating_class_instance)

""""создаём необходимые для тестирования экземпляры класса Operation"""
class_instance = Operation()
operation_info = Operation("12345", "2023-10-30T16:43:26.929246",
                           "EXECUTED", "100", "Рублей",
                           "ПЕРЕВОД", "MAESTRO 1234 1234 1234 1234",
                           "SkyPro 1234 1234 1234 1234", "RUB")
operation_1 = Operation(id_transaction="1", state="EXECUTED")
operation_2 = Operation(id_transaction="2", state="CANCELED")
operation_3 = Operation(id_transaction="3", state="EXECUTED")
operation_4 = Operation(id_transaction="4", state="CANCELED")
operation_5 = Operation(id_transaction="5", state="EXECUTED")
test_data_class = [operation_1, operation_2, operation_3, operation_4, operation_5]


def test_date_formating():
    """"
    Тест для метода формата даты класса Operation
    """
    assert (class_instance.date_formating("2019-08-26T10:50:58.294041") ==
            '26-08-2019')


def test_masking_information():
    assert (class_instance.masking_information("Maestro 1596837868705199") ==
            "Maestro 1596** **** 5199")
    assert class_instance.masking_information("") == class_instance.currency_code


def test_information_print():
    assert operation_info.information_print() == ('30-10-2023 ПЕРЕВОД\n'
                                                  'MAESTRO 1234 12** **** 1234 -> SkyPro 1234 12** **** 1234\n'
                                                  '100 Рублей')


def test_reading_information():
    assert len(reading_information("../operations.json")) > 0


def test_select_state_executed():
    assert len(select_state_executed(test_data_class)) == 3


def test_creating_class_instance(test_data):
    assert (str(creating_class_instance(test_data[0])) ==
            'Operation Перевод организации 31957.58')
