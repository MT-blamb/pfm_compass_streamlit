import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="PFM Compass - Simple Version",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 PFM Compass - Simple Working Version")
st.markdown("### Testing with real data structure")

@st.cache_data
def load_data():
    """Load the parquet file"""
    try:
        df = pd.read_parquet('./pfm_compass_data/retirement_scenarios_FIXED_v4.parquet')
        st.success(f"✅ Loaded {len(df):,} scenarios successfully")
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

def simple_lookup(df, age_bucket, current_savings_bucket, expected_expenses_bucket,
                 gender, household_size, housing_status, income_bucket, 
                 marital_status, monthly_savings_bucket, retirement_age_bucket):
    """Simple lookup using the exact sort key format we discovered"""
    
    # Generate the sort key exactly as shown in the data
    sort_key = f"combo__{age_bucket}__{current_savings_bucket}__{expected_expenses_bucket}__{gender}__{household_size}__{housing_status}__{income_bucket}__{marital_status}__{monthly_savings_bucket}__{retirement_age_bucket}"
    
    # Find matching row
    result = df[df['sk'] == sort_key]
    
    if len(result) > 0:
        return result.iloc[0].to_dict()
    else:
        return None

def parse_timeline(timeline_data):
    """Parse the numpy array timeline data we discovered"""
    try:
        if hasattr(timeline_data, 'tolist'):
            # It's a numpy array - convert to list
            timeline_list = timeline_data.tolist()
            return pd.DataFrame(timeline_list)
        else:
            return None
    except Exception as e:
        st.error(f"Timeline parse error: {e}")
        return None

def format_currency(amount):
    """Simple currency formatting"""
    if amount >= 100_000_000:
        return f"¥{amount/100_000_000:.1f}億円"
    elif amount >= 10_000:
        return f"¥{amount/10_000:.0f}万円"
    else:
        return f"¥{amount:,.0f}"

# Load data
df = load_data()

if df is None:
    st.stop()

# Simple form using the exact bucket values we discovered
st.sidebar.header("👤 Your Profile")

age_bucket = st.sidebar.selectbox(
    "Age Bucket",
    ['20-29', '30-34', '35-39', '40-44', '45-49', '50']
)

current_savings_bucket = st.sidebar.selectbox(
    "Current Savings Bucket", 
    ['a', 'b', 'c', 'd', 'e']
)

expected_expenses_bucket = st.sidebar.selectbox(
    "Expected Expenses Bucket",
    ['a', 'b', 'c', 'd', 'e', 'f']
)

gender = st.sidebar.selectbox(
    "Gender",
    ['m', 'f']
)

household_size = st.sidebar.selectbox(
    "Household Size",
    [1, 2, 3, 4]
)

housing_status = st.sidebar.selectbox(
    "Housing Status",
    ['rent', 'own_paying', 'own_paid', 'planning']
)

income_bucket = st.sidebar.selectbox(
    "Income Bucket",
    ['a', 'b', 'c', 'd', 'e']
)

marital_status = st.sidebar.selectbox(
    "Marital Status",
    ['s', 'm']
)

monthly_savings_bucket = st.sidebar.selectbox(
    "Monthly Savings Bucket",
    ['a', 'b', 'c', 'd', 'e', 'f']
)

retirement_age_bucket = st.sidebar.selectbox(
    "Retirement Age Bucket",
    ['50-59', '60-64', '65', '70']
)

# Show the generated key for debugging
generated_key = f"combo__{age_bucket}__{current_savings_bucket}__{expected_expenses_bucket}__{gender}__{household_size}__{housing_status}__{income_bucket}__{marital_status}__{monthly_savings_bucket}__{retirement_age_bucket}"

with st.expander("🔍 Debug: Generated Key"):
    st.code(generated_key)

