import sys

import collections


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def solve(data) -> int:
    width_data = len(data)
    length_data = len(data[0])
    state_bfs = collections.deque()
    # Состояния - кортеж из 7-и составляющих: 
    # 1-4) 4 пары координат - текущие позиции роботов,
    # 5) Какой из роботов совершил шаг (значения 0 до 3 соответсвующее номеру робота и -1, если не ходил)
    # 6) Число в двоичной записи, где соотвествующий i-й бит содержит информацию о наличие i-го ключа (1 - ключ есть, 0 - ключан нет)
    # 7) Количество шагов внутри лабиринта.

    # Находим начальные позиции роботов и подсчёт количества ключей
    start_state = tuple()
    count_key = 0
    for i in range(width_data):
        for j in range(length_data):
            if data[i][j] == "@":
                start_state = start_state + ((i,j),)
            elif data[i][j] in keys_char:
                count_key += 1
    start_state = start_state + (0, 0, 0)

    state_bfs.append(start_state)
    # Состояния (интересует именно позиция всех роботов и найденые на этот момент ключи) в которых мы уже были не интересуют
    visited_state = set()
    
    while state_bfs:
        size = len(state_bfs)
        for _ in range(size):
            cur_state = state_bfs.popleft()
            # print(cur_state)
            i, j = cur_state[cur_state[5]]
            key_found, steps = cur_state[4], cur_state[6]
            
            cur_pos = data[i][j]
            # print(cur_pos)
            # Если текущая позиция стена или дверь, ключей от которой у нас нет, то в эту позицию мы не могли попасть
            if cur_pos in doors_char and not ((key_found >> (ord(cur_pos) - ord('A'))) & 1):
                continue
            # Если текущая позиция ключ, то учитываем это
            if cur_pos in keys_char:
                key_found |= 1 << (ord(cur_pos) - ord('a'))
                # Если при этом нашли все ключи - возращаем количество шагов
                # print(key_found)
                if key_found == (1 << count_key) - 1:
                    return steps

            for id_robot in range(4):
                i, j = cur_state[id_robot]
                for x, y in [(i+1, j),(i, j+1),(i-1, j),(i, j-1)]:
                    visit_state = tuple()
                    for k in range(4):
                        if k == id_robot:
                            visit_state = visit_state + ((x, y),)
                        else:
                            visit_state = visit_state + (cur_state[k],)
                    visit_state = visit_state + (key_found, )
                    if 0 <= min(x, y) and x < width_data and y < length_data and data[x][y] != "#" and visit_state not in visited_state:
                        visited_state.add(visit_state)
                        new_state_bfs = visit_state + (id_robot, steps + 1)
                        state_bfs.append(new_state_bfs)

    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()