board = list(range(1, 10))

win_coords = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]


def draw_board():
    for i in range(3):
        print(board[0 + i * 3], board[1 + i * 3], board[2 + i * 3])


def take_move(player_move):
    while True:
        value = input('Крестик или Нолик?' + player_move)
        if not (value in '123456789'):
            print('вы ввели неверное значение')
            continue
        value = int(value)
        if str(board[value - 1]) in 'XO':
            print('Клетка уже занята')
            continue
        board[value - 1] = player_move
        break


def check_win():
    for each in win_coords:
        if board[each[0] - 1] == board[each[1] - 1] == board[each[2] - 1]:
            return board[each[1] - 1]
    else:
        return False


def main():
    count = 0
    while True:
        draw_board()
        if count % 2 == 0:
            take_move('X')
        else:
            take_move('O')
        count += 1
        if count > 3:
            draw_board()
            winner = check_win()
            if winner:
                print(winner, 'победитель')
                break
        if count > 8:
            draw_board()
            print('Ничья!')
            break


main()
