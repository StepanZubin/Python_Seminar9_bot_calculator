from datetime import datetime as dt

def logger(num_1, operator, num_2, result):
    '''
    Метод: Записывает дату, время, проводимую операцию в файл logger.csv
    Аргументы: Данные введённые пользователем и результат операции
    '''
    time = dt.now().strftime('date: %d.%m.%Y     time: %H:%M:%S')
    with open('logger.csv', 'a', encoding = 'UTF-8') as file:
        file.write(f'{time}     action: {num_1} {operator} {num_2} = {result}\n')
        