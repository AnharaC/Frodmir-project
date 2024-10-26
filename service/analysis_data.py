from aiogram import types

async def Punnett_table(callback: types.CallbackQuery, genotypes):

    male_genotype, female_genotype = genotypes
    
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

        await callback.message.answer(
            text=f"Чоловічий генотип: {male_genotype}; \n"
                 f"Жіночий генотип: {female_genotype}; \n"
                 f"Дитячі генотипи: {children_genotypes}; \n"
                 f"Відсотки: {percentage}"
        )

    return male_genotype, children_genotypes, percentage, female_genotype


