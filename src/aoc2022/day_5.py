from typing import NamedTuple

import toolz
from parse import parse

from aoc_common import get_file_content


class Instruction(NamedTuple):
    from_stack: int
    to_stack: int
    n_crates: int

    @classmethod
    def parse(cls, instruction: str) -> "Instruction":
        fmt = "move {n_crates:d} from {from_stack:d} to {to_stack:d}"
        parsed = parse(fmt, instruction)
        return cls(**parsed.named)


Stacks = dict[int, list]


def parse_stacks_and_instructions() -> tuple[Stacks, list[Instruction]]:
    raw = get_file_content(2022, 5)
    stacks, instructions = raw.split("\n\n")
    instructions = list(map(Instruction.parse, instructions.split("\n")))
    stack_contents, stack_names_str = stacks.rsplit("\n", 1)
    stack_names = list(map(int, stack_names_str.split()))
    stack_strpos = list(map(stack_names_str.find, map(str, stack_names)))
    stack_contents = list(reversed(stack_contents.split("\n")))
    stacks = {
        stack_name: [
            row[strpos]
            for row in stack_contents
            if len(row) > strpos and row[strpos] != " "
        ]
        for stack_name, strpos in zip(stack_names, stack_strpos)
    }
    return stacks, instructions


def apply_instruction(
    instruction: Instruction, stacks: Stacks, bulk_move: bool
) -> Stacks:
    assert len(stacks[instruction.from_stack]) >= instruction.n_crates
    moved_crates = stacks[instruction.from_stack][-instruction.n_crates :]
    if not bulk_move:
        moved_crates = reversed(moved_crates)
    return toolz.merge(
        stacks,
        {
            instruction.from_stack: stacks[instruction.from_stack][
                : -instruction.n_crates
            ],
            instruction.to_stack: [*stacks[instruction.to_stack], *moved_crates],
        },
    )


def apply_instructions(
    instructions: list[Instruction], stacks: Stacks, bulk_move: bool
) -> Stacks:
    for instruction in instructions:
        stacks = apply_instruction(instruction, stacks, bulk_move)
    return stacks


def apply_and_check_top_crates(bulk_move: bool) -> str:
    stacks, instructions = parse_stacks_and_instructions()
    stacks = apply_instructions(instructions, stacks, bulk_move)
    return "".join(toolz.pluck(-1, stacks.values()))


if __name__ == "__main__":
    print(apply_and_check_top_crates(False))
    print(apply_and_check_top_crates(True))
