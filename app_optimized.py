import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils_optimized import (
    load_data, create_lookup_index, fast_lookup_scenario, format_currency,
    get_bucket_mappings, get_status_insights, get_wealth_timeline
)

# Page config
st.set_page_config(
    page_title="PFM Compass - Retirement Planning",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #262730;
    }
    .metric-card h2, .metric-card h3, .metric-card p {
        color: #262730 !important;
        margin: 0.2rem 0;
    }
    .status-green { border-left: 5px solid #28a745; background-color: #f8fff9; }
    .status-yellow { border-left: 5px solid #ffc107; background-color: #fffef8; }
    .status-red { border-left: 5px solid #dc3545; background-color: #fff8f8; }
    .insight-box {
        background-color: #e8f4f8;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #17a2b8;
        color: #262730;
    }
</style>
""", unsafe_allow_html=True)

# Performance-optimized data loading
@st.cache_data(show_spinner=True)
def get_data_and_index():
    """Load data and create lookup index in one cached operation"""
    with st.spinner("🚀 Loading retirement scenarios..."):
        df = load_data()
        if df is None:
            return None, None
        
        lookup_dict = create_lookup_index(df)
        return df, lookup_dict

# Initialize session state
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# Load data once
df, lookup_dict = get_data_and_index()

if df is None or lookup_dict is None:
    st.error("❌ Failed to load retirement scenarios data. Please check the data file.")
    st.stop()

# Get bucket mappings
mappings = get_bucket_mappings()

# App header
st.title("🎯 PFM Compass - Retirement Planning MVP")
st.markdown("### Internal Employee Testing - Retirement Scenario Analysis")

# Streamlined data overview
with st.expander("📊 Data Overview"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Scenarios", f"{len(df):,}")
    with col2:
        green_pct = (df['status_color'] == 'green').sum() / len(df) * 100
        st.metric("Green Status %", f"{green_pct:.1f}%")
    with col3:
        fire_achievable_pct = df['fire_achievable'].sum() / len(df) * 100
        st.metric("FIRE Achievable %", f"{fire_achievable_pct:.1f}%")

# Sidebar input form
st.sidebar.header("👤 Your Profile")

age_bucket = st.sidebar.selectbox(
    "年齢 / Age",
    options=list(mappings['age_bucket'].keys()),
    format_func=lambda x: mappings['age_bucket'][x]
)

income_bucket = st.sidebar.selectbox(
    "年収 / Annual Income",
    options=list(mappings['income_bucket'].keys()),
    format_func=lambda x: mappings['income_bucket'][x]
)

current_savings_bucket = st.sidebar.selectbox(
    "現在の貯蓄 / Current Savings",
    options=list(mappings['current_savings_bucket'].keys()),
    format_func=lambda x: mappings['current_savings_bucket'][x]
)

monthly_savings_bucket = st.sidebar.selectbox(
    "月間貯蓄額 / Monthly Savings",
    options=list(mappings['monthly_savings_bucket'].keys()),
    format_func=lambda x: mappings['monthly_savings_bucket'][x]
)

expected_expenses_bucket = st.sidebar.selectbox(
    "希望生活費 / Expected Monthly Expenses",
    options=list(mappings['expected_expenses_bucket'].keys()),
    format_func=lambda x: mappings['expected_expenses_bucket'][x]
)

gender = st.sidebar.selectbox(
    "性別 / Gender",
    options=["m", "f"],
    format_func=lambda x: "男性 (Male)" if x == "m" else "女性 (Female)"
)

household_size = st.sidebar.selectbox(
    "世帯人数 / Household Size",
    options=[1, 2, 3, 4],
    format_func=lambda x: f"{x}人"
)

housing_status = st.sidebar.selectbox(
    "住居状況 / Housing Status",
    options=list(mappings['housing_status'].keys()),
    format_func=lambda x: mappings['housing_status'][x]
)

marital_status = st.sidebar.selectbox(
    "婚姻状況 / Marital Status",
    options=["s", "m"],
    format_func=lambda x: "独身 (Single)" if x == "s" else "既婚 (Married)"
)

retirement_age_bucket = st.sidebar.selectbox(
    "希望退職年齢 / Target Retirement Age",
    options=list(mappings['retirement_age_bucket'].keys()),
    format_func=lambda x: mappings['retirement_age_bucket'][x]
)

# Analysis trigger
analyze_clicked = st.sidebar.button("🔍 分析開始 / Analyze", type="primary")

if analyze_clicked:
    with st.spinner("分析中... / Analyzing..."):
        result = fast_lookup_scenario(
            lookup_dict,
            age_bucket,
            current_savings_bucket,
            expected_expenses_bucket,
            gender,
            household_size,
            housing_status,
            income_bucket,
            marital_status,
            monthly_savings_bucket,
            retirement_age_bucket
        )

    if result is not None:
        st.session_state.analysis_result = result
        st.session_state.analysis_completed = True
        st.rerun()
    else:
        st.error("❌ No matching scenario found. Please try different parameters.")
        st.info("💡 Tip: Try adjusting your income, savings, or age ranges.")
        st.session_state.analysis_completed = False

# Display results
if st.session_state.analysis_completed and st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result

    st.markdown("## 📈 Your Retirement Analysis Results")
    col1, col2, col3 = st.columns(3)

    status_colors = {
        "green": "🟢 良好 (Good)",
        "yellow": "🟡 注意 (Caution)",
        "red": "🔴 要改善 (Needs Improvement)"
    }
    status_class = f"status-{result['status_color']}"

    with col1:
        st.markdown(f"""
        <div class="metric-card {status_class}">
            <h3>総合評価 / Overall Status</h3>
            <h2>{status_colors.get(result['status_color'], result['status_color'])}</h2>
            <p>Traditional Grade: {result['traditional_grade']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>退職可能年齢 / Retirement Age</h3>
            <h2>{result['traditional_retirement_age']:.1f}歳</h2>
            <p>FIRE Grade: {result['fire_grade']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>予想総資産 / Projected Wealth</h3>
            <h2>{format_currency(result['projected_wealth'])}</h2>
            <p>FIRE Achievement: {result['fire_percentage']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Detailed analysis
    st.markdown("---")
    st.subheader("📊 詳細分析 / Detailed Analysis")

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.markdown("#### 🔥 FIRE Analysis")
        st.write(f"**Grade:** {result['fire_grade']}")
        st.write(f"**Achievement:** {result['fire_percentage']:.1f}%")
        st.write(f"**Target Amount:** {format_currency(result['fire_number'])}")
        st.write(f"**Achievable:** {'✅ Yes' if result['fire_achievable'] else '❌ No'}")

    with detail_col2:
        st.markdown("#### 🏛️ Traditional Retirement")
        st.write(f"**Grade:** {result['traditional_grade']}")
        st.write(f"**Retirement Age:** {result['traditional_retirement_age']:.1f} years")

        early_ret = result.get('early_retirement_ready', 0)
        late_ret = result.get('late_retirement', 0)

        if early_ret and early_ret > 0:
            st.write(f"**Early by:** {early_ret:.1f} years 🎉")
        elif late_ret and late_ret > 0:
            st.write(f"**Late by:** {late_ret:.1f} years ⚠️")
        else:
            st.write("**Status:** On time ✅")

    # Simplified wealth timeline
    st.markdown("---")
    st.subheader("📈 資産推移 / Wealth Timeline")

    timeline_df = get_wealth_timeline(result)

    if timeline_df is not None and len(timeline_df) > 0:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=timeline_df['age'],
            y=timeline_df['wealth'],
            mode='lines+markers',
            name='Projected Wealth (予想資産)',
            line=dict(color='#1f77b4', width=4),
            marker=dict(size=10, color='#1f77b4'),
            hovertemplate='Age: %{x}<br>Wealth: ¥%{y:,.0f}<extra></extra>'
        ))

        # Add FIRE line
        if result.get('fire_number', 0) > 0:
            fire_line_value = result['fire_number']
            fig.add_hline(
                y=fire_line_value,
                line_dash="dash",
                line_color="red",
                annotation_text=f"🔥 FIRE Goal: {format_currency(fire_line_value)}"
            )

        # Add retirement line
        retirement_age = result.get('traditional_retirement_age', 65)
        if retirement_age and not pd.isna(retirement_age):
            fig.add_vline(
                x=retirement_age,
                line_dash="dot",
                line_color="green",
                annotation_text=f"🏛️ Retirement: {retirement_age:.0f}歳"
            )

        fig.update_layout(
            title="Wealth Accumulation Timeline / 資産推移予測",
            xaxis_title="Age (歳)",
            yaxis_title="Wealth (円)",
            height=500,
            yaxis=dict(tickformat=',.0f'),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Starting Wealth", format_currency(timeline_df.iloc[0]['wealth']))
        with col2:
            mid_idx = len(timeline_df) // 2
            st.metric("Mid-Point Wealth", format_currency(timeline_df.iloc[mid_idx]['wealth']))
        with col3:
            st.metric("Final Wealth", format_currency(timeline_df.iloc[-1]['wealth']))

    else:
        st.error("❌ Could not generate wealth timeline.")

    # Key insights
    st.markdown("---")
    st.subheader("💡 Key Insights")
    insights = get_status_insights(result)
    for insight in insights:
        st.markdown(f"""<div class="insight-box">{insight}</div>""", unsafe_allow_html=True)

elif 'analysis_result' in st.session_state and st.session_state.analysis_result is not None:
    st.info("📊 Your previous analysis is shown above. Adjust parameters and click 'Analyze' for new results.")
    if st.sidebar.button("🗑️ Clear Results"):
        st.session_state.analysis_completed = False
        st.session_state.analysis_result = None
        st.rerun()

else:
    # Welcome screen (simplified)
    st.markdown("""
    ### Welcome to PFM Compass Retirement Planning MVP! 👋
    
    **For internal employee testing only**
    
    This tool helps you understand your retirement readiness using:
    - 🔥 **FIRE Analysis**: Financial independence planning
    - 🏛️ **Traditional Retirement**: Japanese pension system analysis
    
    **How to use:** Fill out your profile in the sidebar and click "分析開始 / Analyze"
    
    **Data Source:** 1.38M pre-computed scenarios
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    🚀 PFM Compass MVP | AI & Data Science Team | Internal Testing Only
</div>
""", unsafe_allow_html=True)