import pandas as pd
import json

# Load the data
df = pd.read_parquet('./data/retirement_scenarios.parquet')

print("🔍 Investigating wealth_timeline column...")
print(f"Total rows: {len(df)}")

# Check if wealth_timeline column exists
if 'wealth_timeline' in df.columns:
    print("✅ wealth_timeline column found")
    
    # Check data types and null values
    print(f"Data type: {df['wealth_timeline'].dtype}")
    print(f"Null values: {df['wealth_timeline'].isnull().sum()}")
    print(f"Non-null values: {(~df['wealth_timeline'].isnull()).sum()}")
    
    # Look at some sample values
    print("\n📊 Sample wealth_timeline values:")
    non_null_samples = df[df['wealth_timeline'].notnull()]['wealth_timeline'].head(5)
    
    for i, sample in enumerate(non_null_samples):
        print(f"\nSample {i+1}:")
        print(f"Type: {type(sample)}")
        print(f"Value: {str(sample)[:200]}...")  # First 200 chars
        
        # Try to parse it
        try:
            if isinstance(sample, str):
                parsed = json.loads(sample)
                print(f"✅ JSON parsed successfully: {len(parsed)} items")
                if len(parsed) > 0:
                    print(f"First item: {parsed[0]}")
            else:
                print(f"⚠️ Not a string: {type(sample)}")
        except Exception as e:
            print(f"❌ JSON parsing failed: {e}")
    
    # Test with a specific scenario that should have good data
    print("\n🎯 Testing specific scenario...")
    test_scenario = df[
        (df['age_bucket'] == '30-34') &
        (df['income_bucket'] == 'd') &
        (df['status_color'] == 'green')
    ].head(1)
    
    if len(test_scenario) > 0:
        timeline_val = test_scenario['wealth_timeline'].iloc[0]
        print(f"Test scenario timeline type: {type(timeline_val)}")
        print(f"Test scenario timeline value: {str(timeline_val)[:300]}")
        
        # Try parsing
        try:
            if pd.notna(timeline_val) and timeline_val != '':
                parsed = json.loads(str(timeline_val))
                print(f"✅ Test scenario parsed: {len(parsed)} data points")
                print(f"Sample data points: {parsed[:3]}")
            else:
                print("❌ Test scenario has no timeline data")
        except Exception as e:
            print(f"❌ Test scenario parsing failed: {e}")

else:
    print("❌ wealth_timeline column not found!")
    print("Available columns:")
    for col in df.columns:
        print(f"  - {col}")

# Check a broader sample
print(f"\n📈 Overall timeline data availability:")
if 'wealth_timeline' in df.columns:
    has_data = df['wealth_timeline'].notnull() & (df['wealth_timeline'] != '') & (df['wealth_timeline'] != 'null')
    print(f"Rows with timeline data: {has_data.sum()} / {len(df)} ({has_data.sum()/len(df)*100:.1f}%)")
    
    # Check by status
    for status in ['green', 'yellow', 'red']:
        status_df = df[df['status_color'] == status]
        status_has_data = status_df['wealth_timeline'].notnull() & (status_df['wealth_timeline'] != '') & (status_df['wealth_timeline'] != 'null')
        print(f"{status} status with timeline: {status_has_data.sum()} / {len(status_df)} ({status_has_data.sum()/len(status_df)*100:.1f}%)")