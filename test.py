male_genotype = input("Введіть генотип особини чоловічої статі: ").replace(" ", "")
female_genotype = input("Введіть генотип особини жіночої статі: ").replace(" ", "")

# print(male_genotype, female_genotype)
male_genotype = list(male_genotype)
female_genotype = list(female_genotype)

children_genotypes = []
for gene_1 in female_genotype:
    for gene_2 in male_genotype:
        genotype = gene_1 + gene_2
        genotype = "".join(sorted(list(genotype)))
        children_genotypes.append(genotype)

line = "_" * 70
print(line)
print("|{:^6}|{:^30}|{:^30}|".format(r" \  ♂ ", "", ""))
print("|{:^6}|{:^30}|{:^30}|".format(r"  \   ", male_genotype[0], male_genotype[1]))
print("|{:^6}|{:^30}|{:^30}|".format(r" ♀ \  ", "", ""))
print(line)
print("|{:^6}|{:^30}|{:^30}|".format("", "", ""))
print("|{:^6}|{:^30}|{:^30}|".format(female_genotype[0], children_genotypes[0], children_genotypes[1]))
print("|{:^6}|{:^30}|{:^30}|".format("", "", ""))
print(line)
print("|{:^6}|{:^30}|{:^30}|".format("", "", ""))
print("|{:^6}|{:^30}|{:^30}|".format(female_genotype[1], children_genotypes[2], children_genotypes[3]))
print("|{:^6}|{:^30}|{:^30}|".format("", "", ""))
print(line)

print()
for genotype in set(children_genotypes):
    number_of_apppearences = children_genotypes.count(genotype)
    percentage = number_of_apppearences / len(children_genotypes)
    print("У нащадків буде генотип {} з імовірністю {:.2f}".format(genotype, percentage))