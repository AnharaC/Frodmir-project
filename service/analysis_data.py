def Punnett_table():
    global male_genotype
    with open("database\gen.txt", "r") as f:
        gen = list(f.read().replace(", ", ","))
        male_genotype = list(gen[0:2])
        female_genotype = list(gen[3:5])
        print(male_genotype, female_genotype)

    children_genotypes = []
    for gene_1 in female_genotype:
        for gene_2 in male_genotype:
            genotype = gene_1 + gene_2
            genotype = "".join(sorted(list(genotype))) # просто для того что бы не были генотыпов таких как "aA" или "BA"
            children_genotypes.append(genotype)
            print("DONE")

    for genotype in set(children_genotypes): # преобразование списка в множество, чтобы случайно не пройтись дважды по одному генотипу
        number_of_apppearences = children_genotypes.count(genotype) # расчет количество появлений конкретного генотипа среди всех возможных
        percentage = number_of_apppearences / len(children_genotypes) # ну и расчет вероятности по формуле количество появлений/общее количество
        print("У нащадків буде генотип {} з імовірністю {:.2f}".format(genotype, percentage))

