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

    "compare_button": {
        Languages.EN: "Compare",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },

    "error_required_cols": {
        Languages.EN: "Please fill out all values in columns 'Cost per Month', 'Deducible' and 'Excess'",
        Languages.FR: "",
        Languages.IT: "",
        Languages.DE: "",
    },
}


_current_language = Languages.EN


def get_text(string):
    print(_current_language.name)
    return _TRANSLATIONS[string][_current_language]


def get_lang():
    return _current_language


def set_lang(language):
    global _current_language

    if language not in Languages:
        raise ValueError(f"Programming error: unrecognized value for language selected: {language}")

    print("setting to", language.name)
    _current_language = language


# Simple validation translations were done correctly.
def _check_translations():
    for _, translations in _TRANSLATIONS.items():
        for language in Languages:
            if language not in translations or translations[language].strip() == "":
                raise RuntimeError(f"Missing translations were detected.")
#_check_translations()