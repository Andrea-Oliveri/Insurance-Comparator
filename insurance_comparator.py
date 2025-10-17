from itertools import combinations

import streamlit as st
import pandas as pd
import plotly.express as px



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
    
    
def _check_insurance_params(df):
    for idx, row in df.iterrows():
        if any(pd.isna(row[col]) for col in ["Cost per Month", "Deducible", "Excess"]):
            st.error("Please fill out all values in columns 'Cost per Month', 'Deducible' and 'Excess'", icon = "🚨")
            return False
        if pd.isna(row["Label"]):
            st.session_state["choices"].loc[idx, "Label"] = f"Choice N. {idx}"
    return True
    
    

def _make_df_lines(df):
    df_lines = []
    for _, row in df.iterrows():
        row["Cost per Year"] = 12 * row["Cost per Month"]
        df_lines.append({'Label': row['Label'], 'Health Expenses': 0, 'Money Given to Insurance': row["Cost per Year"]})
        df_lines.append({'Label': row['Label'], 'Health Expenses': 0 + row["Deducible"], 'Money Given to Insurance': row["Cost per Year"] + row["Deducible"]})
        df_lines.append({'Label': row['Label'], 'Health Expenses': 0 + row["Deducible"] + row["Excess"] * 10, 'Money Given to Insurance': row["Cost per Year"] + row["Deducible"] + row["Excess"]})        
        df_lines.append({'Label': row['Label'], 'Health Expenses': float("inf"), 'Money Given to Insurance': row["Cost per Year"] + row["Deducible"] + row["Excess"]})
    return pd.DataFrame(df_lines)


def _make_intersections(df_lines):
    x = "Health Expenses"
    y = "Money Given to Insurance"
    
    df_lines_new = []
    for label, rows in df_lines.sort_values(x).groupby("Label"):
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
    title = "Insurance Comparator"
    _set_page_config(title, "💸")
    
    st.title(title)
    st.write(
        """
        I built this tool to help you decide which base health insurance is the
        most appropriate for you in the year to come. If you provide me the deducible
        and monthly payout of any insurance, I can run a simple simulation and tell you
        how much you would need to spend in medical expenses next year for the more
        expensive insurance to actually be worth it. Give it a try 😃.
        """
    )
    
    st.session_state["choices"] = st.session_state.get(
        "choices",
        pd.DataFrame([{"Label": "Example 1", "Cost per Month": 500, "Deducible": 300 , "Excess": 700},
                      {"Label": "Example 2", "Cost per Month": 400, "Deducible": 2500, "Excess": 700}],
                     index = [1, 2])
    )

    st.write("### Insurance Parameters")
    st.session_state["choices"] = st.data_editor(st.session_state["choices"],
                                                 hide_index = False,
                                                 num_rows   = "dynamic" if len(st.session_state["choices"]) < MAX_CHOICES else "fixed",
                                                 disabled   = False)
    st.session_state["choices"].index = range(1, len(st.session_state["choices"]) + 1)
    
    if st.button("Compare 🚀"):        
        if _check_insurance_params(st.session_state["choices"]):
            df_lines = _make_df_lines(st.session_state["choices"])
            intersections = _make_intersections(df_lines)
            
            fig = px.line(df_lines, x = "Health Expenses", y = "Money Given to Insurance", color = "Label")
            for x_inter in intersections:
                fig.add_vline(x = x_inter, line_dash = "dot")
            st.plotly_chart(fig)