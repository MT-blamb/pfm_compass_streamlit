import pandas as pd
import streamlit as st

def test_data_loading():
    """Test if FIXED data loads properly for Streamlit"""
    try:
        df = pd.read_parquet('./pfm_compass_data/retirement_scenarios_FIXED_v4.parquet')
        
        st.write("🎯 FIXED Retirement Data Test")
        st.write(f"✅ Data loaded: {len(df):,} rows")
        
        # Test key lookups that Streamlit app will use
        st.write("🔍 Testing key lookups:")
        
        # Sample lookup scenario
        test_scenario = df[
            (df['age_bucket'] == '30-34') &
            (df['income_bucket'] == 'c') &
            (df['current_savings_bucket'] == 'b') &
            (df['monthly_savings_bucket'] == 'c') &
            (df['retirement_age_bucket'] == '65') &
            (df['expected_expenses_bucket'] == 'c') &
            (df['household_size'] == 2) &
            (df['housing_status'] == 'rent') &
            (df['gender'] == 'm') &
            (df['marital_status'] == 'm')
        ]
        
        if len(test_scenario) > 0:
            result = test_scenario.iloc[0]
            st.write(f"✅ Sample lookup successful:")
            st.write(f"  Traditional grade: {result['traditional_grade']}")
            st.write(f"  Status color: {result['status_color']}")
            st.write(f"  Traditional number: ¥{result['traditional_number']:,}")
            st.write(f"  Projected wealth: ¥{result['projected_wealth']:,}")
        else:
            st.write("❌ Sample lookup failed - no matching records")
            
        return True
        
    except Exception as e:
        st.write(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_data_loading()
