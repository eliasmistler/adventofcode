import operator
from collections import deque
from dataclasses import dataclass
from typing import Callable, Optional

import toolz
from parse import parse

from aoc_common import get_file_content


@dataclass
class Monkey:
    id: int
    items: deque[int]
    # note: operator and operator_arg could also simply be a `py_expression.Exp`
    #       which I originally had here, but when exploring solutions for pt.2
    #       I refactored this thinking I might need the inverse of the operator
    operator: Callable[[int, int], int]
    operator_arg: Optional[int]  # if None, use old value instead
    test_div: int
    true_monkey: 'Monkey'
    false_monkey: 'Monkey'
    n_inspected: int = 0

    def inspect(self, item: int) -> int:
        self.n_inspected += 1
        return self.operator(item, self.operator_arg if self.operator_arg is not None else item)

    def take_turn(self, alt_relief: int = None):
        while self.items:
            # get and inspect item
            old_worry = self.items.popleft()
            new_worry = self.inspect(old_worry)

            # relief
            if alt_relief is None:
                # default (pt. 1)
                new_worry //= 3
            else:
                # alternative relief (common multiple of all monkeys)
                new_worry %= alt_relief

            # test and throw
            receiver = (
                self.true_monkey
                if new_worry % self.test_div == 0
                else self.false_monkey
            )
            receiver.items.append(new_worry)


INPUT_FORMAT = """
Monkey {id:d}:
  Starting items: {items}
  Operation: new = old {operator} {arg}
  Test: divisible by {test_div:d}
    If true: throw to monkey {true_monkey:d}
    If false: throw to monkey {false_monkey:d}
""".strip()


def parse_monkeys():
    raw = get_file_content(2022, 11)
    monkeys = raw.split('\n\n')
    operators = {'+': operator.add, '*': operator.mul}

    def parse_monkey(m: str) -> Monkey:
        parsed = parse(INPUT_FORMAT, m).named
        return Monkey(
            id=parsed['id'],
            items=deque(map(int, parsed['items'].split(','))),
            operator=operators[parsed['operator']],
            operator_arg=None if parsed['arg'] == 'old' else int(parsed['arg']),
            test_div=parsed['test_div'],
            true_monkey=parsed['true_monkey'],
            false_monkey=parsed['false_monkey'],
        )

    monkeys_by_id = {
        monkey.id: monkey
        for monkey in map(parse_monkey, monkeys)
    }

    # create links post-hoc
    for monkey in monkeys_by_id.values():
        monkey.true_monkey = monkeys_by_id[monkey.true_monkey]
        monkey.false_monkey = monkeys_by_id[monkey.false_monkey]

    return monkeys_by_id


def play(monkeys: dict[int, Monkey], rounds: int, use_alt_relief: bool) -> None:
    # alternative relief (pt.2):
    # all monkeys test for the rest of an integer division, so we can simply work on the
    # rest of those integer divisions. However, to make sure we get the same output no
    # matter which monkey the item is thrown to, we need to use a common multiple of all
    # possible division values.
    # The division values all seem to be prime, so we do not need any prime factorisation.
    # We can simply multiply all (distinct) values of `test_div` to give us the
    # least common multiple.
    alt_relief = (
        toolz.reduce(operator.mul, {monkey.test_div for monkey in monkeys.values()})
        if use_alt_relief
        else None
    )

    for _ in range(rounds):
        for monkey in monkeys.values():
            monkey.take_turn(alt_relief)


def calculate_monkey_business(monkeys: dict[int, Monkey]) -> int:
    top2 = sorted((monkey.n_inspected for monkey in monkeys.values()), reverse=True)[:2]
    return toolz.reduce(operator.mul, top2)


if __name__ == "__main__":
    monkeys = parse_monkeys()
    play(monkeys, 20, False)
    print(calculate_monkey_business(monkeys))

    monkeys = parse_monkeys()
    play(monkeys, 10000, True)
    print(calculate_monkey_business(monkeys))
