import utils


def get_calories_by_elf():
    calories_list = utils.get_input(__file__, delimiter='\n', line_delimiter='\n\n')
    return [sum(calories) for calories in calories_list]


@utils.part
def part_1():
    calories = get_calories_by_elf()
    print(max(calories))


@utils.part
def part_2():
    calories = get_calories_by_elf()
    top_3 = sorted(calories, reverse=True)[:3]
    print(sum(top_3))
