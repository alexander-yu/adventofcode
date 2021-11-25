import collections

import click

import utils


class Queue:
    def __init__(self, capacity):
        self.items = collections.deque([])
        self.capacity = capacity
        self.counts = collections.defaultdict(int)

    def enqueue(self, x):
        if len(self.items) == self.capacity:
            item = self.items.popleft()
            self.counts[item] -= 1

            if not self.counts[item]:
                self.counts.pop(item)

        self.items.append(x)
        self.counts[x] += 1

    def __iter__(self):
        for item in self.items:
            yield item

    def __contains__(self, x):
        return x in self.counts and self.counts[x] > 0


def get_subarray_sum(arr, target_sum):
    start = 0
    current_sum = arr[0]

    for end in range(1, len(arr)):
        current_sum += arr[end]

        while current_sum > target_sum and start < end:
            current_sum -= arr[start]
            start += 1

        if current_sum == target_sum:
            return arr[start:end + 1]

    raise ValueError(f'Could not find contiguous subarray that sums to {target_sum}')


@click.group()
def cli():
    pass


@cli.command()
@utils.part(__name__, 1)
def part_1():
    numbers = utils.get_input(__file__, delimiter=None)
    queue = Queue(25)
    for i, number in enumerate(numbers):
        if i >= 25:
            is_valid = any(number - x in queue for x in queue)
            if not is_valid:
                print(number)
                return

        queue.enqueue(number)


@cli.command()
@utils.part(__name__, 2)
def part_2():
    numbers = utils.get_input(__file__, delimiter=None)
    subarray = get_subarray_sum(numbers, 104054607)
    print(min(subarray) + max(subarray))


if __name__ == '__main__':
    cli()
