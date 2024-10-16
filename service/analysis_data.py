import json

def Punnett_table():
    with open("database/temp_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        genotypes = data["gen"]
        male_genotype, female_genotype = genotypes.split(", ")
    if male_genotype != None and female_genotype != None:
        children_genotypes = []
        for gene_1 in female_genotype:
            for gene_2 in male_genotype:
                genotype = gene_1 + gene_2
                genotype = "".join(sorted(list(genotype))) # просто для того что бы не были генотыпов таких как "aA" или "BA"
                children_genotypes.append(genotype)

        for genotype in set(children_genotypes): # преобразование списка в множество, чтобы случайно не пройтись дважды по одному генотипу
            number_of_apppearences = children_genotypes.count(genotype) # расчет количество появлений конкретного генотипа среди всех возможных
            percentage = number_of_apppearences / len(children_genotypes) # ну и расчет вероятности по формуле количество появлений/общее количество
    return male_genotype, children_genotypes, percentage, female_genotype
