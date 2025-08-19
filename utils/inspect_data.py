import pandas as pd
import streamlit as st
import json

st.set_page_config(
    page_title="PFM Compass - Data Inspector",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 PFM Compass - Data Inspector")
st.markdown("### Understanding the retirement scenarios parquet file")

@st.cache_data
def load_sample_data():
    """Load a small sample of data for inspection"""
    try:
        # Load the full dataset
        df = pd.read_parquet('./data/retirement_scenarios.parquet')
        
        st.write(f"📊 **Total rows:** {len(df):,}")
        st.write(f"📊 **Total columns:** {len(df.columns)}")
        
        # Get samples from each status color
        samples = []
        for color in ['green', 'yellow', 'red']:
            color_df = df[df['status_color'] == color]
            if len(color_df) > 0:
                sample = color_df.sample(n=min(2, len(color_df)), random_state=42)
                samples.append(sample)
        
        sample_df = pd.concat(samples, ignore_index=True)
        
        return df, sample_df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

df, sample_df = load_sample_data()

if df is not None:
    
    # Column information
    st.markdown("---")
    st.subheader("📋 Column Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**All Columns:**")
        for i, col in enumerate(df.columns, 1):
            st.write(f"{i:2d}. {col}")
    
    with col2:
        st.markdown("**Column Data Types:**")
        dtypes_df = pd.DataFrame({
            'Column': df.dtypes.index,
            'Type': df.dtypes.values,
            'Non-Null': [df[col].notna().sum() for col in df.columns],
            'Null %': [f"{(df[col].isna().sum() / len(df) * 100):.1f}%" for col in df.columns]
        })
        st.dataframe(dtypes_df, height=400)
    
    # Sample data inspection
    st.markdown("---")
    st.subheader("🎯 Sample Data (2 from each status color)")
    
    if sample_df is not None:
        st.write(f"Sample size: {len(sample_df)} rows")
        
        # Show key columns first
        key_cols = ['status_color', 'age_bucket', 'income_bucket', 'current_savings_bucket', 
                   'monthly_savings_bucket', 'fire_grade', 'traditional_grade', 
                   'fire_achievable', 'projected_wealth']
        
        available_key_cols = [col for col in key_cols if col in sample_df.columns]
        
        st.markdown("**Key Columns:**")
        st.dataframe(sample_df[available_key_cols])
        
        # Full sample data
        with st.expander("🔍 Full Sample Data (all columns)"):
            st.dataframe(sample_df)
    
    # Timeline data inspection
    st.markdown("---")
    st.subheader("📈 Wealth Timeline Investigation")
    
    if 'wealth_timeline' in df.columns:
        timeline_col = df['wealth_timeline']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Timeline column stats:**")
            st.write(f"- Total rows: {len(timeline_col)}")
            st.write(f"- Non-null: {timeline_col.notna().sum()}")
            st.write(f"- Null: {timeline_col.isna().sum()}")
            st.write(f"- Data type: {timeline_col.dtype}")
        
        with col2:
            st.write(f"**Timeline value types:**")
            non_null_timelines = timeline_col.dropna()
            if len(non_null_timelines) > 0:
                sample_timeline = non_null_timelines.iloc[0]
                st.write(f"- Sample type: {type(sample_timeline)}")
                st.write(f"- Sample length: {len(str(sample_timeline))}")
        
        # Show sample timeline values
        st.markdown("**Sample Timeline Values:**")
        
        for i, (idx, row) in enumerate(sample_df.iterrows()):
            if i >= 3:  # Show max 3 samples
                break
                
            timeline_val = row.get('wealth_timeline', None)
            status = row.get('status_color', 'unknown')
            
            st.write(f"**Sample {i+1} ({status} status):**")
            
            # Handle numpy array or other types
            try:
                if timeline_val is None:
                    st.write("- No timeline data (None)")
                elif hasattr(timeline_val, '__len__') and len(timeline_val) == 0:
                    st.write("- Empty timeline data")
                else:
                    st.write(f"- Type: {type(timeline_val)}")
                    st.write(f"- Shape/Length: {getattr(timeline_val, 'shape', len(str(timeline_val))) if hasattr(timeline_val, 'shape') else 'N/A'}")
                    
                    # Convert to string for display
                    timeline_str = str(timeline_val)
                    st.write(f"- Raw value: {timeline_str[:200]}...")
                    
                    # Try different parsing approaches
                    if hasattr(timeline_val, 'tolist'):
                        # It's a numpy array
                        try:
                            timeline_list = timeline_val.tolist()
                            st.write(f"- ✅ Numpy array converted: {len(timeline_list)} items")
                            if len(timeline_list) > 0:
                                st.write(f"- First item: {timeline_list[0]}")
                                st.write(f"- Last item: {timeline_list[-1]}")
                                
                                # Check if items are dictionaries with age/wealth/year
                                if isinstance(timeline_list[0], dict):
                                    keys = list(timeline_list[0].keys())
                                    st.write(f"- Item keys: {keys}")
                        except Exception as e:
                            st.write(f"- ❌ Numpy conversion error: {e}")
                    
                    elif isinstance(timeline_val, str):
                        try:
                            parsed = json.loads(timeline_val)
                            st.write(f"- ✅ JSON parsed successfully: {len(parsed)} items")
                            if len(parsed) > 0:
                                st.write(f"- First item: {parsed[0]}")
                                st.write(f"- Last item: {parsed[-1]}")
                        except Exception as e:
                            st.write(f"- ❌ JSON parse error: {e}")
                    
                    else:
                        st.write(f"- Unknown format, direct value: {timeline_val}")
            
            except Exception as e:
                st.write(f"- ❌ General error: {e}")
            
            st.write("")
    
    else:
        st.error("❌ No 'wealth_timeline' column found in data!")
    
    # Timeline data deep dive
    st.markdown("---")
    st.subheader("🔬 Timeline Deep Dive")
    
    if 'wealth_timeline' in sample_df.columns and len(sample_df) > 0:
        st.write("**Let's extract one complete timeline example:**")
        
        first_timeline = sample_df.iloc[0]['wealth_timeline']
        first_status = sample_df.iloc[0]['status_color']
        
        try:
            if hasattr(first_timeline, 'tolist'):
                timeline_data = first_timeline.tolist()
                
                st.write(f"**Complete timeline ({first_status} status):**")
                st.write(f"- Number of data points: {len(timeline_data)}")
                
                # Display as formatted JSON
                st.json(timeline_data)
                
                # Create a simple chart if the data looks right
                if len(timeline_data) > 0 and isinstance(timeline_data[0], dict):
                    try:
                        import plotly.express as px
                        timeline_df = pd.DataFrame(timeline_data)
                        
                        if 'age' in timeline_df.columns and 'wealth' in timeline_df.columns:
                            fig = px.line(timeline_df, x='age', y='wealth', 
                                        title=f"Sample Wealth Timeline ({first_status} status)")
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.write("⚠️ Timeline data doesn't have expected 'age' and 'wealth' columns")
                            st.write(f"Available columns: {list(timeline_df.columns)}")
                            
                    except Exception as e:
                        st.write(f"Chart creation error: {e}")
                        
        except Exception as e:
            st.write(f"Timeline extraction error: {e}")
    
    # Timeline data deep dive
    st.markdown("---")
    st.subheader("🔬 Timeline Deep Dive")
    
    if 'wealth_timeline' in sample_df.columns and len(sample_df) > 0:
        st.write("**Let's extract one complete timeline example:**")
        
        first_timeline = sample_df.iloc[0]['wealth_timeline']
        first_status = sample_df.iloc[0]['status_color']
        
        try:
            if hasattr(first_timeline, 'tolist'):
                timeline_data = first_timeline.tolist()
                
                st.write(f"**Complete timeline ({first_status} status):**")
                st.write(f"- Number of data points: {len(timeline_data)}")
                
                # Display as formatted JSON
                st.json(timeline_data)
                
                # Create a simple chart if the data looks right
                if len(timeline_data) > 0 and isinstance(timeline_data[0], dict):
                    try:
                        import plotly.express as px
                        timeline_df = pd.DataFrame(timeline_data)
                        
                        if 'age' in timeline_df.columns and 'wealth' in timeline_df.columns:
                            fig = px.line(timeline_df, x='age', y='wealth', 
                                        title=f"Sample Wealth Timeline ({first_status} status)")
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.write("⚠️ Timeline data doesn't have expected 'age' and 'wealth' columns")
                            st.write(f"Available columns: {list(timeline_df.columns)}")
                            
                    except Exception as e:
                        st.write(f"Chart creation error: {e}")
                        
        except Exception as e:
            st.write(f"Timeline extraction error: {e}")
    st.markdown("---")
    st.subheader("🗂️ Bucket Values Analysis")
    
    bucket_cols = [col for col in df.columns if 'bucket' in col.lower()]
    
    if bucket_cols:
        st.write("**Unique values in bucket columns:**")
        
        for col in bucket_cols:
            unique_vals = df[col].unique()
            st.write(f"**{col}:** {sorted([str(v) for v in unique_vals if pd.notna(v)])}")
    
    # Key generation test
    st.markdown("---")
    st.subheader("🔑 Key Generation Test")
    
    if sample_df is not None and len(sample_df) > 0:
        st.write("**Testing DynamoDB key generation with sample data:**")
        
        first_row = sample_df.iloc[0]
        
        # Extract key components
        key_components = {
            'age_bucket': first_row.get('age_bucket', '30-34'),
            'current_savings_bucket': first_row.get('current_savings_bucket', 'b'),
            'expected_expenses_bucket': first_row.get('expected_expenses_bucket', 'c'),
            'gender': first_row.get('gender', 'm'),
            'household_size': first_row.get('household_size', 2),
            'housing_status': first_row.get('housing_status', 'rent'),
            'income_bucket': first_row.get('income_bucket', 'c'),
            'marital_status': first_row.get('marital_status', 's'),
            'monthly_savings_bucket': first_row.get('monthly_savings_bucket', 'b'),
            'retirement_age_bucket': first_row.get('retirement_age_bucket', '65')
        }
        
        st.write("**Key components from sample:**")
        for key, value in key_components.items():
            st.write(f"- {key}: {value}")
        
        # Generate the key
        sort_key = f"combo__{key_components['age_bucket']}__{key_components['current_savings_bucket']}__{key_components['expected_expenses_bucket']}__{key_components['gender']}__{key_components['household_size']}__{key_components['housing_status']}__{key_components['income_bucket']}__{key_components['marital_status']}__{key_components['monthly_savings_bucket']}__{key_components['retirement_age_bucket']}"
        
        st.write(f"**Generated sort key:**")
        st.code(sort_key)
        
        # Check if SK column exists
        if 'sk' in df.columns:
            actual_sk = first_row.get('sk', 'N/A')
            st.write(f"**Actual SK in data:** {actual_sk}")
            st.write(f"**Match:** {'✅ Yes' if sort_key == actual_sk else '❌ No'}")

else:
    st.error("❌ Could not load data. Please check that './data/retirement_scenarios.parquet' exists.")

# Raw data download
if df is not None:
    st.markdown("---")
    st.subheader("💾 Data Export")
    
    # Export sample as CSV for inspection
    if sample_df is not None:
        csv_data = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample as CSV",
            data=csv_data,
            file_name="retirement_scenarios_sample.csv",
            mime="text/csv"
        )
    
    # Show memory usage
    memory_usage = df.memory_usage(deep=True).sum() / 1024**2
    st.write(f"**Memory usage:** {memory_usage:.1f} MB")
    
    # File size
    import os
    if os.path.exists('./data/retirement_scenarios.parquet'):
        file_size = os.path.getsize('./data/retirement_scenarios.parquet') / 1024**2
        st.write(f"**File size:** {file_size:.1f} MB")