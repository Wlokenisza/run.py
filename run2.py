import sys

import collections


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input() -> list[list[str]]:
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]

# Избавляемся от не нужных путей и тупиков
def maze_processing(data: list[list[str]]) -> None: # type: ignore
    
    # Проверка того, что текущая позиция - тупик
    # Тупик - позиция в которой со всех сторон стены, кроме одной.
    # При этом можно забыть про двери ("#") и путь (".")

    def is_deadlock(data, x, y) -> bool: # type: ignore
        result = ((data[x][y] == "." or data[x][y] in doors_char) and (
                    (data[x+1][y] == "#" and data[x-1][y] == "#" and data[x][y-1] == "#") or
                    (data[x+1][y] == "#" and data[x-1][y] == "#" and data[x][y+1] == "#") or
                    (data[x][y+1] == "#" and data[x-1][y] == "#" and data[x][y-1] == "#") or
                    (data[x+1][y] == "#" and data[x][y-1] == "#" and data[x][y+1] == "#")
            )
        )
        return result

    # Проходим весь лабиринт и убираем пути приводящие к тупикам.

    length_data = len(data[0])
    width_data = len(data)
    for y in range(1, length_data-1):
        for x in range(1, width_data-1):
            if is_deadlock(data, x, y):
                next_x, next_y = x, y
                while is_deadlock(data, next_x, next_y):
                    data[next_x][next_y] = "#"
                    if data[next_x+1][next_y] != "#":
                        next_x += 1
                    elif data[next_x-1][next_y] != "#":
                        next_x -= 1
                    elif data[next_x][next_y-1] != "#":
                        next_y -= 1
                    elif data[next_x][next_y+1] != "#":
                        next_y += 1

# Оставим только информацию о расстояних между вершинами в виде словаря:
# ключ - вершина, значение в ключе - словарь (ключ - вершина до которой можно дойти, значение - расстояние до неё)
# Также вводим нумерацию для роботов заменой четырёх "@" на "@0", "@1", "@2", "@3".
def graph_paths(data):  # type: ignore
    width_data = len(data)
    length_data = len(data[0])
    vertex = tuple()
    id_robot = 0
    for i in range(width_data):
        for j in range(length_data):
            if data[i][j] == "@" or data[i][j] in keys_char or data[i][j] in doors_char:
                if data[i][j] == "@": 
                    data[i][j] = "@" + str(id_robot)
                    id_robot += 1
                vertex = vertex + ((data[i][j], i, j),)
    result = dict()
    for name, x, y in vertex:
        paths_from_vertex = dict()
        visited = set()
        step = 0
        bfs = collections.deque()
        bfs.append((x, y))
        while bfs:
            step += 1
            size = len(bfs)
            for _ in range(size):
                coordinate = bfs.popleft()
                if coordinate in visited:
                    continue
                else:
                    cur_x, cur_y = coordinate
                    visited.add(coordinate)
                    for i, j in [(cur_x+1, cur_y), (cur_x-1, cur_y), (cur_x, cur_y+1), (cur_x, cur_y-1)]:
                        if data[i][j] == "#" or data[i][j] == name:
                            continue
                        elif data[i][j][0] == "@" or data[i][j] in keys_char or data[i][j] in doors_char:
                            paths_from_vertex[data[i][j]] = step
                        else:
                            bfs.append((i, j))
        result[name] = paths_from_vertex
    return result


def solve(data) -> int:  # type: ignore
    maze_processing(data)
    dict_paths = graph_paths(data)
    state_bfs = collections.deque()

    # Состояния - кортеж из 7-и составляющих: 
    # 1-4) 4 вершины - текущие позиции роботов в графе
    # 5) Какой из роботов совершил перемещение (значения 0 до 3 соответсвующее номеру робота и -1, если не ходил)
    # 6) Число в двоичной записи, где соотвествующий i-й бит содержит информацию о наличие i-го ключа (1 - ключ есть, 0 - ключан нет)
    # 7) Количество шагов внутри лабиринта.

    # Инициация начальных позиции роботов и подсчёт количества ключей
    start_state = tuple()
    count_key = 0
    for key in dict_paths:
        if key in keys_char:
            count_key += 1
        elif key[0] == "@":
            start_state = start_state + (key,)
    start_state = start_state + (0, 0, 0)
    # print(start_state)

    state_bfs.append(start_state)
    # Состояния (интересует именно позиция всех роботов и найденые на этот момент ключи) 
    # в которых мы уже были не интересуют
    all_visit_state = set()
    all_visit_state_distance = dict()
    min_steps = float('inf')

    while state_bfs:
        size = len(state_bfs)
        for _ in range(size):
            cur_state = state_bfs.popleft()
            last_visited_vertex = cur_state[cur_state[5]]
            key_found, steps = cur_state[4], cur_state[6]
            if last_visited_vertex in doors_char and not ((key_found >> (ord(last_visited_vertex) - ord('A'))) & 1):
                continue
            # Если текущая позиция ключ, то учитываем это
            if last_visited_vertex in keys_char:
                key_found |= 1 << (ord(last_visited_vertex) - ord('a'))
                # Если при этом нашли все ключи - возращаем количество шагов
                if key_found == (1 << count_key) - 1 and min_steps > steps:
                    if min_steps > steps:
                        min_steps = steps
                    continue

            # BFS. Добавляем все возможные состояния в которые можем попасть из текущего состояния
            for id_robot in range(4):
                cur_vertex = cur_state[id_robot]
                for next_vertex, next_steps in dict_paths[cur_vertex].items():
                    visit_state = tuple()
                    for k in range(4):
                        if k == id_robot:
                            visit_state = visit_state + (next_vertex,)
                        else:
                            visit_state = visit_state + (cur_state[k],)
                    visit_state = visit_state + (key_found,)
                    
                    # Добавляем, если такого состояние не было, или обновляем, если в состояние есть вариант с меньшим числом шагов.
                    if (visit_state in all_visit_state and all_visit_state_distance[visit_state] > steps + next_steps) or (visit_state not in all_visit_state):
                        all_visit_state.add(visit_state)
                        all_visit_state_distance[visit_state] = steps + next_steps
                        new_state_bfs = visit_state + (id_robot, steps + next_steps)
                        state_bfs.append(new_state_bfs)

    if min_steps == float('inf'):
        return -1
    else:
        return min_steps


def main() -> None:
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()
