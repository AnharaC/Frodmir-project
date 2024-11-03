from aiogram import types
from service.survey_manager import save_survey


async def Punnett_table(callback: types.CallbackQuery, genotypes):

    male_genotype = [
        gene.strip() for gene in genotypes[1].strip("[]").split(",") if gene.strip()
    ]
    female_genotype = [
        gene.strip() for gene in genotypes[2].strip("[]").split(",") if gene.strip()
    ]

    if male_genotype and female_genotype:
        children_genotypes = set()
        for gene_1 in female_genotype:
            for gene_2 in male_genotype:
                genotype = gene_1 + gene_2
                genotype = "".join(sorted(list(genotype)))
                children_genotypes.add(genotype)
        children_genotypes = list(children_genotypes)

        genotype_data = {}
        for genotype in set(children_genotypes):
            number_of_appearances = children_genotypes.count(genotype)
            percentage = (number_of_appearances / len(children_genotypes)) * 100

            genotype_data[genotype] = {
                "count": number_of_appearances,
                "percentage": round(percentage, 2),
            }

        table_header = (
            f"{'🧬 Генотип':^12} | {'🔢 Кількість':^14} | {'📊 Процент (%)':^15}\n"
        )
        table_separator = "-" * 45 + "\n"
        table_rows = ""

        for genotype, data in genotype_data.items():
            table_rows += (
                f"{genotype:^12} | {data['count']:^14} | {data['percentage']:>14}\n"
            )

        await callback.message.answer(
            text=(
                f"💼 Чоловічий генотип: {male_genotype};\n"
                f"👩‍🔬 Жіночий генотип: {female_genotype};\n\n"
                f"🧑‍👧 Дитячі генотипи:\n"
                f"{table_header}{table_separator}{table_rows}"
            )
        )

    return male_genotype, female_genotype
