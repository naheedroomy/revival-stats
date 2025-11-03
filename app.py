import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Revival Cup Analytics", layout="wide")

st.title("🎮 Revival Cup Analytics Dashboard")

# Load all JSON files
data_dir = os.path.dirname(__file__)

def load_json(filename):
    try:
        with open(os.path.join(data_dir, filename), 'r') as f:
            return pd.DataFrame(json.load(f))
    except:
        return pd.DataFrame()

# Load all data
summary_df = load_json("Summary.json")
players_df = load_json("All_Players.json")
kd_leaders_df = load_json("KD_Leaders.json")
damage_leaders_df = load_json("Damage_Leaders.json")
clutch_masters_df = load_json("Clutch_Masters.json")
economy_leaders_df = load_json("Economy_Leaders.json")
win_rate_leaders_df = load_json("Win_Rate_Leaders.json")
ability_usage_df = load_json("Ability_Usage.json")
agent_meta_df = load_json("Agent_Meta.json")
top_killers_df = load_json("Top_Killers.json")
mvp_rankings_df = load_json("MVP_Rankings.json")
headshot_leaders_df = load_json("Headshot_Leaders.json")
first_kills_leaders_df = load_json("First_Kills_Leaders.json")

# Navigation
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Summary",
    "All Players",
    "Agent Meta",
    "Leaderboards",
    "Clutch Analysis",
    "Economy",
    "Ability Usage",
    "MVP Rankings"
])

with tab1:
    st.header("Tournament Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Players", int(summary_df[summary_df['Metric'] == 'Total Players']['Value'].values[0]))
    with col2:
        st.metric("Total Matches", int(summary_df[summary_df['Metric'] == 'Total Matches']['Value'].values[0]))
    with col3:
        st.metric("Total Rounds", int(summary_df[summary_df['Metric'] == 'Total Rounds Played']['Value'].values[0]))
    with col4:
        st.metric("Total Kills", int(summary_df[summary_df['Metric'] == 'Total Kills']['Value'].values[0]))

    st.subheader("All Summary Metrics")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

with tab2:
    st.header("All Players Statistics")

    # Add sorting and filtering
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by:", players_df.columns)
    with col2:
        sort_order = st.radio("Order:", ["Descending", "Ascending"])

    sorted_df = players_df.sort_values(by=sort_by, ascending=(sort_order == "Ascending"))
    st.dataframe(sorted_df, use_container_width=True, hide_index=True)

with tab3:
    st.header("Agent Meta Analysis")
    st.dataframe(agent_meta_df, use_container_width=True, hide_index=True)

with tab4:
    st.header("Leaderboards")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("K/D")
        st.dataframe(kd_leaders_df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Damage")
        st.dataframe(damage_leaders_df, use_container_width=True, hide_index=True)

    with col3:
        st.subheader("Top Killers")
        st.dataframe(top_killers_df, use_container_width=True, hide_index=True)

    st.subheader("Headshots")
    st.dataframe(headshot_leaders_df, use_container_width=True, hide_index=True)

    st.subheader("First Kills")
    st.dataframe(first_kills_leaders_df, use_container_width=True, hide_index=True)

with tab5:
    st.header("Clutch Analysis")

    # Remove Main Agent column for display
    clutch_display_df = clutch_masters_df.drop(columns=['Main Agent'], errors='ignore')

    # Show clutch distribution columns
    clutch_cols = [col for col in clutch_display_df.columns if col not in ['Player', 'Total Clutches', 'Clutch Attempts', 'Clutch %']]

    st.subheader("Clutch Statistics")
    st.dataframe(clutch_display_df, use_container_width=True, hide_index=True)

    if clutch_cols:
        st.subheader("Clutch Distribution Summary")
        clutch_summary = clutch_masters_df[clutch_cols].sum()
        st.bar_chart(clutch_summary)

with tab6:
    st.header("Economy Analysis")
    st.dataframe(economy_leaders_df, use_container_width=True, hide_index=True)

with tab7:
    st.header("Ability Usage")
    st.dataframe(ability_usage_df, use_container_width=True, hide_index=True)

with tab8:
    st.header("MVP Rankings")
    st.dataframe(mvp_rankings_df, use_container_width=True, hide_index=True)

    st.subheader("What is Impact Rating?")
    st.markdown("""
Impact Rating is a normalized composite metric measuring overall player contribution:

**Formula:** K/D + (FK-FD × 0.2) + (Win% ÷ 100) + (ACS ÷ 300) + Clutch Factor

**Components** (all normalized to contribute proportionally):

- **K/D Ratio** - Combat efficiency (0.5-2.5 typical)
- **FK-FD × 0.2** - Opening duel impact (first kills win rounds)
- **Win Rate ÷ 100** - Contribution to team success (0.0-1.0)
- **ACS ÷ 300** - Average Combat Score (Riot's per-round performance metric)
  - 300+ ACS is extraordinary
  - Includes kills, assists, plants, defuses, ability usage
- **Clutch Factor** - Weighted clutch performance per match (0.0-0.3+)
  - 1v2 = 1 point | 1v3 = 2 points | 1v4 = 3 points | 1v5 = 4 points
  - Formula: (Weighted Clutches ÷ Matches) ÷ 3

**Why this works:**
- ✅ All components normalized - no arbitrary weights
- ✅ Rewards well-rounded players across all dimensions
- ✅ No agent/role bias - works for fraggers and support players
- ✅ Penalizes stat-padding on losing teams (Win% component)
- ✅ Values opening duels (crucial in competitive Valorant)
- ✅ Recognizes clutch ability (winning impossible situations)

**Minimum 6 matches required for statistical significance.**
    """)