# Analyze button
if st.sidebar.button("🔍 Analyze", type="primary"):
    
    with st.spinner("Looking up scenario..."):
        result = simple_lookup(
            df, age_bucket, current_savings_bucket, expected_expenses_bucket,
            gender, household_size, housing_status, income_bucket,
            marital_status, monthly_savings_bucket, retirement_age_bucket
        )
    
    if result:
        st.success("✅ Found matching scenario!")
        
        # Display basic results
        st.markdown("## 📈 Your Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_color = result['status_color']
            status_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
            st.metric("Status", f"{status_emoji.get(status_color, '⚪')} {status_color.title()}")
        
        with col2:
            st.metric("FIRE Grade", result['fire_grade'])
        
        with col3:
            st.metric("Traditional Grade", result['traditional_grade'])
        
        # More details
        st.markdown("### 📊 Financial Details")
        
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.write(f"**Projected Wealth:** {format_currency(result['projected_wealth'])}")
            st.write(f"**FIRE Number:** {format_currency(result['fire_number'])}")
            st.write(f"**FIRE Achievable:** {'✅ Yes' if result['fire_achievable'] else '❌ No'}")
        
        with detail_col2:
            st.write(f"**Traditional Retirement Age:** {result['traditional_retirement_age']:.1f} years")
            st.write(f"**FIRE Percentage:** {result['fire_percentage']:.1f}%")
            
            if result.get('early_retirement_ready', 0) > 0:
                st.write(f"**Early Retirement:** {result['early_retirement_ready']:.1f} years early 🎉")
            elif result.get('late_retirement', 0) > 0:
                st.write(f"**Late Retirement:** {result['late_retirement']:.1f} years late ⚠️")
        
        # Timeline chart
        st.markdown("### 📈 Wealth Timeline")
        
        timeline_df = parse_timeline(result['wealth_timeline'])
        
        if timeline_df is not None and len(timeline_df) > 0:
            
            # Create simple line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=timeline_df['age'],
                y=timeline_df['wealth'],
                mode='lines+markers',
                name='Wealth Projection',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8)
            ))
            
            # Add FIRE goal line
            if result['fire_number'] > 0:
                fig.add_hline(
                    y=result['fire_number'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"FIRE Goal: {format_currency(result['fire_number'])}"
                )
            
            # Add retirement age line
            retirement_age = result['traditional_retirement_age']
            if retirement_age and not pd.isna(retirement_age):
                fig.add_vline(
                    x=retirement_age,
                    line_dash="dot", 
                    line_color="green",
                    annotation_text=f"Retirement: {retirement_age:.0f}"
                )
            
            fig.update_layout(
                title="Wealth Growth Over Time",
                xaxis_title="Age",
                yaxis_title="Wealth (¥)",
                height=400,
                yaxis=dict(tickformat=',.0f')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show timeline data
            with st.expander("📊 Timeline Data Points"):
                st.dataframe(timeline_df)
        
        else:
            st.error("❌ Could not parse timeline data")
        
        # Raw result for debugging
        with st.expander("🔧 Raw Result Data"):
            debug_result = {k: v for k, v in result.items() if k != 'wealth_timeline'}
            st.json(debug_result)
    
    else:
        st.error("❌ No matching scenario found")
        st.info("💡 Try different parameter combinations")

else:
    # Welcome message
    st.markdown("""
    ### Welcome! 👋
    
    This is a simplified version that works with the real data structure we discovered.
    
    **What we learned:**
    - ✅ Timeline data is stored as numpy arrays
    - ✅ Keys use the exact format: `combo__age__savings__expenses...`
    - ✅ Bucket values are simple: a,b,c,d,e,f and age ranges
    
    **Instructions:**
    1. Select your parameters in the sidebar
    2. Click "Analyze" 
    3. See your wealth timeline chart!
    """)
    
    # Show a sample from each status
    st.markdown("### 📊 Sample Data")
    
    sample_data = []
    for color in ['green', 'yellow', 'red']:
        color_sample = df[df['status_color'] == color].sample(1)
        sample_data.append(color_sample)
    
    sample_df = pd.concat(sample_data)
    
    display_cols = ['status_color', 'age_bucket', 'income_bucket', 'fire_grade', 
                   'traditional_grade', 'projected_wealth']
    st.dataframe(sample_df[display_cols])

st.markdown("---")
st.markdown("🚀 **Simple Version** - Testing real data structure")