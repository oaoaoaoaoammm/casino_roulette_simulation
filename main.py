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
history_size = 4  # Количество последних чисел для анализа

# Хранение последних чисел
history = []

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
    elif bet_type == 'dozen':
        return number in DOZENS[bet_value]
    elif bet_type == 'row':
        return number in ROWS[bet_value]
    return False

# Заранее заданные ставки
bets1 = [
    ('corner', [2, 3, 5, 6]),  # Ставка на угол
    ('corner', [7, 8, 10, 11]),  # Ставка на угол
    ('corner', [14, 15, 17, 18]),  # Ставка на угол
    ('corner', [19, 20, 22, 23]),  # Ставка на угол
    ('corner', [26, 27, 29, 30]),  # Ставка на угол
    ('corner', [31, 32, 34, 35]),  # Ставка на угол
    ('dozen', 1),          # Ставка на дюжину (1-я дюжина)
    ('dozen', 2),  # Ставка на дюжину (2-я дюжина)
    ('row', 1),  # Ставка на 1-й ряд
    ('row', 3)  # Ставка на 3-й ряд
]

bets2 = [
    ('corner', [1, 2, 4, 5]),  # Ставка на угол
    ('corner', [8, 9, 11, 12]),  # Ставка на угол
    ('corner', [13, 14, 16, 17]),  # Ставка на угол
    ('corner', [20, 21, 23, 24]),  # Ставка на угол
    ('corner', [25, 26, 28, 29]),  # Ставка на угол
    ('corner', [32, 33, 35, 36]),  # Ставка на угол
    ('dozen', 1),          # Ставка на дюжину (1-я дюжина)
    ('dozen', 2),  # Ставка на дюжину (2-я дюжина)
    ('row', 1),  # Ставка на 1-й ряд
    ('row', 3)  # Ставка на 3-й ряд
]

# Функция для определения текущих ставок
def get_current_bets():
    if len(history) < history_size:
        return bets1  # Если недостаточно данных, используем первую стратегию
    counts = {bet_type: 0 for bet_type, _ in bets1}
    for number in history:
        for bet_type, bet_value in bets1:
            if evaluate_bet(bet_type, number, bet_value):
                counts[bet_type] += 1
    # Если количество чисел, подходящих под bets2, превышает порог, используем bets2
    if any(count > history_size // 2 for count in counts.values()):
        return bets2
    return bets1

# Основной цикл
# Основной цикл
def simulate_roulette():
    balance = initial_balance
    total_bets = 0
    total_wins = 0
    total_cycles_done = 0

    for _ in range(cycles):
        if balance < bet_amount * len(bets1):
            print("Баланс недостаточен для продолжения игры.")
            break

        number = spin_roulette()
        history.append(number)
        if len(history) > history_size:
            history.pop(0)  # Удаляем старые числа, если их больше history_size

        bets = get_current_bets()
        total_bet = len(bets) * bet_amount
        total_bets += total_bet
        total_win = 0

        for bet_type, bet_value in bets:
            if evaluate_bet(bet_type, number, bet_value):
                if bet_type == 'number':
                    total_win += bet_amount * 35
                elif bet_type == 'split':
                    total_win += bet_amount * 17
                elif bet_type == 'street':
                    total_win += bet_amount * 11
                elif bet_type == 'corner':
                    total_win += bet_amount * 8
                elif bet_type == 'six_line':
                    total_win += bet_amount * 5
                elif bet_type in ['column', 'dozen', 'row']:
                    total_win += bet_amount * 2
                else:
                    total_win += bet_amount
            else:
                total_win -= bet_amount  # Уменьшение баланса при проигрыше

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