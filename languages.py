from enum import IntEnum


Languages = IntEnum("Languages", ["EN", "FR", "IT", "DE"])


_TRANSLATIONS = {
    "choose_language": {
        Languages.EN: "Choose the site's language 🌐",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "title": {
        Languages.EN: "Insurance Comparator",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "decription": {
        Languages.EN: """I built this tool to help you decide which base health insurance is the most appropriate
                         for you in the year to come. If you provide me the deducible and monthly payout of any
                         insurance, I can run a simple simulation and tell you how much you would need to spend
                         in medical expenses next year for the more expensive insurance to actually be worth it.
                         Give it a try 😃.""",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "label": {
        Languages.EN: "Label",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "cost_per_month": {
        Languages.EN: "Cost per Month",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "deducible": {
        Languages.EN: "Deducible",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "excess": {
        Languages.EN: "Excess",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "insurance_parameters": {
        Languages.EN: "Insurance Parameters",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "add_row_button": {
        Languages.EN: "Add a row",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "comparison": {
        Languages.EN: "Comparison of the Offers",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "error_duplicate_labels": {
        Languages.EN: "Some of your options have the same label: {}. Please change that before starting the comparison.",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "error_required_cols": {
        Languages.EN: "Please fill out all values in columns 'Cost per Month', 'Deducible' and 'Excess'.",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "colname_spend_per_year": {
        Languages.EN: "If you spend, in CHF per year",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "health_expenses_range_any": {
        Languages.EN: "Any amount",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "health_expenses_range_less": {
        Languages.EN: "Less than {}",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "health_expenses_range_between": {
        Languages.EN: "Between {} and {}",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "health_expenses_range_over": {
        Languages.EN: "Over {}",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "colname_1st_cheapest": {
        Languages.EN: "Cheapest",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "colname_2nd_cheapest": {
        Languages.EN: "2nd Cheapest",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "colname_3rd_cheapest": {
        Languages.EN: "3rd Cheapest",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "comparison_table_explaination": {
        Languages.EN: """The table below shows which are the cheapest offers for each range of yearly medical
                         expenses. If you have an idea of how much you spend each year, you can finally now find
                         out which one is your best option to save money.""",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "comparison_plot_explaination": {
        Languages.EN: """This plot shows you how each offer compares at any amount of yearly medical expenses.
                         The plot is interactive, try it out!""",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "health_expenses_plot": {
        Languages.EN: "Medical Expenses, in CHF per year",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "money_to_insurance_plot": {
        Languages.EN: "Money to Pay Insurance, in CHF per year",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "labels_plot": {
        Languages.EN: "Legend",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "hover_title": {
        Languages.EN: "<b>If medical expenses are %{x} CHF per year,<br>you will pay to the health insurance:</b>",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "hover_template": {
        Languages.EN: "%{customdata}: %{y} CHF per year<extra></extra>",
        Languages.FR: "",
        Languages.IT: "",
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