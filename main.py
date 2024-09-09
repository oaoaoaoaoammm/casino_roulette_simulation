import random

# Константы для рулетки
NUMBERS = list(range(37))  # Числа от 0 до 36
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
RED_NUMBERS = set(NUMBERS) - BLACK_NUMBERS - {0}
ROWS = {1: list(range(1, 37, 3)), 2: list(range(2, 37, 3)), 3: list(range(3, 37, 3))}  # Горизонтальные ряды
DOZENS = {1: list(range(1, 13)), 2: list(range(13, 25)), 3: list(range(25, 37))}  # Дюжины

# Начальные параметры
initial_balance = 100  # начальный баланс игрока
bet_amount = 1  # ставка на одно поле
cycles = 10000000  # количество циклов

# Функция для запуска одной игры рулетки
def spin_roulette():
    return random.choice(NUMBERS)

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
        return number in bet_value
    elif bet_type == 'six_line':
        return number in bet_value
    elif bet_type == 'column':
        return number in ROWS[bet_value]
    elif bet_type == 'dozen':
        return number in DOZENS[bet_value]
    elif bet_type == 'row':
        return number in ROWS[bet_value]
    return False

# Заранее заданные ставки
bets = [
    ('corner', [2, 3, 5, 6]),  # Ставка на угол
    ('corner', [7, 8, 10, 11]),  # Ставка на угол
    ('corner', [14, 15, 17, 18]),  # Ставка на угол
    ('corner', [19, 20, 22, 23]),  # Ставка на угол
    ('corner', [26, 27, 29, 30]),  # Ставка на угол
    ('corner', [31, 32, 34, 35]),  # Ставка на угол
    ('dozen', 1),          # Ставка на дюжину (1-я дюжина)
    ('dozen', 3),  # Ставка на дюжину (3-я дюжина)
    ('column', 1),  # Ставка на 1-й ряд (вертикальная колонка)
    ('column', 2)  # Ставка на 2-й ряд (вертикальная колонка)
]

# Основной цикл
def simulate_roulette():
    balance = initial_balance
    total_bets = 0
    total_wins = 0
    total_cycles_done = 0

    for _ in range(cycles):
        if balance < bet_amount * len(bets):
            print("Баланс недостаточен для продолжения игры.")
            break

        number = spin_roulette()
        total_bet = len(bets) * bet_amount
        total_bets += total_bet
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

        balance += total_win
        total_wins += total_win

        print(f'Выпало число: {number}')
        print(f'Сумма ставок: {total_bet}')
        print(f'Выигрыш: {total_win}')
        print(f'Баланс: {balance}')
        total_cycles_done += 1

    return balance, total_wins, total_cycles_done

# Запуск симуляции
final_balance, total_wins, tot_cycles = simulate_roulette()
print(f'Финальный баланс: {final_balance}')
print(f'Общая сумма выигрышей: {total_wins}')
print(f'Общее количество игр: {tot_cycles}')