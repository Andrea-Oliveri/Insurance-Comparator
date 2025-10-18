from itertools import combinations
from functools import partial

import streamlit as st
import pandas as pd
import plotly.express as px

import languages



MIN_CHOICES = 2
MAX_CHOICES = 10
MAX_TEXT_INPUTS_LEN = 20
MIN_NUM_INPUTS_VALUE = 0
MAX_NUM_INPUTS_VALUE = 5000


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


def _insurance_params_section(df):
    st.write("### " + languages.get_text("insurance_parameters"))

    # Ensure index of df are unique. It is important later in for loop.
    df = df.reset_index(drop = True)

    # Set up mappings to help with later for loop.
    colnames_to_translation_text = {"label"         : "label",
                                    "cost_per_month": "cost_per_month",
                                    "deducible"     : "deducible",
                                    "excess"        : "excess"}
    if set(colnames_to_translation_text.keys()) != set(df.columns):
        raise RuntimeError(f"Programming error: the provided dataframe does not have the expected column names: {df.columns}.")

    colnames_to_dtypes = {"label"         : "text",
                          "cost_per_month": "number",
                          "deducible"     : "number",
                          "excess"        : "number"}
    missing_keys = set(colnames_to_dtypes.keys()) - set(df.columns)
    if missing_keys:
        raise RuntimeError(f"Programming error: variable colnames_to_dtypes has some missing keys: {missing_keys}.")

    # Create streamlit columns, accounting for the fact we want an extra one compared to what is in the dataframe to put a button
    # that deletes the row.
    col_names = list(df.columns) + ["delete_button"]
    col_sizes = [1] * len(df.columns) + [0.5]
    if len(col_names) != len(col_sizes):
        raise RuntimeError(f"Programming error: something changed and the lenghts don't match...")
    columns = dict(zip(col_names, st.columns(col_sizes, vertical_alignment = "bottom")))
    del col_names, col_sizes

    # Display all values of the dataframe and allow updating.
    for col_name in df.columns:
        with columns[col_name]:
            st.write("**" + languages.get_text(colnames_to_translation_text[col_name]) + "**")

            widget_factory = None
            if colnames_to_dtypes[col_name] == "text":
                widget_factory = partial(st.text_input,
                                         max_chars        = MAX_TEXT_INPUTS_LEN,
                                         type             = "default",
                                         autocomplete     = "off",
                                         label_visibility = "collapsed")
            elif colnames_to_dtypes[col_name] == "number":
                widget_factory = partial(st.number_input,
                                         min_value        = MIN_NUM_INPUTS_VALUE,
                                         max_value        = MAX_NUM_INPUTS_VALUE,
                                         label_visibility = "collapsed")
            else:
                raise RuntimeError(f"Programming error: unhandled data type {colnames_to_dtypes[col_name]}...")

            for idx in df.index:
                df.loc[idx, col_name] = widget_factory(label = f"Entry {idx}, col {col_name}",
                                                       value = df.loc[idx, col_name])

    # Display buttons to delete rows.
    with columns["delete_button"]:
        for idx in df.index:
            if st.button(":material/delete:", key = f"Button to delete row {idx}", disabled = len(df) <= MIN_CHOICES):
                df = df.loc[df.index != idx]

    # Display button to add a row.
    if st.button(languages.get_text("add_row_button"), icon = "➕", key = f"Button to add a row", disabled = len(df) >= MAX_CHOICES):
        new_row = df.iloc[-1:].copy()
        new_row["label"] = f"Option {len(df) + 1}"
        df = pd.concat([df, new_row], axis = "index", ignore_index = True)

    # Return whether entries are good quality.
    entries_ok = True

    # Check the labels provided by user are unique.
    duplicate_labels = ', '.join(df.loc[df["label"].duplicated(), "label"])
    if duplicate_labels:
        st.error(languages.get_text("error_duplicate_labels").format(duplicate_labels), icon = "🚨")
        entries_ok = False

    # It should not be possible for a user to leave a numerical value blank since number_input will re-fill it with previous value.
    # It should also not be possible for a user to have too many or too little lines.
    # Nonetheless, a small chack won't hurt.
    if df[["cost_per_month", "deducible", "excess"]].isna().any(axis = None):
        st.error(languages.get_text("error_required_cols"), icon = "🚨")
        entries_ok = False
    if len(df) < MIN_CHOICES or len(df) > MAX_CHOICES:
        st.error(languages.get_text("error_n_choices_out_of_range").format(MIN_CHOICES, MAX_CHOICES), icon = "🚨")
        entries_ok = False

    return df, entries_ok


def _make_df_points(df):
    df_points = []
    for _, row in df.iterrows():
        cost_per_year = 12 * row["cost_per_month"]
        df_points.append({'label': row['label'], 'health_expenses': 0                                        , 'money_to_insurance': cost_per_year})
        df_points.append({'label': row['label'], 'health_expenses': 0 + row["deducible"]                     , 'money_to_insurance': cost_per_year + row["deducible"]})
        df_points.append({'label': row['label'], 'health_expenses': 0 + row["deducible"] + row["excess"] * 10, 'money_to_insurance': cost_per_year + row["deducible"] + row["excess"]})
        df_points.append({'label': row['label'], 'health_expenses': float("inf")                             , 'money_to_insurance': cost_per_year + row["deducible"] + row["excess"]})
    return pd.DataFrame(df_points)


def _make_df_lines(df_points):
    x = "health_expenses"
    y = "money_to_insurance"

    df_lines = []
    for label, rows in df_points.sort_values(x).groupby("label"):
        for idx in range(len(rows) - 1):
            start_point = rows.iloc[idx]
            end_point   = rows.iloc[idx + 1]
            slope       = (end_point[y] - start_point[y]) / (end_point[x] - start_point[x])
            intercept   = start_point[y] - slope * start_point[x]
            df_lines.append({"label": label, "slope": slope, "intercept": intercept, "x_min": start_point[x], "x_max": end_point[x]})
    return pd.DataFrame(df_lines)


def _make_intersections(df_lines):
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

    st.session_state["button_pressed"] = st.session_state.get("button_pressed", False)
    st.session_state["choices"] = st.session_state.get("choices", _get_example_dataframe())

    # Create section to edit choices dataframe. Also need to handle Streamlit not updating frontend
    # if values are changed from session_state after the widget was rendered. This is done with a rerun
    # if a change is detected.
    df_old = st.session_state["choices"]
    df_new, entries_ok = _insurance_params_section(df_old)
    if not df_old.equals(df_new):
        st.session_state["choices"] = df_new
        st.session_state["button_pressed"] = False
        st.rerun()
    del df_old, df_new

    st.write("### " + languages.get_text("comparison"))
    if st.button(languages.get_text("compare_button"), icon = "🚀", disabled = not entries_ok):
        st.session_state["button_pressed"] = True

    if st.session_state["button_pressed"]:
        df_points     = _make_df_points(st.session_state["choices"])
        df_lines      = _make_df_lines(df_points)
        intersections = _make_intersections(df_lines)

        fig = px.line(df_points, x = "health_expenses", y = "money_to_insurance", color = "label")
        for x_inter in intersections:
            fig.add_vline(x = x_inter, line_dash = "dot")
        st.plotly_chart(fig)