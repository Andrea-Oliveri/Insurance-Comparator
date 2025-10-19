from enum import IntEnum


Languages = IntEnum("Languages", ["EN", "FR", "IT", "DE"])


_TRANSLATIONS = {
    "choose_language": {
        Languages.EN: "Choose the site's language 🌐",
        Languages.FR: "Choisis la langue du site 🌐",
        Languages.IT: "Scegli la lingua del sito 🌐",
        Languages.DE: "",
    },

    "title": {
        Languages.EN: "LAMal Comparator",
        Languages.FR: "Comparateur LAMal",
        Languages.IT: "Comparatore LAMal",
        Languages.DE: "",
    },

    "decription": {
        Languages.EN: """I built this tool to help you decide which base health insurance is the most appropriate
                         for you in the year to come. If you provide me the deducible and monthly payout of any
                         LAMal insurance, I can run a simple simulation and tell you how much you would need to spend
                         in medical expenses next year for the more expensive insurance to actually be worth it.
                         Give it a try 😃.""",
        Languages.FR: """J'ai construit cet outil pour vous aider à décider quelle assurance de base est la plus
                         appropriée dans l'année à venir. Si vous connaissez la franchise et prix mensuel
                         de toute assurance LAMal, je peux tourner une simple simulation et vous dire à partir de combien
                         d'argent dépensé en medecins l'assurance plus chère vaudra la peine. Essayez-voir 😃.""",
        Languages.IT: """Ho creato questo strumento per aiutarla a decidere quale assicurazione di base é la più
                         appropriata nell'anno a venire. Se conosce la franchigia e il prezzo mensile di qualsiasi
                         assicurazione LAMal, posso fare una semplice simulazione per dirle a partire da quante spese
                         mediche l'assicurazione più cara varrà la pena. Provi a vedere 😃.""",
        Languages.DE: "",
    },

    "label": {
        Languages.EN: "Label of offer",
        Languages.FR: "Nom de l'offre",
        Languages.IT: "Nome dell'offerta",
        Languages.DE: "",
    },

    "cost_per_month": {
        Languages.EN: "Cost per month",
        Languages.FR: "Coût par mois",
        Languages.IT: "Costo al mese",
        Languages.DE: "",
    },

    "deducible": {
        Languages.EN: "Deducible",
        Languages.FR: "Franchise",
        Languages.IT: "Franchigia",
        Languages.DE: "",
    },

    "excess": {
        Languages.EN: "Excess (at 10%)",
        Languages.FR: "Quote-part (à 10%)",
        Languages.IT: "Aliquota (al 10%)",
        Languages.DE: "",
    },

    "insurance_parameters": {
        Languages.EN: "Insurance Parameters",
        Languages.FR: "Paramètres Assurances",
        Languages.IT: "Parametri Assicurazioni",
        Languages.DE: "",
    },

    "add_row_button": {
        Languages.EN: "Add a row",
        Languages.FR: "Ajouter une ligne",
        Languages.IT: "Aggiungere una linea",
        Languages.DE: "",
    },

    "comparison": {
        Languages.EN: "Comparison of the Offers",
        Languages.FR: "Comparaison des Offres",
        Languages.IT: "Confronto delle Offerte",
        Languages.DE: "",
    },

    "error_duplicate_labels": {
        Languages.EN: "Some of your options have the same label: {}. Please ensure they are unique before starting the comparison.",
        Languages.FR: "Certaines de vos options ont le même nom: {}. S'il-vous-plait assurez-vous qu'elles soient unique avant de démarrer la comparaison.",
        Languages.IT: "Alcune delle sue optioni hanno lo stesso nome: {}. Per piacere si assicuri che siano unici prima di iniziare il confronto.",
        Languages.DE: "",
    },

    "error_required_cols": {
        Languages.EN: "Please fill out all values in columns 'Cost per month', 'Deducible' and 'Excess (at 10%)'.",
        Languages.FR: "S'il-vous-plaît remplissez toutes les valeurs dans les colonnes 'Coût par mois', 'Franchise' et 'Quote-part (à 10%)'",
        Languages.IT: "Per piacere riempia tutti i valori nelle colonne 'Costo al mese', 'Franchigia' e 'Aliquota (al 10%)'.",
        Languages.DE: "",
    },

    "colname_spend_per_year": {
        Languages.EN: "If you spend, in CHF per year",
        Languages.FR: "Si vous dépensez, en CHF par année",
        Languages.IT: "Se lei spende, in CHF per anno",
        Languages.DE: "",
    },

    "health_expenses_range_any": {
        Languages.EN: "Any amount",
        Languages.FR: "Tout montant",
        Languages.IT: "Qualunque montante",
        Languages.DE: "",
    },

    "health_expenses_range_less": {
        Languages.EN: "Less than {}",
        Languages.FR: "Moins que {}",
        Languages.IT: "Meno di {}",
        Languages.DE: "",
    },

    "health_expenses_range_between": {
        Languages.EN: "Between {} and {}",
        Languages.FR: "Entre {} et {}",
        Languages.IT: "Tra {} e {}",
        Languages.DE: "",
    },

    "health_expenses_range_over": {
        Languages.EN: "Over {}",
        Languages.FR: "Plus que {}",
        Languages.IT: "Più di {}",
        Languages.DE: "",
    },

    "colname_1st_cheapest": {
        Languages.EN: "Cheapest",
        Languages.FR: "Moins Chère",
        Languages.IT: "Meno Cara",
        Languages.DE: "",
    },

    "colname_2nd_cheapest": {
        Languages.EN: "2nd Cheapest",
        Languages.FR: "2ème Moins Chère",
        Languages.IT: "2ª Meno Cara",
        Languages.DE: "",
    },

    "colname_3rd_cheapest": {
        Languages.EN: "3rd Cheapest",
        Languages.FR: "3ème Moins Chère",
        Languages.IT: "3ª Meno Cara",
        Languages.DE: "",
    },

    "comparison_table_explaination": {
        Languages.EN: """The table below shows which are the cheapest offers for each range of yearly medical
                         expenses. If you have an idea of how much you spend next year, you can finally now find
                         out which one is your best option to save money.""",
        Languages.FR: """La table ci-dessous montre quelles sont les offres moins chères pour chaque interval de
                         dépenses médicales annuelles. Si vous avez une idée de combien vous allez dépenser
                         l'année prochaine année, vous pouvez finalement savoir quelle est la meilleure option
                         pour sauver de l'argent.""",
        Languages.IT: """La tabella qui sotto mostra quali sono le offerte meno care per ciascun intervallo di
                         spese mediche annuali. Se ha un'idea di quanto spenderà l'anno prossimo, può finalmente
                         sapere qual'é la sua opzione migliore per risparmiare.""",
        Languages.DE: "",
    },

    "comparison_plot_explaination": {
        Languages.EN: """This plot shows you how each offer compares at any amount of yearly medical expenses.
                         The plot is interactive, try it out!""",
        Languages.FR: """Ce graphique vous montre comment chaque offre se place par rapport aux autres pour toute
                         valeur des dépenses médicales annuelles. Le graphique est interactif, esseyez-le!""",
        Languages.IT: """Questo grafico le mostra come ciascuna offerta si posiziona rispetto alle altre per
                         qualunque valore delle spese mediche annuali. Il grafico é interattivo, lo provi!""",
        Languages.DE: "",
    },

    "health_expenses_plot": {
        Languages.EN: "Medical Expenses, in CHF per year",
        Languages.FR: "Dépenses Médicales, en CHF par année",
        Languages.IT: "Spese Mediche, in CHF per anno",
        Languages.DE: "",
    },

    "money_to_insurance_plot": {
        Languages.EN: "Money to Pay Insurance, in CHF per year",
        Languages.FR: "Argent à Payer à l'Assurance, en CHF par an",
        Languages.IT: "Soldi da Pagare all'Assicurazione, in CHF per anno",
        Languages.DE: "",
    },

    "labels_plot": {
        Languages.EN: "Legend",
        Languages.FR: "Légende",
        Languages.IT: "Legenda",
        Languages.DE: "",
    },

    "hover_title": {
        Languages.EN: "<b>If medical expenses are %{x} CHF per year,<br>you will pay to the health insurance:</b>",
        Languages.FR: "<b>Si les dépenses médicales sont %{x} CHF par année,<br>vous allez payer à l'assureur:</b>",
        Languages.IT: "<b>Se le spese mediche sono %{x} CHF per anno,<br>lei pagherà all'assicurazione:</b>",
        Languages.DE: "",
    },

    "hover_template": {
        Languages.EN: "%{customdata}: %{y} CHF per year<extra></extra>",
        Languages.FR: "%{customdata}: %{y} CHF par année<extra></extra>",
        Languages.IT: "%{customdata}: %{y} CHF per anno<extra></extra>",
        Languages.DE: "",
    },
}


_current_language = Languages.EN


def get_text(string):
    return _TRANSLATIONS[string][_current_language]


def get_lang():
    return _current_language


def set_lang(language):
    global _current_language

    if language not in Languages:
        raise ValueError(f"Programming error: unrecognized value for language selected: {language}")

    _current_language = language


# Simple validation translations were done correctly.
def _check_translations():
    for _, translations in _TRANSLATIONS.items():
        for language in Languages:
            if language not in translations or translations[language].strip() == "":
                raise RuntimeError(f"Programming error: missing translations were detected.")
#_check_translations()