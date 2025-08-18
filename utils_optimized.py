import pandas as pd
import streamlit as st
import json
import numpy as np

# ---------- Optimized Data Loading ----------

@st.cache_data(show_spinner=False, ttl=3600)  # Cache for 1 hour
def load_data():
    """Load retirement scenarios with performance optimizations"""
    try:
        # Load only essential columns
        df = pd.read_parquet(
            './data/retirement_scenarios.parquet',
            columns=[
                'pk', 'sk', 'age_bucket', 'age_midpoint', 'current_savings_bucket',
                'current_savings_midpoint', 'expected_expenses_bucket', 'expected_expenses_midpoint',
                'gender', 'household_size', 'housing_status', 'income_bucket', 'income_midpoint',
                'marital_status', 'monthly_savings_bucket', 'monthly_savings_midpoint',
                'retirement_age_bucket', 'retirement_age_midpoint', 'fire_achievable',
                'fire_percentage', 'fire_grade', 'projected_wealth', 'fire_number',
                'wealth_timeline', 'traditional_retirement_age', 'traditional_grade',
                'early_retirement_ready', 'late_retirement', 'status_color'
            ]
        )
        
        # Simple dtype optimizations (avoid categorical for now)
        numeric_cols = ['household_size', 'fire_percentage', 'projected_wealth', 'fire_number',
                       'traditional_retirement_age', 'early_retirement_ready', 'late_retirement']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert boolean column
        if 'fire_achievable' in df.columns:
            df['fire_achievable'] = df['fire_achievable'].astype('bool')
        
        # Reset index for faster operations
        df = df.reset_index(drop=True)
        
        print(f"✅ Loaded {len(df):,} scenarios")
        print(f"📊 Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# ---------- Ultra-Fast Lookup ----------

@st.cache_data(show_spinner=False)
def create_lookup_index(df):
    """Create a fast lookup index for scenarios"""
    if df is None:
        return None
    
    # Create a compound key for ultra-fast lookups
    # Handle categorical columns properly
    def safe_str_convert(series):
        if pd.api.types.is_categorical_dtype(series):
            # Convert categorical to string, handling NaNs
            return series.astype(str).fillna('missing')
        else:
            return series.astype(str).fillna('')
    
    df['lookup_key'] = (
        safe_str_convert(df['age_bucket']) + '|' +
        safe_str_convert(df['current_savings_bucket']) + '|' +
        safe_str_convert(df.get('expected_expenses_bucket', pd.Series([''] * len(df)))) + '|' +
        safe_str_convert(df['gender']) + '|' +
        df['household_size'].astype(str) + '|' +
        safe_str_convert(df['housing_status']) + '|' +
        safe_str_convert(df['income_bucket']) + '|' +
        safe_str_convert(df['marital_status']) + '|' +
        safe_str_convert(df['monthly_savings_bucket']) + '|' +
        safe_str_convert(df['retirement_age_bucket'])
    )
    
    # Create dictionary for O(1) lookup
    lookup_dict = {}
    for idx, row in df.iterrows():
        key = row['lookup_key']
        if key not in lookup_dict:
            lookup_dict[key] = row.to_dict()
    
    print(f"✅ Created lookup index with {len(lookup_dict):,} unique scenarios")
    return lookup_dict

def fast_lookup_scenario(lookup_dict, age_bucket, current_savings_bucket, expected_expenses_bucket,
                        gender, household_size, housing_status, income_bucket, 
                        marital_status, monthly_savings_bucket, retirement_age_bucket):
    """Ultra-fast scenario lookup using pre-built index"""
    if lookup_dict is None:
        return None
    
    # Create the same compound key - handle missing expected_expenses_bucket
    expected_bucket_str = str(expected_expenses_bucket) if expected_expenses_bucket else 'missing'
    
    lookup_key = (
        f"{age_bucket}|{current_savings_bucket}|{expected_bucket_str}|"
        f"{gender}|{household_size}|{housing_status}|{income_bucket}|"
        f"{marital_status}|{monthly_savings_bucket}|{retirement_age_bucket}"
    )
    
    result = lookup_dict.get(lookup_key, None)
    
    # If not found with expected_expenses_bucket, try with empty string fallback
    if result is None and expected_bucket_str != '':
        fallback_key = (
            f"{age_bucket}|{current_savings_bucket}||"
            f"{gender}|{household_size}|{housing_status}|{income_bucket}|"
            f"{marital_status}|{monthly_savings_bucket}|{retirement_age_bucket}"
        )
        result = lookup_dict.get(fallback_key, None)
    
    return result

# ---------- Simplified Timeline Generation ----------

def generate_simple_timeline(result):
    """Generate a simple, fast wealth timeline"""
    try:
        # Get basic parameters with sensible defaults
        current_age = result.get('age_midpoint', 32)
        if pd.isna(current_age) or current_age == 0:
            age_bucket = result.get('age_bucket', '30-34')
            age_map = {'20-29': 25, '30-34': 32, '35-39': 37, '40-44': 42, '45-49': 47, '50': 55}
            current_age = age_map.get(age_bucket, 32)
        
        current_savings = result.get('current_savings_midpoint', 2500000)
        if pd.isna(current_savings) or current_savings == 0:
            savings_bucket = result.get('current_savings_bucket', 'b')
            savings_map = {'a': 500000, 'b': 2500000, 'c': 12500000, 'd': 35000000, 'e': 75000000}
            current_savings = savings_map.get(savings_bucket, 2500000)
        
        monthly_savings = result.get('monthly_savings_midpoint', 150000)
        if pd.isna(monthly_savings) or monthly_savings == 0:
            monthly_bucket = result.get('monthly_savings_bucket', 'b')
            monthly_map = {'a': 50000, 'b': 150000, 'c': 250000, 'd': 400000, 'e': 650000, 'f': 900000}
            monthly_savings = monthly_map.get(monthly_bucket, 150000)
        
        retirement_age = result.get('traditional_retirement_age', 65)
        if pd.isna(retirement_age):
            retirement_age = 65
        
        # Simple calculation - just 5 key points
        annual_savings = monthly_savings * 12
        annual_return = 0.07
        
        timeline_points = []
        wealth = current_savings
        
        # Calculate wealth at key ages
        ages = [
            current_age,
            min(current_age + 10, retirement_age),
            retirement_age,
            retirement_age + 5,
            min(retirement_age + 10, 80)
        ]
        
        for target_age in ages:
            years_from_now = target_age - current_age
            
            if target_age <= retirement_age:
                # Working years: compound with contributions
                wealth_at_age = current_savings
                for year in range(int(years_from_now)):
                    wealth_at_age = wealth_at_age * (1 + annual_return) + annual_savings
            else:
                # Retirement years: compound without contributions, with withdrawals
                wealth_at_retirement = current_savings
                years_to_retirement = retirement_age - current_age
                for year in range(int(years_to_retirement)):
                    wealth_at_retirement = wealth_at_retirement * (1 + annual_return) + annual_savings
                
                wealth_at_age = wealth_at_retirement
                years_in_retirement = target_age - retirement_age
                for year in range(int(years_in_retirement)):
                    withdrawal = wealth_at_age * 0.04  # 4% withdrawal rate
                    wealth_at_age = (wealth_at_age - withdrawal) * (1 + annual_return)
                    wealth_at_age = max(0, wealth_at_age)
            
            timeline_points.append({
                'age': int(target_age),
                'wealth': int(max(0, wealth_at_age)),
                'year': int(2024 + (target_age - current_age))
            })
        
        return pd.DataFrame(timeline_points)
        
    except Exception as e:
        print(f"Timeline generation error: {e}")
        return None

# ---------- Other optimized functions (keeping the same interface) ----------

def format_currency(amount):
    """Format currency in Japanese Yen with appropriate suffixes"""
    if pd.isna(amount) or amount == 0:
        return "¥0"
    if amount >= 100_000_000:
        return f"¥{amount/100_000_000:.1f}億円"
    elif amount >= 10_000:
        return f"¥{amount/10_000:.0f}万円"
    else:
        return f"¥{amount:,.0f}"

def get_bucket_mappings():
    """Create mapping dictionaries for all bucket types (cached)"""
    return {
        'age_bucket': {
            "20-29": "20代 (20-29歳)",
            "30-34": "30代前半 (30-34歳)",
            "35-39": "30代後半 (35-39歳)",
            "40-44": "40代前半 (40-44歳)",
            "45-49": "40代後半 (45-49歳)",
            "50": "50代以上 (50歳〜)"
        },
        'income_bucket': {
            "a": "〜300万円 (Under ¥3M)",
            "b": "300-600万円 (¥3M-6M)",
            "c": "600-900万円 (¥6M-9M)",
            "d": "900-1200万円 (¥9M-12M)",
            "e": "1200万円〜 (Over ¥12M)"
        },
        'current_savings_bucket': {
            "a": "〜100万円 (Under ¥1M)",
            "b": "100-500万円 (¥1M-5M)",
            "c": "500-2000万円 (¥5M-20M)",
            "d": "2000-5000万円 (¥20M-50M)",
            "e": "5000万円〜 (Over ¥50M)"
        },
        'monthly_savings_bucket': {
            "a": "〜10万円 (Under ¥100K)",
            "b": "10-20万円 (¥100K-200K)",
            "c": "20-30万円 (¥200K-300K)",
            "d": "30-50万円 (¥300K-500K)",
            "e": "50-80万円 (¥500K-800K)",
            "f": "80万円〜 (Over ¥800K)"
        },
        'expected_expenses_bucket': {
            "a": "〜5万円 (Minimal)",
            "b": "5-10万円 (Basic)",
            "c": "10-15万円 (Standard)",
            "d": "15-20万円 (Comfortable)",
            "e": "20-30万円 (Premium)",
            "f": "30万円〜 (Luxury)"
        },
        'retirement_age_bucket': {
            "50-59": "50代 (Early retirement)",
            "60-64": "60代前半 (Early 60s)",
            "65": "65歳 (Standard retirement)",
            "70": "70歳 (Late retirement)"
        },
        'housing_status': {
            "rent": "賃貸 (Renting)",
            "own_paying": "ローン返済中 (Paying mortgage)",
            "own_paid": "持ち家完済 (Owned - paid off)",
            "planning": "購入予定 (Planning to buy)"
        }
    }

def get_status_insights(result):
    """Generate personalized insights (optimized)"""
    insights = []
    
    color = result.get('status_color', 'yellow')
    if color == 'green':
        insights.append("🎉 Great job! Your retirement planning is on track.")
        early_ret = result.get('early_retirement_ready', 0)
        if early_ret and early_ret > 5:
            insights.append(f"🌟 Excellent! You could retire {early_ret:.1f} years early.")
    elif color == 'yellow':
        insights.append("⚠️ Your plan needs some adjustments. Consider increasing savings or extending timeline.")
        late_ret = result.get('late_retirement', 0)
        if late_ret and late_ret > 0:
            insights.append(f"⏰ Current plan might delay retirement by {late_ret:.1f} years.")
    else:
        insights.append("🚨 Your current plan needs significant changes to meet retirement goals.")
        late_ret = result.get('late_retirement', 0)
        if late_ret and late_ret > 0:
            insights.append(f"📈 Consider increasing savings or working {late_ret:.1f} years longer.")
    
    # FIRE insights
    fire_achievable = result.get('fire_achievable', False)
    fire_percentage = result.get('fire_percentage', 0) or 0
    
    if fire_achievable:
        insights.append(f"🔥 FIRE achievable! You're {fire_percentage:.1f}% ready for financial independence.")
    else:
        gap = 100 - fire_percentage
        if gap < 20:
            insights.append(f"🎯 Almost there! You need {gap:.1f}% more to reach FIRE.")
        else:
            insights.append("🎯 To reach FIRE, focus on increasing savings or reducing expenses.")
    
    # Grade insights
    fire_grade = result.get('fire_grade', '')
    traditional_grade = result.get('traditional_grade', '')
    if fire_grade == 'A+' and traditional_grade == 'A+':
        insights.append("🏆 Perfect score! You're a retirement planning champion.")
    elif fire_grade in ['A+', 'A'] or traditional_grade in ['A+', 'A']:
        insights.append("🌟 Strong performance in retirement planning!")
    
    return insights

def get_wealth_timeline(result):
    """Get wealth timeline - simplified for speed"""
    # Skip complex parsing, just generate simple timeline
    return generate_simple_timeline(result)