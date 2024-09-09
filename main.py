import random

# Константы для рулетки
NUMBERS = list(range(37))  # Числа от 0 до 36
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
RED_NUMBERS = set(NUMBERS) - BLACK_NUMBERS - {0}
ROWS = {1: list(range(1, 37, 3)), 2: list(range(2, 37, 3)), 3: list(range(3, 37, 3))}  # Горизонтальные ряды
DOZENS = {1: list(range(1, 13)), 2: list(range(13, 25)), 3: list(range(25, 37))}  # Дюжины

# Начальные параметры
initial_balance = 20  # начальный баланс игрока
bet_amount = 1  # ставка на одно поле
cycles = 100  # количество циклов

# Функция для запуска одной игры рулетки
def spin_roulette():
    num = random.choice(NUMBERS)
    print(f'Выпало число: {num}')
    return num

# Функция для расчета выигрыша/проигрыша по одной ставке
def evaluate_bet(bet_type, number, bet_value=None):
    if bet_type == 'red':
        return number in RED_NUMBERS
    elif bet_type == 'black':
        return number in BLACK_NUMBERS
    elif bet_type == 'even':
        return number != 0 and number % 2 == 0
    elif bet_type == 'odd':
        return number != 0 and number % 2 != 0
    elif bet_type == 'low':
        return 1 <= number <= 18
    elif bet_type == 'high':
        return 19 <= number <= 36
    elif bet_type == 'number':
        return number == bet_value
    elif bet_type == 'split':
        return number in bet_value
    elif bet_type == 'street':
        return number in bet_value
    elif bet_type == 'corner':  # Ставка на угол
        return any(number in corner for corner in bet_value)
    elif bet_type == 'six_line':
        return number in bet_value
    elif bet_type == 'column':
        return number in [n for row in ROWS.values() if row in bet_value for n in row]
    elif bet_type == 'dozen':
        return number in [n for d in bet_value for n in DOZENS[d]]
    elif bet_type == 'row':
        return number in ROWS[bet_value]
    return False

# Заранее заданные ставки
bets = [
    ('corner', [[2, 3, 5, 6], [7, 8, 10, 11], [14, 15, 17, 18], [19, 20, 22, 23], [26, 27, 29, 30], [31, 31, 34, 35]]),  # Ставка на угол
    ('dozen', [1, 3]),          # Ставка на дюжину (1-я дюжина)
    ('column', [1, 2])          # Ставка на 2-й ряд (вертикальная колонка)
]

# Основной цикл
def simulate_roulette():
    balance = initial_balance
    for _ in range(cycles):
        number = spin_roulette()
        total_win = 0

        for bet_type, bet_value in bets:
            if evaluate_bet(bet_type, number, bet_value):
                if bet_type == 'number':
                    total_win += bet_amount * 35  # выигрыш для числа с множителем 35
                elif bet_type == 'split':
                    total_win += bet_amount * 17  # выигрыш для сплита с множителем 17
                elif bet_type == 'street':
                    total_win += bet_amount * 11  # выигрыш для улицы с множителем 11
                elif bet_type == 'corner':
                    total_win += bet_amount * 8  # выигрыш для угла с множителем 8
                elif bet_type == 'six_line':
                    total_win += bet_amount * 5  # выигрыш для линии с множителем 5
                elif bet_type in ['column', 'dozen', 'row']:
                    total_win += bet_amount * 2  # выигрыш для ряда/дюжины/колонки с множителем 2
                else:
                    total_win += bet_amount  # выигрыш для простых ставок (красное/черное, чет/нечет и т.д.)
            else:
                total_win -= bet_amount  # проигрыш по данной ставке

        print(f'Выигрыш: {total_win}')
        balance += total_win
        print(f'баланс: {balance}')

    return balance

# Запуск симуляции
print(evaluate_bet('red', 5))    # True
print(evaluate_bet('black', 2))  # True
print(evaluate_bet('even', 6))   # True
print(evaluate_bet('odd', 7))    # True
print(evaluate_bet('low', 10))   # True
print(evaluate_bet('high', 20))  # True
print(evaluate_bet('number', 13, 13))  # True
print(evaluate_bet('number', 13, 15))  # False
print(evaluate_bet('column', 2, [1, 2]))  # True
print(evaluate_bet('dozen', 14, [1, 2]))  # True
print(evaluate_bet('corner', 5, [[2, 3, 5, 6]]))  # True
final_balance = simulate_roulette()
print(f'Финальный баланс после {cycles} циклов: {final_balance}')