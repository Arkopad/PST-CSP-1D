from itertools import groupby

lst = [10, 10, 10, 20, 20, 20, 20, 30]

for key, group in groupby(lst):
    print(f'Item: {key}, Count: {len(list(group))}')
