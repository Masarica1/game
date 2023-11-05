import csv
import numpy as np

from random import choice

from game import simulation


def read_gene() -> list[list[int]]:
    gene_mat: list[list[int]] = []

    with open('setting/gene.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            list_1 = []
            for i in row:
                list_1.append(int(i))

            gene_mat.append(list_1)

    return gene_mat


def crossover(gene_mat: list, numbers: list[int, int]):
    gene1 = gene_mat[numbers[0]]
    gene2 = gene_mat[numbers[1]]

    gene = []
    for i in range(50000):
        choiced = int(choice([gene1[i], gene2[i]]))

        if choice(range(5)) == 0:
            if choiced == 1:
                choiced = -1
            else:
                choiced = 1

        gene.append(int(choice([gene1[i], gene2[i]])))

    return gene


def get_table() -> list[int]:
    record = simulation()

    print(record)
    for i in range(len(record)):
        record[i] -= int(min(record))

    _p_list: list[int] = []
    for i in range(len(record)):
        for _ in range(record[i]):
            _p_list.append(i)

    return _p_list


gene_matrix = read_gene()
p_list = get_table()

with open('setting/gene.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for _ in range(10):
        writer.writerow(crossover(gene_matrix, [choice(p_list), choice(p_list)]))
