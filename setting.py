import random
import csv


def location_setting():
    with open('setting/enemy_loc.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(10000):
            loc = random.choice(range(0, 1280))
            writer.writerow([loc])


def gene_setting(number: int):
    with open('setting/gene.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        for _ in range(number):
            row = []
            for _ in range(50000):
                row.append(random.choice([1, -1]))
            writer.writerow(row)


location_setting()
gene_setting(1)
