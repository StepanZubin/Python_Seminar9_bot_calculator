import config
import logger as l
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,  ConversationHandler
from fractions import Fraction   # Модуль fractions предоставляет поддержку рациональных чисел


# Константы этапа разговора:
ENTER_NUMBER_ONE, RATIONAL_ONE, COMPLEX_ONE, ENTER_NUMBER_TWO, RATIONAL_TWO, COMPLEX_TWO, CALCULATIONS = range(7)


# функция обратного вызова точки входа в разговор
def start(update, _):
    update.message.reply_text( 
        '1. Калькулятор для работы с рациональными и комплексными числами.'
        '\n2. Выполняет простые арифметические действия (+, -, *, /)'
        '\n3. Может выполнять действия:' 
        '\n → "рациональное число с комплексным"'
        '\n → "рациональное число с рациональным"'
        '\n → "комплексное число с комплексным"')

    # Список кнопок для ответа
    reply_keyboard = [['рациональное', 'комплексное']]  # если вместо [[ ]] → [ ], будет много кнопок с одним символом внутри: [р] [а] и т.д.

    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор

    update.message.reply_text(
            'КАЛЬКУЛЯТОР (выйти: /cancel)' 
            '\n'
            '\nВыберите тип первого числа:'
            '\nРациональное(a/b) или Комплексное(a+bj)',
        reply_markup=markup_key)
        
    return ENTER_NUMBER_ONE


def enter_number_one(update, _):
    user_choice = update.message.text
    if user_choice == 'рациональное':
        update.message.reply_text('Введите рациональное число (a/b)')
        return RATIONAL_ONE
    elif user_choice == 'комплексное':
        update.message.reply_text('Введите комплексное число (a+bj)')
        return COMPLEX_ONE
    

def rational_one(update, context):
    num_one = update.message.text
    try:
        num_one = Fraction(num_one)
        context.user_data['one_number'] = num_one
        
        reply_keyboard_1 = [['рациональное', 'комплексное']]
        markup_key_1 = ReplyKeyboardMarkup(reply_keyboard_1, one_time_keyboard=True)
        update.message.reply_text(
            'КАЛЬКУЛЯТОР (выйти: /cancel)' 
            '\n'
            '\nВыберите тип второго числа:'
            '\nРациональное(a/b) или Комплексное(a+bj)',
            reply_markup=markup_key_1)
        return ENTER_NUMBER_TWO
    except ValueError:
        update.message.reply_text(
            'некорректный ввод!'
            '\nВведите рациональное число (a/b)')
        return RATIONAL_ONE


def complex_one(update, context):
    num_one = update.message.text
    try:
        num_one = complex(num_one)
        context.user_data['one_number'] = num_one
        
        reply_keyboard_1 = [['рациональное', 'комплексное']]
        markup_key_1 = ReplyKeyboardMarkup(reply_keyboard_1, one_time_keyboard=True)
        update.message.reply_text(
            'КАЛЬКУЛЯТОР (выйти: /cancel)' 
            '\n'
            '\nВыберите тип второго числа:'
            '\nРациональное(a/b) или Комплексное(a+bj) /complex_one/',
            reply_markup=markup_key_1)
        return ENTER_NUMBER_TWO
    except ValueError:
        update.message.reply_text(
            'некорректный ввод!'
            '\nВведите комплексное число (a+bj)')
        return COMPLEX_ONE


def enter_number_two(update, _):
   
    user_choice = update.message.text
    #update.message.reply_text(user_choice)
    if user_choice == 'рациональное':
        update.message.reply_text('Введите второе (рациональное) число (a/b)')
        return RATIONAL_TWO
    elif user_choice == 'комплексное':
        update.message.reply_text('Введите второе (комплексное) число (a+bj)')
        return COMPLEX_TWO
    

def rational_two(update, context):
    num_two = update.message.text
    try:
        num_two = Fraction(num_two)
        context.user_data['two_number'] = num_two

        reply_keyboard_2 = [['+', '-', '*', '/']]
        markup_key_2 = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=True)
        update.message.reply_text(
            'Выберите арифметическую операцию (выйти: /cancel)',
            reply_markup=markup_key_2)
        return CALCULATIONS
    except ValueError:
        update.message.reply_text(
            'некорректный ввод!'
            '\nВведите рациональное число (a/b)')
        return RATIONAL_TWO


def complex_two(update, context):
    num_two = update.message.text
    try:
        num_two = complex(num_two)
        context.user_data['two_number'] = num_two

        reply_keyboard_2 = [['+', '-', '*', '/']]
        markup_key_2 = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=True)
        update.message.reply_text(
            'Выберите арифметическую операцию (выйти: /cancel)',
            reply_markup=markup_key_2)
        return CALCULATIONS
    except ValueError:
        update.message.reply_text(
            'некорректный ввод!'
            '\nВведите комплексное число (a+bj)')
        return COMPLEX_TWO


def calculations(update, context):
    operator = update.message.text

    num_1 = context.user_data.get('one_number')
    num_2 = context.user_data.get('two_number')

    if operator == '+': result = num_1 + num_2
    elif operator == '-': result = num_1 - num_2
    elif operator == '*': result = num_1 * num_2
    elif operator == '/': 
        if num_2 == 0: result = 'на ноль делить нельзя!'
        else: result = num_1 / num_2

    update.message.reply_text(f'{str(num_1)}  {operator}  {str(num_2)} = {str(result)}')

    l.logger(num_1, operator, num_2, result)
    return ConversationHandler.END




# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Вы вышли', 
        reply_markup=ReplyKeyboardRemove()  # убрать клавиатуру
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен бота.
    updater = Updater(config.TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher
    '''
    Определяем обработчик разговоров `ConversationHandler` с состояниями 
    ENTER_NUMBER_ONE, RATIONAL_ONE, COMPLEX_ONE, ENTER_NUMBER_TWO, RATIONAL_TWO, COMPLEX_TWO, CALCULATIONS
    '''
    conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            ENTER_NUMBER_ONE: [MessageHandler(Filters.regex('^(рациональное|комплексное)$'), enter_number_one)],
            RATIONAL_ONE: [MessageHandler(Filters.text, rational_one)],
            COMPLEX_ONE: [MessageHandler(Filters.text, complex_one)],
            ENTER_NUMBER_TWO: [MessageHandler(Filters.all, enter_number_two)],
            RATIONAL_TWO: [MessageHandler(Filters.text, rational_two)],
            COMPLEX_TWO: [MessageHandler(Filters.text, complex_two)],
            CALCULATIONS: [MessageHandler(Filters.text, calculations)],


        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    print('server started')
    updater.start_polling()
    updater.idle()
