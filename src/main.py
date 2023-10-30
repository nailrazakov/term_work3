from classes import (reading_information, creating_class_instance,
                     select_state_executed)
# создаем список для хранения экземпляров класса
operations = []
# считываем файл
list_of_transactions = reading_information("../operations.json")
# записываем экземпляры класса, если элемент не пустой
for items in list_of_transactions:
    if items != {}:
        operation = creating_class_instance(items)
        operations.append(operation)
# Производим выборку данных по нужным параметрам
list_selected = select_state_executed(operations)
# сортируем по дате
sorted_from_date = sorted(list_selected, key=lambda x: x.date, reverse=True)
# Выводим пять последних операций
for i in range(0, 5):
    print(f"{sorted_from_date[i].information_print()}\n")
