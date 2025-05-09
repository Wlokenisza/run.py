import json


def check_capacity(max_capacity: int, guests: list) -> bool:
    # Реализация алгоритма
    def compare(elem1: list[int, int, int, int], elem2: list[int, int, int, int]) -> bool:
        year1 = elem1[0]
        year2 = elem2[0]
        mounth1 = elem1[1]
        mounth2 = elem2[1]
        day1 = elem1[2]
        day2 = elem2[2]
        in_out1 = elem1[3]
        in_out2 = elem2[3]
        if year1 > year2:
            return True
        elif year1 == year2 and mounth1 > mounth2:
            return True
        elif year1 == year2 and mounth1 == mounth2 and day1 > day2:
            return True
        elif year1 == year2 and mounth1 == mounth2 and day1 == day2 and in_out1 == in_out2:
            return True
        else:
            return False

    def insert_with_sorted(sorted_list: list[list[int, int, int, int]], add_elem: list[int, int, int, int]) -> None:
        left, right = 0, len(sorted_list)
        center = None
        while left < right:
            center = (left + right) // 2
            if compare(sorted_list[center], add_elem):
                right = center - 1
            else:
                left = center + 1
        if right == 0:
            sorted_list.insert(0, add_elem)
        else:
            sorted_list.insert(right + 1, add_elem)

    def data_transformation(data: list) -> list[list[int, int, int, int]]:
        result = []
        for elem in data:
            data_in = list(map(int, elem["check-in"].split("-")))
            data_in.append(1)
            data_out = list(map(int, elem["check-out"].split("-")))
            data_out.append(-1)
            insert_with_sorted(result, data_in)
            insert_with_sorted(result, data_out)
        return result

    def find_max_counts_guests(sorted_data_in_out: list[list[int, int, int, int]]) -> int:
        current_count = 0
        max_count = 0
        for elem in sorted_data_in_out:
            current_count += elem[3]
            max_count = max(max_count, current_count)
        return max_count

    return max_capacity >= find_max_counts_guests(data_transformation(guests))


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())

    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)

    result = check_capacity(max_capacity, guests)
    print(result)
