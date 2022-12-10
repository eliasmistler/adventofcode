import toolz

from aoc_common import get_file_content_lazy


def run_instructions() -> tuple[list[int], list[str]]:
    x = 1
    t = 0
    signal_observations = []
    screen = ''

    def cycle():
        nonlocal screen
        if t % 40 == 20:
            signal_observations.append(x * t)
        screen += '#' if (t - 1) % 40 in {x - 1, x, x + 1} else '.'

    for command in get_file_content_lazy(2022, 10):
        t += 1
        cycle()
        if command == 'noop':
            pass
        else:
            instruction, arg = command.split(' ')
            assert instruction == 'addx'
            t += 1
            cycle()
            x += int(arg)

    screen = list(map(''.join, toolz.partition_all(40, screen)))
    return signal_observations, screen


if __name__ == "__main__":
    observations, screen = run_instructions()
    print(sum(observations))
    print('\n'.join(screen))
