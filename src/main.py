from classes import reading_information, creating_class_instance, select_state_executed
# считываем файл
list_of_transactions = reading_information("../operations.json")
# записываем экземпляры класса
operation = creating_class_instance(list_of_transactions)
# Производим выборку данных по нужным параметрам
list_selected = select_state_executed(operation)
# сортируем по дате
sorted_from_date = sorted(list_selected, key=lambda x: x.date, reverse=True)
# Выводим пять последних операций
for i in range(0, 5):
    print(f"{sorted_from_date[i].information_print()}\n")
