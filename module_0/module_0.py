import numpy as np


def game_core_v2(number):
    '''В моем решении использован алгоритм бинарного поиска. Он заключается в нахождении среднего значения для
    уменьшения поиска значения.'''
    count = 1
    predict = np.random.randint(1, 101)
    lower_bound = 1
    upper_bound = 100

    while number != predict:
        count += 1
        current = (lower_bound + upper_bound) // 2
        predict = current

        if number > current:
            lower_bound = current + 1

        elif number < current:
            upper_bound = current - 1

        else:
            current = number

    return count


def score_game(game_core):
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!

    random_array = np.random.randint(1, 101, size=(100))
    for number in random_array:
        count_ls.append(game_core(number))

    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")


    return (score)


score_game(game_core_v2)



