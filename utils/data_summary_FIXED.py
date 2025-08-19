import pandas as pd
import json

print("🎯 Loading FIXED retirement scenarios data...")
try:
    df = pd.read_parquet('./pfm_compass_data/retirement_scenarios_FIXED_v4.parquet')
    print(f"✅ FIXED Data loaded: {len(df):,} rows, {len(df.columns)} columns")
    
    # Validate this is the FIXED version
    print(f"\n🔍 FIXED Version Validation:")
    
    # Check for realistic expense ranges (key indicator of fix)
    expense_samples = df['expected_expenses_midpoint'].value_counts().head()
    print(f"  Expense midpoints (top 5): {expense_samples.to_dict()}")
    
    # Check pension eligibility logic
    pension_age_retirements = len(df[df['retirement_age_midpoint'] >= 65])
    zero_traditional = len(df[(df['retirement_age_midpoint'] >= 65) & (df['traditional_number'] == 0)])
    print(f"  Pension-age retirements: {pension_age_retirements:,}")
    print(f"  Zero traditional savings needed: {zero_traditional:,}")
    print(f"  Pension coverage rate: {zero_traditional/pension_age_retirements*100:.1f}%")
    
    # Distribution analysis
    print(f"\n📊 FIXED Data Distribution:")
    print(f"  Status colors: {df['status_color'].value_counts().to_dict()}")
    print(f"  Fire grades: {df['fire_grade'].value_counts().to_dict()}")
    print(f"  Traditional grades: {df['traditional_grade'].value_counts().to_dict()}")
    
    # Calculate percentages
    total = len(df)
    green_pct = df['status_color'].value_counts().get('green', 0) / total * 100
    red_pct = df['status_color'].value_counts().get('red', 0) / total * 100
    
    print(f"\n🎯 Key Metrics:")
    print(f"  Green (success): {green_pct:.1f}%")
    print(f"  Red (failure): {red_pct:.1f}%")
    print(f"  Expected: ~84% green, ~7% red (from validation)")
    
    # Demographics
    print(f"\n👥 Demographics Distribution:")
    print(f"  Age buckets: {df['age_bucket'].value_counts().to_dict()}")
    print(f"  Income buckets: {df['income_bucket'].value_counts().to_dict()}")
    print(f"  Savings buckets: {df['monthly_savings_bucket'].value_counts().to_dict()}")
    print(f"  Gender: {df['gender'].value_counts().to_dict()}")
    
    # Sample scenarios
    print(f"\n🔬 Sample FIXED Scenarios:")
    sample = df.sample(3)
    for i, row in sample.iterrows():
        print(f"  Sample {list(sample.index).index(i)+1}:")
        print(f"    Age {row['age_midpoint']}, Income ¥{row['income_midpoint']:,}, Retire at {row['retirement_age_midpoint']}")
        print(f"    Monthly expenses: ¥{row['expected_expenses_midpoint']:,}")
        print(f"    Traditional number: ¥{row['traditional_number']:,}")
        print(f"    Grade: {row['traditional_grade']}, Status: {row['status_color']}")
    
    print(f"\n🚀 FIXED retirement data ready for Streamlit app testing!")
    
except FileNotFoundError:
    print("❌ FIXED retirement data file not found. Run merge_parquet.py first.")
except Exception as e:
    print(f"❌ Error loading data: {e}")
