# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from pathlib import Path
import networkx as nx

# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Healthcare Transformation Prioritization Simulator",
    layout="wide"
)

st.title("Healthcare Transformation Prioritization Simulator")
st.caption("Executive decision-support dashboard for healthcare transformation investment prioritization")

# ============================================================
# 3. LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "healthcare_transformation_initiatives.csv"

df = pd.read_csv(DATA_PATH)

# ============================================================
# CUSTOM TOOLTIP STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Tooltip container */
    div[data-baseweb="tooltip"] {
        background-color: #dbeafe !important;
        color: #111827 !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 13px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }

    /* Tooltip text */
    div[data-baseweb="tooltip"] * {
        color: #111827 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 4. CORE EMV & PRIORITIZATION CALCULATIONS
# ============================================================

df["EMV_USD"] = (
    df["Success_Probability"] * df["Success_Impact_USD"] +
    df["Partial_Success_Probability"] * df["Partial_Success_Impact_USD"] +
    df["Failure_Probability"] * df["Failure_Impact_USD"]
)

df["Net_EMV_USD"] = df["EMV_USD"] - df["Estimated_Cost_USD"]

risk_score_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

df["Risk_Score"] = df["Risk_Level"].map(risk_score_map)

df["Normalized_Net_EMV"] = df["Net_EMV_USD"] / df["Net_EMV_USD"].max()
df["Normalized_Readiness"] = df["Operational_Readiness_Score"] / 100
df["Normalized_Risk"] = 1 - (df["Risk_Score"] / 3)

df["Composite_Priority_Score"] = (
    (0.5 * df["Normalized_Net_EMV"]) +
    (0.3 * df["Normalized_Readiness"]) +
    (0.2 * df["Normalized_Risk"])
)

df = df.sort_values("Composite_Priority_Score", ascending=False)

# ============================================================
# DASHBOARD NOTE & DATA DISCLAIMER
# ============================================================

st.sidebar.header("Dashboard Controls")

st.sidebar.markdown(
    """
    **Purpose:**  
    Explore healthcare transformation initiatives using EMV, readiness, risk, scenario analysis, and portfolio prioritization.

    **Use this dashboard to:**  
    - compare initiatives  
    - test uncertainty scenarios  
    - assess readiness  
    - select projects under budget constraints  
    - generate executive recommendations
    """
)

st.sidebar.divider()

with st.sidebar.expander("About this dashboard & data", expanded=False):

    st.markdown(
        """
        <div style='font-size:12px;'>

        This dashboard is an exploratory healthcare transformation intelligence prototype.

        It demonstrates:

        <ul>
        <li>transformation prioritization</li>
        <li>operational readiness modeling</li>
        <li>portfolio governance concepts</li>
        <li>scenario analysis</li>
        <li>risk intelligence</li>
        <li>systems-thinking approaches</li>
        </ul>

        The current version uses simulated and illustrative analytical data for portfolio demonstration purposes.

        The models and assumptions are intended to showcase decision-support methods, not real-world healthcare performance or official implementation outcomes.
        
         📘 See the Documentation section in the sidebar navigation for methodology, assumptions, and dashboard guidance.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 18. SIDEBAR NAVIGATION
# ============================================================

selected_page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Portfolio Analytics",
        "Scenario Analysis",
        "Strategic Portfolio Map",
        "Operational Maturity",
        "Transformation Roadmap",
        "Budget Selection",
        "Dependency Network",
        "Risk Intelligence",
        "Monte Carlo Simulation",
        "Executive Recommendations",
        "Interactive Network",
        "Documentation"
    ]
)

# ============================================================
# 5. SIDEBAR CONTEXTUAL FILTERS & CONTROLS
# ============================================================

# Default values used on pages where controls are hidden
selected_risks = sorted(df["Risk_Level"].unique())
selected_categories = sorted(df["Category"].unique())
success_adjustment = 0.00
available_budget = 4000000

filter_pages = [
    "Executive Overview",
    "Portfolio Analytics",
    "Scenario Analysis",
    "Strategic Portfolio Map",
    "Operational Maturity",
    "Transformation Roadmap",
    "Budget Selection",
    "Risk Intelligence",
    "Monte Carlo Simulation",
    "Executive Recommendations"
]

scenario_pages = [
    "Executive Overview",
    "Portfolio Analytics",
    "Scenario Analysis",
    "Strategic Portfolio Map",
    "Budget Selection",
    "Risk Intelligence",
    "Monte Carlo Simulation",
    "Executive Recommendations"
]

budget_pages = [
    "Budget Selection"
]

no_control_pages = [
    "Dependency Network",
    "Interactive Network",
    "Documentation"
]

if selected_page in filter_pages:

    with st.sidebar.expander("Portfolio Filters", expanded=True):

        selected_risks = st.multiselect(
            "Filter by Risk Level",
            options=sorted(df["Risk_Level"].unique()),
            default=sorted(df["Risk_Level"].unique()),
            help="""
            Filters initiatives by implementation risk level.

            Use this to focus the dashboard on:
            - low-risk quick wins
            - medium-risk transformation options
            - high-risk initiatives requiring stronger governance oversight

            Changing this filter updates relevant dashboard views, including portfolio rankings, scenario outputs, budget selection, risk intelligence, and recommendations.
            """
        )

        selected_categories = st.multiselect(
            "Filter by Category",
            options=sorted(df["Category"].unique()),
            default=sorted(df["Category"].unique()),
            help="""
            Filters initiatives by transformation category.

            Use this to focus analysis on specific transformation domains such as digital health, workforce management, supply chain, reporting, service delivery, or health security.

            Changing this filter updates relevant dashboard views and allows category-specific portfolio analysis.
            """
        )

if selected_page in scenario_pages:

    with st.sidebar.expander("Scenario Controls", expanded=True):

        success_adjustment = st.slider(
            "Adjust Success Probability",
            min_value=-0.20,
            max_value=0.20,
            value=0.00,
            step=0.05,
            help="""
            Simulates changes in overall transformation success conditions.

            Increasing the value:
            - improves portfolio attractiveness
            - increases expected transformation value
            - simulates optimistic implementation conditions

            Decreasing the value:
            - reduces expected outcomes
            - simulates implementation uncertainty
            - models operational or governance instability
            """
        )

if selected_page in budget_pages:

    with st.sidebar.expander("Budget Controls", expanded=True):

        available_budget = st.number_input(
            "Available Portfolio Budget",
            min_value=0,
            value=4000000,
            step=250000,
            help="""
            Simulates financial constraints for healthcare transformation investments.

            The dashboard will attempt to prioritize initiatives within the specified funding envelope.

            Increasing the budget:
            - allows selection of more initiatives
            - expands portfolio coverage

            Decreasing the budget:
            - forces stricter prioritization
            - simulates constrained investment conditions
            """
        )

if selected_page in no_control_pages:

    st.sidebar.info(
        "This page uses fixed documentation, methodology, or dependency logic and does not require interactive filters."
    )

# ============================================================
# 6. APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Risk_Level"].isin(selected_risks)) &
    (df["Category"].isin(selected_categories))
].copy()

if filtered_df.empty:

    st.warning(
        "No initiatives match the selected filters."
    )

    st.stop()

# ============================================================
# 7. DYNAMIC SCENARIO RECALCULATION
# ============================================================

filtered_df["Scenario_Success_Probability"] = (
    filtered_df["Success_Probability"] + success_adjustment
).clip(0, 1)

remaining_probability = (
    1 - filtered_df["Scenario_Success_Probability"]
)

original_non_success_total = (
    filtered_df["Partial_Success_Probability"] +
    filtered_df["Failure_Probability"]
)

filtered_df["Scenario_Partial_Probability"] = (
    filtered_df["Partial_Success_Probability"] /
    original_non_success_total
) * remaining_probability

filtered_df["Scenario_Failure_Probability"] = (
    filtered_df["Failure_Probability"] /
    original_non_success_total
) * remaining_probability

# Recalculate Scenario EMV

filtered_df["Scenario_EMV_USD"] = (
    filtered_df["Scenario_Success_Probability"] * filtered_df["Success_Impact_USD"]
    +
    filtered_df["Scenario_Partial_Probability"] * filtered_df["Partial_Success_Impact_USD"]
    +
    filtered_df["Scenario_Failure_Probability"] * filtered_df["Failure_Impact_USD"]
)

filtered_df["Scenario_Net_EMV_USD"] = (
    filtered_df["Scenario_EMV_USD"] -
    filtered_df["Estimated_Cost_USD"]
)

# ============================================================
# 8. DISPLAY COLUMN DEFINITIONS
# ============================================================

display_cols = [
    "Initiative_ID",
    "Initiative_Name",
    "Category",
    "Estimated_Cost_USD",
    "EMV_USD",
    "Net_EMV_USD",
    "Scenario_Net_EMV_USD",
    "Operational_Readiness_Score",
    "Risk_Level",
    "Composite_Priority_Score",
    "Executive_Recommendation"
]

# ============================================================
# 9. OPERATIONAL MATURITY & READINESS MODELING
# ============================================================

def classify_operational_maturity(score):
    if score < 55:
        return "Chaotic"
    elif score < 65:
        return "Reactive"
    elif score < 75:
        return "Semi-Structured"
    elif score < 85:
        return "Standardized"
    else:
        return "Operationally Mature"


def readiness_gate(row):
    maturity = row["Operational_Maturity_Level"]
    complexity = row["Implementation_Complexity"]

    if complexity == "High" and maturity in ["Chaotic", "Reactive"]:
        return "Not Ready"
    elif complexity == "High" and maturity == "Semi-Structured":
        return "Conditional Readiness"
    else:
        return "Ready"


filtered_df["Operational_Maturity_Level"] = filtered_df[
    "Operational_Readiness_Score"
].apply(classify_operational_maturity)

filtered_df["Transformation_Readiness_Gate"] = filtered_df.apply(
    readiness_gate,
    axis=1
)

# ============================================================
# 10. TRANSFORMATION ROADMAP SEQUENCING
# ============================================================

def assign_transformation_phase(row):
    readiness = row["Operational_Readiness_Score"]
    risk = row["Risk_Level"]

    if readiness >= 80 and risk == "Low":
        return "Phase 1 - Quick Wins"
    elif readiness >= 65 and risk in ["Low", "Medium"]:
        return "Phase 2 - Operational Strengthening"
    else:
        return "Phase 3 - Complex Transformation"


filtered_df["Transformation_Phase"] = filtered_df.apply(
    assign_transformation_phase,
    axis=1
)


# ============================================================
# 11. BUDGET-CONSTRAINED PORTFOLIO SELECTION
# ============================================================

budget_df = filtered_df.sort_values(
    "Composite_Priority_Score",
    ascending=False
).copy()

selected_projects = []
running_cost = 0

for _, row in budget_df.iterrows():
    project_cost = row["Estimated_Cost_USD"]

    if running_cost + project_cost <= available_budget:
        selected_projects.append(row)
        running_cost += project_cost

selected_portfolio_df = pd.DataFrame(selected_projects)

# ============================================================
# 12. TRANSFORMATION DEPENDENCY MODELING
# ============================================================

dependency_summary_map = {
    "EMR Rollout": [
        "Training & LMS Integration",
        "District Performance Dashboard"
    ],

    "Referral Management System": [
        "District Performance Dashboard"
    ],

    "Workforce Scheduling Optimization": [],

    "Medicine Inventory Automation": [
        "District Performance Dashboard"
    ],

    "Telemedicine Expansion": [
        "Referral Management System",
        "Training & LMS Integration"
    ],

    "District Performance Dashboard": [],

    "Training & LMS Integration": [],

    "Emergency Preparedness Coordination Platform": [
        "District Performance Dashboard",
        "Training & LMS Integration"
    ]
}

# ============================================================
# 13. RISK INTELLIGENCE MODELING
# ============================================================

risk_priority_df = filtered_df.copy()

risk_priority_df["Risk_Category"] = risk_priority_df["Risk_Level"]

risk_priority_df["Value_Risk_Position"] = risk_priority_df.apply(
    lambda row: (
        "High Value / High Risk"
        if row["Scenario_Net_EMV_USD"] >= risk_priority_df["Scenario_Net_EMV_USD"].median()
        and row["Risk_Level"] == "High"
        else
        "High Value / Manageable Risk"
        if row["Scenario_Net_EMV_USD"] >= risk_priority_df["Scenario_Net_EMV_USD"].median()
        else
        "Lower Value / Monitor"
    ),
    axis=1
)

# ============================================================
# 14. MONTE CARLO PORTFOLIO SIMULATION
# ============================================================

def simulate_portfolio_once(dataframe):

    total_value = 0

    for _, row in dataframe.iterrows():

        outcome = np.random.choice(
            [
                row["Success_Impact_USD"],
                row["Partial_Success_Impact_USD"],
                row["Failure_Impact_USD"]
            ],
            p=[
                row["Scenario_Success_Probability"],
                row["Scenario_Partial_Probability"],
                row["Scenario_Failure_Probability"]
            ]
        )

        total_value += (
            outcome - row["Estimated_Cost_USD"]
        )

    return total_value

# Run simulation
simulation_results = []

simulation_runs = 1000

for _ in range(simulation_runs):

    simulated_value = simulate_portfolio_once(
        filtered_df
    )

    simulation_results.append(simulated_value)

simulation_df = pd.DataFrame({
    "Simulated_Portfolio_Value": simulation_results
})

# ============================================================
# 15. EXECUTIVE RECOMMENDATION ENGINE
# ============================================================

def generate_recommendation(row):
    if (
        row["Transformation_Readiness_Gate"] == "Ready"
        and row["Composite_Priority_Score"] >= 0.70
        and row["Risk_Level"] in ["Low", "Medium"]
    ):
        return "Prioritize for early implementation"

    elif (
        row["Transformation_Readiness_Gate"] == "Conditional Readiness"
        or row["Risk_Level"] == "High"
    ):
        return "Proceed with risk mitigation and phased rollout"

    elif row["Transformation_Readiness_Gate"] == "Not Ready":
        return "Strengthen operational readiness before investment"

    else:
        return "Monitor for future portfolio consideration"


filtered_df["Executive_Recommendation"] = filtered_df.apply(
    generate_recommendation,
    axis=1
)

# ============================================================
# 16. INTERACTIVE DEPENDENCY NETWORK MODELING
# ============================================================

interactive_dependency_map = {
    "EMR Rollout": [
        "Training & LMS Integration",
        "District Performance Dashboard"
    ],
    "Referral Management System": [
        "District Performance Dashboard"
    ],
    "Workforce Scheduling Optimization": [],
    "Medicine Inventory Automation": [
        "District Performance Dashboard"
    ],
    "Telemedicine Expansion": [
        "Referral Management System",
        "Training & LMS Integration"
    ],
    "District Performance Dashboard": [],
    "Training & LMS Integration": [],
    "Emergency Preparedness Coordination Platform": [
        "District Performance Dashboard",
        "Training & LMS Integration"
    ]
}

# ============================================================
# 17. EXPORTABLE DASHBOARD OUTPUTS
# ============================================================

export_df = filtered_df.copy()

export_csv = export_df.to_csv(index=False).encode("utf-8")

# ============================================================
# 18. EXECUTIVE INTERPRETATION HELPER
# ============================================================

def interpretation_box(items):
    bullet_html = "".join(
        f"<li>{item}</li>" for item in items
    )

    st.markdown(
        f"""
        <div style="
            padding:12px;
            background-color:#f8fafc;
            border-left:4px solid #2563eb;
            border-radius:8px;
            font-size:13px;
            margin-bottom:16px;
        ">
            <b>How to interpret this section</b>
            <ul>
                {bullet_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 10. PAGE — EXECUTIVE OVERVIEW
# ============================================================

if selected_page == "Executive Overview":
    st.subheader("Executive Portfolio Overview")

    st.markdown("""
    This section provides a high-level overview of the healthcare transformation portfolio.

    The objective is to support executive decision-making by summarizing:
    - overall portfolio investment exposure
    - expected transformation value
    - operational readiness
    - initiative prioritization

    The metrics and portfolio table below simulate how healthcare transformation offices, PMOs, and governance teams may evaluate competing strategic investments under operational and financial constraints.
    """)

    interpretation_box([
        "Higher Scenario Net EMV suggests stronger expected transformation value under current assumptions.",
        "Higher readiness scores indicate stronger implementation preparedness.",
        "Large total costs may require phased rollout or budget prioritization.",
        "Use this section to assess overall portfolio exposure and strategic attractiveness."
    ])

    total_initiatives = len(filtered_df)
    total_cost = filtered_df["Estimated_Cost_USD"].sum()
    total_net_emv = filtered_df["Scenario_Net_EMV_USD"].sum()
    average_readiness = filtered_df["Operational_Readiness_Score"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Initiatives", total_initiatives)
    col2.metric("Total Estimated Cost", f"${total_cost:,.0f}")
    col3.metric("Scenario Net EMV", f"${total_net_emv:,.0f}")
    col4.metric("Average Readiness", f"{average_readiness:.1f}")

    st.subheader("Prioritized Initiative Portfolio")

    st.dataframe(
        filtered_df[display_cols],
        use_container_width=True
    )

    st.download_button(
        label="Download Portfolio Data as CSV",
        data=export_csv,
        file_name="healthcare_transformation_portfolio.csv",
        mime="text/csv"
    )

# ============================================================
# 11. PAGE — PORTFOLIO ANALYTICS
# ============================================================

elif selected_page == "Portfolio Analytics":
    st.subheader("Portfolio Analytics")

    st.markdown("""
    This section analyzes healthcare transformation initiatives according to scenario-adjusted expected monetary value (EMV).

    The analysis supports:
    - transformation prioritization
    - investment comparison
    - portfolio tradeoff analysis
    - value-focused decision-making

    The ranking reflects both expected transformation value and implementation uncertainty, helping identify comparatively attractive investment opportunities across the portfolio.
    """)

    interpretation_box([
        "Longer bars indicate initiatives with higher scenario-adjusted expected value.",
        "Initiatives at the top of the ranking may be stronger candidates for prioritization.",
        "Lower-ranked initiatives may still hold strategic importance but may require additional justification.",
        "Use this section to compare financial attractiveness across the portfolio."
    ])

    fig_emv = px.bar(
        filtered_df.sort_values(
            "Scenario_Net_EMV_USD",
            ascending=True
        ),
        x="Scenario_Net_EMV_USD",
        y="Initiative_Name",
        orientation="h",
        title="Healthcare Transformation Initiatives Ranked by Scenario Net EMV",
        hover_data=[
            "Estimated_Cost_USD",
            "Operational_Readiness_Score",
            "Risk_Level"
        ],
        template="plotly_white"
    )

    st.plotly_chart(
        fig_emv,
        use_container_width=True,
        key="portfolio_analytics_chart"
    )

# ============================================================
# 12. PAGE — SCENARIO ANALYSIS
# ============================================================

elif selected_page == "Scenario Analysis":
    st.subheader("Scenario Analysis")

    st.markdown("""
    Healthcare transformation programmes often operate under uncertainty due to operational, governance, financial, and implementation risks.

    This section simulates how changes in transformation success probability may influence portfolio attractiveness and initiative prioritization.

    The scenario adjustment control may be used to explore:
    - optimistic transformation environments
    - conservative implementation conditions
    - uncertainty sensitivity
    - portfolio resilience under changing assumptions
    """)

    interpretation_box([
        "Compare baseline Net EMV with Scenario Net EMV to assess sensitivity to changing assumptions.",
        "Increasing the success adjustment simulates improved implementation conditions.",
        "Decreasing the success adjustment simulates operational or governance uncertainty.",
        "Use this section to test portfolio resilience under varying transformation environments."
    ])

    st.write(
        f"Current success probability adjustment: **{success_adjustment:+.0%}**"
    )

    scenario_cols = [
        "Initiative_ID",
        "Initiative_Name",
        "Success_Probability",
        "Scenario_Success_Probability",
        "Net_EMV_USD",
        "Scenario_Net_EMV_USD"
    ]

    st.dataframe(
        filtered_df[scenario_cols],
        use_container_width=True
    )

# ============================================================
# 13. PAGE — STRATEGIC PORTFOLIO MAP
# ============================================================

elif selected_page == "Strategic Portfolio Map":
    st.subheader("Strategic Portfolio Map")

    st.markdown("""
    The strategic portfolio map visualizes the relationship between operational readiness and transformation value.

    The objective is to identify:
    - operationally mature quick wins
    - high-value but operationally immature initiatives
    - high-risk transformation investments
    - potential sequencing priorities

    Bubble size represents estimated implementation cost, while color reflects implementation risk.
    """)

    interpretation_box([
        "Initiatives toward the upper-right are generally more attractive: higher readiness and higher expected value.",
        "Larger bubbles represent higher-cost initiatives.",
        "Bubble color reflects implementation risk level.",
        "Use this section to identify quick wins, high-risk investments, and sequencing priorities."
    ])

    fig_scatter = px.scatter(
        filtered_df,
        x="Operational_Readiness_Score",
        y="Scenario_Net_EMV_USD",
        size="Estimated_Cost_USD",
        color="Risk_Level",
        hover_name="Initiative_Name",
        text="Initiative_ID",
        title="Operational Readiness vs Scenario Net EMV",
        labels={
            "Operational_Readiness_Score": "Operational Readiness Score",
            "Scenario_Net_EMV_USD": "Scenario Net EMV (USD)",
            "Estimated_Cost_USD": "Estimated Cost"
        },
        template="plotly_white"
    )

    fig_scatter.update_traces(textposition="top center")

    st.plotly_chart(
        fig_scatter,
        use_container_width=True,
        key="strategic_portfolio_map_chart"
    )

# ============================================================
# 14. PAGE — OPERATIONAL MATURITY
# ============================================================

elif selected_page == "Operational Maturity":
    st.subheader("Operational Maturity & Readiness Gate")

    st.markdown("""
    Healthcare transformation success is often influenced by operational maturity rather than technology investment alone.

    This section evaluates whether transformation initiatives are aligned with the operational readiness of the implementation environment.

    The analysis introduces:
    - operational maturity classification
    - transformation readiness gating
    - implementation feasibility assessment
    - operational stabilization considerations

    The objective is to reduce transformation failure risk by aligning transformation ambition with organizational readiness.
    """)

    interpretation_box([
        "Higher maturity levels suggest stronger organizational preparedness for transformation.",
        "Initiatives marked 'Not Ready' may require stabilization before implementation.",
        "Conditional readiness indicates that safeguards or phased rollout approaches may be necessary.",
        "Use this section to align transformation ambition with operational capability."
    ])

    maturity_cols = [
        "Initiative_ID",
        "Initiative_Name",
        "Operational_Readiness_Score",
        "Operational_Maturity_Level",
        "Implementation_Complexity",
        "Transformation_Readiness_Gate"
    ]

    st.dataframe(
        filtered_df[maturity_cols],
        use_container_width=True
    )

    maturity_summary = (
        filtered_df["Operational_Maturity_Level"]
        .value_counts()
        .reset_index()
    )

    maturity_summary.columns = [
        "Operational_Maturity_Level",
        "Number_of_Initiatives"
    ]

    fig_maturity = px.bar(
        maturity_summary,
        x="Operational_Maturity_Level",
        y="Number_of_Initiatives",
        title="Operational Maturity Distribution",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_maturity,
        use_container_width=True,
        key="operational_maturity_chart"
)

# ============================================================
# 15. PAGE — TRANSFORMATION ROADMAP
# ============================================================

elif selected_page == "Transformation Roadmap":
    st.subheader("Transformation Roadmap Sequencing")

    st.markdown("""
    Healthcare transformation initiatives rarely succeed when implemented simultaneously without sequencing discipline.

    This section introduces a phased transformation roadmap that prioritizes:
    - operational stabilization
    - quick wins
    - readiness-building investments
    - phased transformation progression

    The roadmap helps simulate how healthcare transformation offices may structure multi-phase implementation strategies under operational and governance constraints.
    """)

    interpretation_box([
        "Phase 1 initiatives represent comparatively lower-risk quick wins.",
        "Phase 2 initiatives help strengthen operational foundations.",
        "Phase 3 initiatives are more complex and may require sequencing or governance support.",
        "Use this section to simulate phased transformation implementation planning."
    ])

    roadmap_cols = [
        "Initiative_ID",
        "Initiative_Name",
        "Operational_Readiness_Score",
        "Risk_Level",
        "Implementation_Complexity",
        "Transformation_Readiness_Gate",
        "Transformation_Phase"
    ]

    st.dataframe(
        filtered_df[roadmap_cols],
        use_container_width=True
    )

    phase_order = [
        "Phase 1 - Quick Wins",
        "Phase 2 - Operational Strengthening",
        "Phase 3 - Complex Transformation"
    ]

    roadmap_df = filtered_df.copy()
    roadmap_df["Transformation_Phase"] = pd.Categorical(
        roadmap_df["Transformation_Phase"],
        categories=phase_order,
        ordered=True
    )

    roadmap_df = roadmap_df.sort_values(
        ["Transformation_Phase", "Operational_Readiness_Score"],
        ascending=[True, False]
    )

    fig_roadmap = px.bar(
        roadmap_df,
        x="Operational_Readiness_Score",
        y="Initiative_Name",
        color="Transformation_Phase",
        orientation="h",
        title="Transformation Roadmap by Readiness and Phase",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_roadmap,
        use_container_width=True,
        key="transformation_roadmap_chart"
)

# ============================================================
# 16. PAGE — BUDGET SELECTION
# ============================================================

elif selected_page == "Budget Selection":
    st.subheader("Budget-Constrained Portfolio Selection")

    st.markdown("""
    Healthcare transformation programmes frequently operate under constrained financial conditions.

    This section simulates how decision-makers may prioritize initiatives when available investment funding is limited.

    The portfolio selection engine attempts to maximize transformation value within the specified budget constraint while preserving strategic prioritization logic.
    """)

    interpretation_box([
        "The selected portfolio represents initiatives that fit within the available funding constraint.",
        "Higher utilization indicates that more of the available budget is being allocated.",
        "If few initiatives are selected, the portfolio may be financially constrained under current assumptions.",
        "Use this section to simulate investment tradeoffs under limited funding conditions."
    ])

    st.write(
        f"Available budget: **${available_budget:,.0f}**"
    )

    if selected_portfolio_df.empty:
        st.warning("No initiatives can be selected within the current budget.")
    else:
        selected_cost = selected_portfolio_df["Estimated_Cost_USD"].sum()
        selected_net_emv = selected_portfolio_df["Scenario_Net_EMV_USD"].sum()

        st.progress(
            min(selected_cost / available_budget, 1.0)
        )

        st.caption(
            f"Portfolio utilization: "
            f"${selected_cost:,.0f} / ${available_budget:,.0f}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Selected Initiatives", len(selected_portfolio_df))
        col2.metric("Selected Portfolio Cost", f"${selected_cost:,.0f}")
        col3.metric("Selected Portfolio Net EMV", f"${selected_net_emv:,.0f}")

        st.dataframe(
            selected_portfolio_df[
                [
                    "Initiative_ID",
                    "Initiative_Name",
                    "Estimated_Cost_USD",
                    "Scenario_Net_EMV_USD",
                    "Composite_Priority_Score",
                    "Transformation_Phase"
                ]
            ],
            use_container_width=True
        )

        fig_budget = px.bar(
            selected_portfolio_df.sort_values(
                "Scenario_Net_EMV_USD",
                ascending=True
            ),
            x="Scenario_Net_EMV_USD",
            y="Initiative_Name",
            orientation="h",
            title="Selected Portfolio Initiatives by Scenario Net EMV",
            template="plotly_white"
        )

        st.plotly_chart(
            fig_budget,
            use_container_width=True,
            key="budget_selection_chart"
        )   

# ============================================================
# 17. PAGE — DEPENDENCY NETWORK
# ============================================================

elif selected_page == "Dependency Network":

    st.subheader("Healthcare Transformation Dependency Network")

    st.markdown("""
    Healthcare transformation initiatives often operate as interconnected systems rather than isolated projects.

    This section models dependency relationships between initiatives to identify:
    - foundational enabling capabilities
    - dependency-heavy transformation programmes
    - operational bottlenecks
    - sequencing considerations

    The dependency analysis supports systems-oriented transformation planning and governance coordination.
    """)

    interpretation_box([
        "Higher dependency counts indicate initiatives requiring stronger enabling foundations.",
        "Foundational initiatives may support multiple downstream transformation efforts.",
        "Dependency-heavy initiatives may require careful sequencing and governance coordination.",
        "Use this section to identify operational bottlenecks and enabling capabilities."
    ])

    G = nx.DiGraph()

    for initiative, deps in dependency_summary_map.items():

        G.add_node(initiative)

        for dep in deps:
            G.add_edge(dep, initiative)

    dependency_df = pd.DataFrame([
        {
            "Initiative": initiative,
            "Dependency_Count": len(deps)
        }
        for initiative, deps in dependency_summary_map.items()
    ])

    st.dataframe(
        dependency_df.sort_values(
            "Dependency_Count",
            ascending=False
        ),
        use_container_width=True
    )

    fig_dependency = px.bar(
        dependency_df.sort_values(
            "Dependency_Count",
            ascending=True
        ),
        x="Dependency_Count",
        y="Initiative",
        orientation="h",
        title="Transformation Dependency Burden",
        template="plotly_white"
    )

    st.plotly_chart(
        fig_dependency,
        use_container_width=True,
        key="dependency_burden_chart"
    )

# ============================================================
# 18. PAGE — RISK INTELLIGENCE
# ============================================================

elif selected_page == "Risk Intelligence":
    st.subheader("Risk Intelligence")

    st.markdown("""
    Transformation initiatives may simultaneously possess high strategic value and elevated implementation risk.

    This section evaluates the relationship between:
    - expected transformation value
    - implementation risk
    - operational readiness
    - investment exposure

    The analysis supports executive risk assessment by identifying initiatives that may require enhanced governance oversight, phased rollout strategies, or additional mitigation planning.
    """)

    interpretation_box([
        "High-value/high-risk initiatives may require stronger oversight and mitigation planning.",
        "Lower-value initiatives may be deferred unless strategically necessary.",
        "Risk should be interpreted alongside readiness, cost, and transformation value.",
        "Use this section to evaluate strategic risk exposure across the portfolio."
    ])

    risk_cols = [
        "Initiative_ID",
        "Initiative_Name",
        "Risk_Level",
        "Risk_Score",
        "Scenario_Net_EMV_USD",
        "Operational_Readiness_Score",
        "Implementation_Complexity",
        "Value_Risk_Position"
    ]

    st.dataframe(
        risk_priority_df[risk_cols],
        use_container_width=True
    )

    fig_risk = px.scatter(
        risk_priority_df,
        x="Risk_Score",
        y="Scenario_Net_EMV_USD",
        size="Estimated_Cost_USD",
        color="Value_Risk_Position",
        hover_name="Initiative_Name",
        text="Initiative_ID",
        title="Risk vs Scenario Net EMV",
        template="plotly_white"
    )

    fig_risk.update_traces(textposition="top center")

    fig_risk.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 2, 3],
            ticktext=["Low", "Medium", "High"]
        ),
        xaxis_title="Implementation Risk Level",
        yaxis_title="Scenario Net EMV (USD)"
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
        key="risk_intelligence_chart"
    )

# ============================================================
# 19. PAGE — MONTE CARLO SIMULATION
# ============================================================

elif selected_page == "Monte Carlo Simulation":

    st.subheader(
        "Monte Carlo Portfolio Simulation"
    )

    st.markdown("""
    Healthcare transformation programmes are inherently uncertain and may produce varying outcomes depending on operational, financial, and implementation conditions.

    This section applies Monte Carlo simulation techniques to model portfolio uncertainty across multiple simulated transformation scenarios.

    The simulation supports:
    - uncertainty modeling
    - downside exposure assessment
    - outcome variability analysis
    - portfolio resilience evaluation

    The resulting distribution illustrates how portfolio outcomes may vary under probabilistic implementation conditions.
    """)

    interpretation_box([
        "Wider outcome distributions indicate greater portfolio uncertainty.",
        "The 5th percentile represents a conservative downside scenario.",
        "The 95th percentile represents an optimistic upside scenario.",
        "Use this section to understand how portfolio outcomes may vary under uncertainty."
    ])

    mean_value = simulation_df[
        "Simulated_Portfolio_Value"
    ].mean()

    min_value = simulation_df[
        "Simulated_Portfolio_Value"
    ].min()

    max_value = simulation_df[
        "Simulated_Portfolio_Value"
    ].max()

    percentile_5 = simulation_df[
        "Simulated_Portfolio_Value"
    ].quantile(0.05)

    percentile_95 = simulation_df[
        "Simulated_Portfolio_Value"
    ].quantile(0.95)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Mean Portfolio Value", f"${mean_value:,.0f}")
    col2.metric("Minimum Outcome", f"${min_value:,.0f}")
    col3.metric("Maximum Outcome", f"${max_value:,.0f}")
    col4.metric("5th Percentile", f"${percentile_5:,.0f}")
    col5.metric("95th Percentile", f"${percentile_95:,.0f}")

    fig_simulation = px.histogram(
        simulation_df,
        x="Simulated_Portfolio_Value",
        nbins=40,
        title="Monte Carlo Portfolio Outcome Distribution",
        template="plotly_white"
    )

    fig_simulation.update_layout(
        bargap=0.05
    )

    fig_simulation.add_vline(
        x=percentile_5,
        line_dash="dash",
        line_color="red",
        annotation_text="5th Percentile"
    )

    fig_simulation.add_vline(
        x=percentile_95,
        line_dash="dash",
        line_color="green",
        annotation_text="95th Percentile"
    )

    st.plotly_chart(
        fig_simulation,
        use_container_width=True,
        key="monte_carlo_simulation_chart"
    )

# ============================================================
# 20. PAGE — EXECUTIVE RECOMMENDATIONS
# ============================================================

elif selected_page == "Executive Recommendations":
    st.subheader("Executive Recommendations")

    st.markdown("""
    This section translates analytical outputs into simplified executive-level transformation guidance.

    Recommendations are generated using:
    - transformation readiness
    - operational maturity
    - implementation risk
    - prioritization scoring
    - transformation sequencing logic

    The objective is to simulate how transformation governance teams may derive actionable strategic recommendations from portfolio analytics.
    """)

    interpretation_box([
        "Recommendations translate analytical outputs into simplified strategic guidance.",
        "Initiatives recommended for prioritization may represent stronger early implementation candidates.",
        "Risk mitigation recommendations indicate elevated implementation uncertainty.",
        "Readiness-focused recommendations suggest operational strengthening before investment."
    ])

    recommendation_cols = [
        "Initiative_ID",
        "Initiative_Name",
        "Scenario_Net_EMV_USD",
        "Composite_Priority_Score",
        "Risk_Level",
        "Transformation_Readiness_Gate",
        "Transformation_Phase",
        "Executive_Recommendation"
    ]

    st.dataframe(
        filtered_df[recommendation_cols],
        use_container_width=True
    )

    recommendation_summary = (
        filtered_df["Executive_Recommendation"]
        .value_counts()
        .reset_index()
    )

    recommendation_summary.columns = [
        "Executive_Recommendation",
        "Number_of_Initiatives"
    ]

    fig_recommendations = px.bar(
        recommendation_summary,
        x="Executive_Recommendation",
        y="Number_of_Initiatives",
        title="Executive Recommendation Summary",
        template="plotly_white"
    )
    
    recommendation_export = filtered_df[recommendation_cols].to_csv(
        index=False
    ).encode("utf-8")

    fig_recommendations.update_layout(
        xaxis_tickangle=-15
    )

    st.plotly_chart(
        fig_recommendations,
        use_container_width=True,
        key="executive_recommendations_chart"
    )

    st.download_button(
        label="Download Executive Recommendations as CSV",
        data=recommendation_export,
        file_name="executive_recommendations.csv",
        mime="text/csv"
    )

# ============================================================
# 21. PAGE — INTERACTIVE DEPENDENCY NETWORK
# ============================================================

elif selected_page == "Interactive Network":
    st.subheader("Interactive Transformation Dependency Network")

    st.markdown("""
    This interactive network visualizes transformation interdependencies across the healthcare portfolio.

    The network highlights:
    - foundational initiatives
    - enabling capabilities
    - interconnected transformation clusters
    - dependency-heavy programmes

    Node size reflects enabling influence within the transformation ecosystem, while network relationships illustrate how transformation initiatives may interact within a broader operational architecture.
    """)

    interpretation_box([
        "Larger nodes indicate initiatives with greater enabling influence within the portfolio.",
        "Connections represent transformation interdependencies.",
        "Highly connected initiatives may represent foundational transformation capabilities.",
        "Use this section to understand the portfolio as an interconnected operational system."
    ])

    G = nx.DiGraph()

    for initiative, deps in interactive_dependency_map.items():

        G.add_node(initiative)

        for dep in deps:
            G.add_edge(dep, initiative)

    pos = nx.spring_layout(
        G,
        seed=42,
        k=1.2
    )

    edge_x = []
    edge_y = []

    for source, target in G.edges():

        x0, y0 = pos[source]
        x1, y1 = pos[target]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = px.line(
        x=edge_x,
        y=edge_y
    ).data[0]

    edge_trace.update(
        line=dict(
            width=1,
            color="rgba(100,100,100,0.35)"
        ),
        hoverinfo="none",
        mode="lines"
    )

    node_x = []
    node_y = []
    node_text = []
    node_size = []

    for node in G.nodes():

        x, y = pos[node]

        dependency_count = len(
            interactive_dependency_map.get(node, [])
        )

        enabled_count = G.out_degree(node)

        node_x.append(x)
        node_y.append(y)

        node_text.append(
            f"{node}<br>"
            f"Dependencies: {dependency_count}<br>"
            f"Enables: {enabled_count}"
        )

        node_size.append(
            20 + (enabled_count * 10)
        )

    network_df = pd.DataFrame({
        "x": node_x,
        "y": node_y,
        "Initiative": list(G.nodes()),
        "Node_Info": node_text,
        "Node_Size": node_size
    })

    fig_network = px.scatter(
        network_df,
        x="x",
        y="y",
        size="Node_Size",
        text="Initiative",
        custom_data=["Node_Info"],
        title="Interactive Healthcare Transformation Dependency Network",
        template="plotly_white"
    )

    fig_network.add_trace(edge_trace)

    fig_network.update_traces(
        textposition="top center",
        hovertemplate="%{customdata[0]}<extra></extra>"
    )

    fig_network.update_layout(
        showlegend=False,
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            visible=False
        ),
        height=700,
        plot_bgcolor="white",
        paper_bgcolor="white",
        hoverlabel=dict(
            bgcolor="#dbeafe",
            font_size=12,
            font_family="Arial",
            font_color="#111827"
        )
    )

    st.plotly_chart(
        fig_network,
        use_container_width=True,
        key="interactive_dependency_network_chart"
    )

# ============================================================
# 22. PAGE — DOCUMENTATION
# ============================================================

elif selected_page == "Documentation":

    st.title(
        "Dashboard Documentation & Methodology"
    )

    interpretation_box([
        "This section explains the dashboard methodology, assumptions, and analytical logic.",
        "Use the documentation to understand how the models, simulations, and prioritization approaches were constructed.",
        "The current dashboard uses simulated data for demonstration and portfolio purposes.",
        "This section provides context for interpreting all analytical outputs across the dashboard."
    ])

    DOCS_PATH = BASE_DIR / "docs" / "Dashboard_User_Manual.md"

    with open(
        DOCS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        manual_text = file.read()

    st.markdown(manual_text)

    
st.divider()

st.caption(
    "Healthcare Transformation Prioritization Simulator | Exploratory Portfolio Governance & Transformation Intelligence Prototype"
)