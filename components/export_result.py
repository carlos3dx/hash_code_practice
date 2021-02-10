from typing import List


def write_result(file_path: str, result: List[List[int]]) -> None:
    with open(file_path, 'w') as file:
        num_orders = len(result)
        file.write(f'{num_orders}\n')
        for line in result:
            file.write(' '.join(map(str, line)))
            file.write('\n')
