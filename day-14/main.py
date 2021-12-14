MAX_STEPS = 40


class Node(object):

    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node


def read_input() -> (str, list):
    template = None
    rules = []
    with open('data.txt', 'r') as data_file:
        lines = data_file.read().splitlines()
        for line in lines:
            if ' -> ' in line:
                pair, value = line.strip().split(' -> ')
                rules.append((pair, value))
            elif line.strip():
                template = line.strip()
    return template, rules


def print_polymer(head):
    current = head
    print(current.value, end='')
    while current.next_node:
        current = current.next_node
        print(current.value, end='')
    print('')


def apply_rule(previous, current, rule):
    if previous.value == rule[0][0] and current.value == rule[0][1]:
        previous.next_node = Node(rule[1], current)


def apply_rules(head, rules):
    current = head
    while current.next_node:
        previous = current
        current = current.next_node
        for rule in rules:
            apply_rule(previous, current, rule)


def count_elements(head) -> {}:
    element_counts = {}
    current = head
    while current:
        if current.value in element_counts:
            element_counts[current.value] += 1
        else:
            element_counts[current.value] = 1
        current = current.next_node
    return element_counts


def get_solution(head) -> int:
    element_counts = count_elements(head)
    min_element = None
    max_element = None
    for element, count in element_counts.items():
        if not min_element:
            min_element = max_element = element
            continue
        if count < element_counts[min_element]:
            min_element = element
        if count > element_counts[max_element]:
            max_element = element
    return element_counts[max_element] - element_counts[min_element]


def main() -> None:
    head = None
    current = None
    template, rules = read_input()
    for element in list(template):
        if not head:
            head = Node(element)
            current = head
            continue
        previous = current
        current = Node(element)
        previous.next_node = current
    for step in range(MAX_STEPS):
        apply_rules(head, rules)
        if step == 9:
            print('Part 1, most common - least common after 10 steps = {}'.format(get_solution(head)))
    print('Part 2, most common - least common after 40 steps = {}'.format(get_solution(head)))


main()
