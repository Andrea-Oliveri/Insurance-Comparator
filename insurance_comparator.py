from itertools import combinations

import streamlit as st
import pandas as pd
import plotly.express as px

import languages



MAX_CHOICES = 50



def _set_page_config(title, icon):
    st.set_page_config(page_title = title, page_icon = icon)

    st.markdown(
        """
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            .block-container {
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }
            #MainMenu {visibility: hidden;}
            .stAppDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
        """,
        unsafe_allow_html = True)


def _choose_language():
    # On first run, try infering from locale. The format is fr-FR, fr-CH, ...
    if not st.session_state.get("language_inferred_from_locale", False):
        locale_language, _ = st.context.locale.split('-')
        locale_mapping = {"en": languages.Languages.EN,
                          "fr": languages.Languages.FR,
                          "it": languages.Languages.IT,
                          "de": languages.Languages.DE}
        language = locale_mapping.get(locale_language, languages.Languages.EN)
        languages.set_lang(language)
        st.session_state["language_inferred_from_locale"] = True

    previous_language = languages.get_lang()

    language_options = {languages.Languages.EN: "🇺🇸 English",
                        languages.Languages.FR: "🇫🇷 Français",
                        languages.Languages.IT: "🇮🇹 Italiano",
                        languages.Languages.DE: "🇩🇪 Deutsch"}

    language = st.sidebar.selectbox(
        label       = languages.get_text("choose_language"),
        options     = language_options.keys(),
        index       = list(language_options.keys()).index(previous_language),
        format_func = language_options.get
    )

    languages.set_lang(language)

    if language != previous_language:
        st.rerun()



def _get_example_dataframe():
    return pd.DataFrame([
        {"label": f"Option 1", "cost_per_month": 500, "deducible": 300 , "excess": 700},
        {"label": f"Option 2", "cost_per_month": 400, "deducible": 2500, "excess": 700}
    ])


def _check_insurance_params(df):
    if df[["cost_per_month", "deducible", "excess"]].isna().any(axis = None):
        st.error(languages.get_text("error_required_cols"), icon = "🚨")
        return False
    return True



def _make_df_lines(df):
    df_lines = []
    for _, row in df.iterrows():
        cost_per_year = 12 * row["cost_per_month"]
        df_lines.append({'label': row['label'], 'health_expenses': 0                                        , 'money_to_insurance': cost_per_year})
        df_lines.append({'label': row['label'], 'health_expenses': 0 + row["deducible"]                     , 'money_to_insurance': cost_per_year + row["deducible"]})
        df_lines.append({'label': row['label'], 'health_expenses': 0 + row["deducible"] + row["excess"] * 10, 'money_to_insurance': cost_per_year + row["deducible"] + row["excess"]})
        df_lines.append({'label': row['label'], 'health_expenses': float("inf")                             , 'money_to_insurance': cost_per_year + row["deducible"] + row["excess"]})
    return pd.DataFrame(df_lines)


def _make_intersections(df_lines):
    x = "health_expenses"
    y = "money_to_insurance"

    df_lines_new = []
    for label, rows in df_lines.sort_values(x).groupby("label"):
        for idx in range(len(rows) - 1):
            start_point = rows.iloc[idx]
            end_point   = rows.iloc[idx + 1]
            slope       = (end_point[y] - start_point[y]) / (end_point[x] - start_point[x])
            intercept   = start_point[y] - slope * start_point[x]
            df_lines_new.append({"label": label, "slope": slope, "intercept": intercept, "x_min": start_point[x], "x_max": end_point[x]})
    df_lines = pd.DataFrame(df_lines_new)
    del df_lines_new, label, rows, idx, start_point, end_point, slope, intercept

    intersections = []
    for label1, label2 in combinations(df_lines["label"].unique(), 2):
        for _, line1 in df_lines[df_lines["label"] == label1].iterrows():
            for _, line2 in df_lines[df_lines["label"] == label2].iterrows():
                if line1["slope"] == line2["slope"]:
                    continue # In this scenario, we don't care for perfectly overlapping lines
                x_inter = (line2["intercept"] - line1["intercept"]) / (line1["slope"] - line2["slope"])
                if x_inter < line1["x_min"] or x_inter < line2["x_min"] or x_inter > line1["x_max"] or x_inter > line2["x_max"]:
                    continue
                intersections.append(x_inter)
    return intersections





if __name__ == "__main__":
    _choose_language()

    _set_page_config(languages.get_text("title"), "💸")

    st.title(languages.get_text("title"))
    st.write(languages.get_text("decription"))

    st.session_state["choices"] = st.session_state.get("choices", _get_example_dataframe())
    st.session_state["button_pressed"] = st.session_state.get("button_pressed", False)

    st.write("### " + languages.get_text("insurance_parameters"))
    st.session_state["choices"] = st.data_editor(
        st.session_state["choices"],
        hide_index = True,
        num_rows   = "dynamic" if len(st.session_state["choices"]) < MAX_CHOICES else "fixed",
        disabled   = False,
        on_change  = lambda: st.session_state.__setitem__("button_pressed", False)
    )

    if st.button(languages.get_text("compare_button")+ " 🚀"):
        st.session_state["button_pressed"] = _check_insurance_params(st.session_state["choices"])
        for idx in range(len(st.session_state["choices"])):
            if pd.isna(st.session_state["choices"].iloc[idx].loc["label"]):
                st.session_state["choices"].iloc[idx].loc["label"] = f"Option {idx + 1}"
        st.rerun()

    if st.session_state["button_pressed"]:
        df_lines = _make_df_lines(st.session_state["choices"])
        intersections = _make_intersections(df_lines)

        fig = px.line(df_lines, x = "health_expenses", y = "money_to_insurance", color = "label")
        for x_inter in intersections:
            fig.add_vline(x = x_inter, line_dash = "dot")
        st.plotly_chart(fig)