from aiogram import types

from service.survey_manager import save_survey

async def Punnett_table(callback: types.CallbackQuery, genotypes):

    male_genotype = [gene.strip() for gene in genotypes[1].strip('[]').split(',') if gene.strip()]
    female_genotype = [gene.strip() for gene in genotypes[2].strip('[]').split(',') if gene.strip()]
    
    if male_genotype != None and female_genotype != None:
        children_genotypes = set()
        for gene_1 in female_genotype:
            for gene_2 in male_genotype:
                genotype = gene_1 + gene_2
                genotype = "".join(sorted(list(genotype))) # просто для того что бы не были генотыпов таких как "aA" или "BA"
                children_genotypes.add(genotype)
        children_genotypes = list(children_genotypes)

        genotype_data = {}
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


