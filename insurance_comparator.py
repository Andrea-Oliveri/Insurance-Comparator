from itertools import combinations
from functools import partial

import streamlit as st
import streamlit_analytics
import pandas as pd
import numpy as np
import plotly.express as px

from src import constants
from src import languages



def _set_page_config(title, icon):
    st.set_page_config(page_title = title, page_icon = icon)

    st.markdown(
        """
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            .block-container {
                padding-top: 4rem;
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
    if not st.session_state.get("language_inferred_from_locale", False) and st.context.locale is not None:
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

    language = st.pills(
        label          = languages.get_text("choose_language"),
        options        = language_options.keys(),
        selection_mode = "single",
        default        = previous_language,
        format_func    = language_options.get
    )

    languages.set_lang(language)

    if language != previous_language:
        st.rerun()


def _get_example_dataframe():
    return pd.DataFrame([
        {"label": f"Option 1", "cost_per_month": 500., "deducible": 300. , "excess": 700.},
        {"label": f"Option 2", "cost_per_month": 400., "deducible": 2500., "excess": 700.}
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

    # We need to do a bit of CSS hacking to prevent flex layout used by Streamlit columns from wrapping the elements on the same line when
    # the viewport width gets too small.
    st.markdown(
        """
        <style>
            div.stHorizontalBlock {
                display: flex !important;
                flex-flow: row no-wrap !important;
                min-width: 45rem;
            }
            div.stColumn {
                flex: 1 1 auto;
                min-width: 1rem;
            }
        </style>
        """,
        unsafe_allow_html = True)

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
                                         max_chars        = constants.MAX_TEXT_INPUTS_LEN,
                                         type             = "default",
                                         autocomplete     = "off",
                                         label_visibility = "collapsed")
            elif colnames_to_dtypes[col_name] == "number":
                widget_factory = partial(st.number_input,
                                         min_value        = constants.MIN_NUM_INPUTS_VALUE,
                                         max_value        = constants.MAX_NUM_INPUTS_VALUE,
                                         format           = "%0.2f",
                                         label_visibility = "collapsed")
            else:
                raise RuntimeError(f"Programming error: unhandled data type {colnames_to_dtypes[col_name]}...")

            for idx in df.index:
                df.loc[idx, col_name] = widget_factory(label = f"Entry {idx}, col {col_name}",
                                                       value = df.loc[idx, col_name])

    # Display buttons to delete rows.
    with columns["delete_button"]:
        for idx in df.index:
            if st.button(":material/delete:", key = f"Button to delete row {idx}", disabled = len(df) <= constants.MIN_CHOICES):
                df = df.loc[df.index != idx]

    # Display button to add a row.
    if st.button(languages.get_text("add_row_button"), icon = "➕", key = f"Button to add a row", disabled = len(df) >= constants.MAX_CHOICES):
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
    if len(df) < constants.MIN_CHOICES or len(df) > constants.MAX_CHOICES:
        st.error(languages.get_text("error_n_choices_out_of_range").format(constants.MIN_CHOICES, constants.MAX_CHOICES), icon = "🚨")
        entries_ok = False

    return df, entries_ok


def _make_df_points(df, mergin_right_ratio = 0.15):
    df_points = []
    for _, row in df.iterrows():
        cost_per_year = 12 * row["cost_per_month"]
        df_points.append({'label': row['label'], 'health_expenses': 0                                        , 'money_to_insurance': cost_per_year})
        df_points.append({'label': row['label'], 'health_expenses': 0 + row["deducible"]                     , 'money_to_insurance': cost_per_year + row["deducible"]})
        df_points.append({'label': row['label'], 'health_expenses': 0 + row["deducible"] + row["excess"] * 10, 'money_to_insurance': cost_per_year + row["deducible"] + row["excess"]})
        df_points.append({'label': row['label'], 'health_expenses': np.inf                                   , 'money_to_insurance': cost_per_year + row["deducible"] + row["excess"]})
    df_points = pd.DataFrame(df_points)

    # Replace infinites with finite larger than all other points.
    mask = np.isfinite(df_points['health_expenses'])
    right_lim = (1 + mergin_right_ratio) * df_points.loc[mask, 'health_expenses'].max()
    df_points.loc[~mask, 'health_expenses'] = right_lim

    return df_points


def _make_df_lines(df_points, x_col = "health_expenses", y_col = "money_to_insurance"):
    df_lines = []
    for label, rows in df_points.sort_values(x_col).groupby("label"):
        for idx in range(len(rows) - 1):
            start_point = rows.iloc[idx]
            end_point   = rows.iloc[idx + 1]
            slope       = (end_point[y_col] - start_point[y_col]) / (end_point[x_col] - start_point[x_col])
            intercept   = start_point[y_col] - slope * start_point[x_col]
            df_lines.append({"label": label, "slope": slope, "intercept": intercept, "x_min": start_point[x_col], "x_max": end_point[x_col]})
    return pd.DataFrame(df_lines)


def _make_intersections(df_lines):
    intersections = set()
    for label1, label2 in combinations(df_lines["label"].unique(), 2):
        for _, line1 in df_lines[df_lines["label"] == label1].iterrows():
            for _, line2 in df_lines[df_lines["label"] == label2].iterrows():
                if line1["slope"] == line2["slope"]:
                    continue # In this scenario, we don't care for perfectly overlapping lines
                x_inter = (line2["intercept"] - line1["intercept"]) / (line1["slope"] - line2["slope"])
                if x_inter < line1["x_min"] or x_inter < line2["x_min"] or x_inter > line1["x_max"] or x_inter > line2["x_max"]:
                    continue
                intersections.add(x_inter)
    return sorted(intersections)


def _draw_comparison_table(df_points, intersections):
    unique_labels = df_points["label"].unique()

    df_comparison = []
    for idx in range(len(intersections) + 1):
        range_start = 0      if idx == 0                  else intersections[idx - 1]
        range_end   = np.inf if idx == len(intersections) else intersections[idx]
        middle      = (range_start + range_end) / 2 if np.isfinite(range_end) else range_start + 1000

        # Sort functions by which is smallest in the range.
        sorted_idx = np.argsort([_get_y_at_x(df_points, label, x = middle) for label in unique_labels])

        # Store the 3 cheapest options.
        df_comparison.append({"start": range_start,
                              "end"  : range_end,
                              "1st"  : unique_labels[sorted_idx[0]],
                              "2nd"  : unique_labels[sorted_idx[1]],
                              "3rd"  : None if len(sorted_idx) < 3 else unique_labels[sorted_idx[2]]})
    df_comparison = pd.DataFrame(df_comparison)

    # Merge ranges which are adjacent and for which the ranking does not change.
    columns_order = df_comparison.columns
    groupby_columns = ["1st", "2nd", "3rd"]
    groups_consecutive = df_comparison[groupby_columns].ne(df_comparison[groupby_columns].shift()) \
                                                       .any(axis = "columns") \
                                                       .cumsum()
    df_comparison = df_comparison.groupby(groups_consecutive) \
                                 .agg({"start": "min", "end": "max"} | {e: "first" for e in groupby_columns}) \
                                 .reset_index()
    df_comparison = df_comparison[columns_order]

    # Build final nicely formatted dataframe, with translated text.
    df_final = []
    for _, row in df_comparison.iterrows():
        range_text = languages.get_text("health_expenses_range_any")                                 if row["start"] == 0 and not np.isfinite(row["end"]) else \
                     languages.get_text("health_expenses_range_less")   .format(round(row["end"]))   if row["start"] == 0 else \
                     languages.get_text("health_expenses_range_over")   .format(round(row["start"])) if not np.isfinite(row["end"]) else \
                     languages.get_text("health_expenses_range_between").format(round(row["start"]), round(row["end"]))

        df_final.append({
            languages.get_text("colname_spend_per_year"): range_text,
            "🥇 " + languages.get_text("colname_1st_cheapest"): row["1st"],
            "🥈 " + languages.get_text("colname_2nd_cheapest"): row["2nd"],
            "🥉 " + languages.get_text("colname_3rd_cheapest"): row["3rd"]
        })
    df_final = pd.DataFrame(df_final)
    df_final.columns = [f"**{e}**" for e in df_final.columns]
    df_final = df_final.set_index(df_final.columns[0], drop = True)
    st.table(df_final)


def _get_y_at_x(df_points, label, x, x_col = "health_expenses", y_col = "money_to_insurance"):
    df_points = df_points[df_points["label"] == label].sort_values(x_col)
    return np.interp(x, df_points[x_col], df_points[y_col])


def _draw_comparison_plot(df_points, intersections, x_col = "health_expenses", y_col = "money_to_insurance", color_col = "label"):
    color_col_ordering = df_points[color_col].unique()

    # Add points to the lines, since Plotly will draw hover legends only on actual points, not on the interpolated parts of the line.
    new_x_coords = set(np.arange(0, df_points[x_col].max(), constants.PLOT_INTERP_STEP)) | set(intersections)
    new_rows = []

    for label, df_label in df_points.groupby(color_col):
         x = list(new_x_coords - set(df_label[x_col]))
         y = _get_y_at_x(df_points, label, x)
         for x_iter, y_iter in zip(x, y):
             new_rows.append({color_col: label, x_col: x_iter, y_col: y_iter})

    df_points = pd.concat([df_points, pd.DataFrame(new_rows)], axis = "index", ignore_index = True)
    df_points[color_col] = pd.Categorical(df_points[color_col], categories = color_col_ordering)
    df_points = df_points.sort_values([color_col, x_col])

    # Draw interactive plots.
    fig = px.line(df_points, x = x_col, y = y_col, color = color_col,
                  labels = {x_col    : languages.get_text("health_expenses_plot"),
                            y_col    : languages.get_text("money_to_insurance_plot"),
                            color_col: languages.get_text("labels_plot")},
                  custom_data = ['label'])

    fig.update_traces(hovertemplate = languages.get_text("hover_template"))

    fig.update_layout(hovermode = "x unified",
                      yaxis = {"fixedrange": True},
                      xaxis = {"fixedrange": True,
                               "unifiedhovertitle": {"text": languages.get_text("hover_title")}})

    st.plotly_chart(fig, config = {'displaylogo': False})



if __name__ == "__main__":
    with streamlit_analytics.track(unsafe_password = st.secrets["ANALYTICS_PASSWORD"]):
        _choose_language()

        _set_page_config(languages.get_text("title"), icon = "💸")

        st.write("\n")
        st.title(languages.get_text("title"))
        st.write(languages.get_text("decription"))

        st.session_state["choices"] = st.session_state.get("choices", _get_example_dataframe())

        # Create section to edit choices dataframe. Also need to handle Streamlit not updating frontend
        # if values are changed from session_state after the widget was rendered. This is done with a rerun
        # if a change is detected.
        df_old = st.session_state["choices"]
        df_new, entries_ok = _insurance_params_section(df_old)
        if not df_old.equals(df_new):
            st.session_state["choices"] = df_new
            st.rerun()
        del df_old, df_new

        st.write("### " + languages.get_text("comparison"))
        df_points     = _make_df_points(st.session_state["choices"])
        df_lines      = _make_df_lines(df_points)
        intersections = _make_intersections(df_lines)

        st.write(languages.get_text("comparison_table_explaination"))
        _draw_comparison_table(df_points, intersections)

        st.write(languages.get_text("comparison_plot_explaination"))
        _draw_comparison_plot(df_points, intersections)