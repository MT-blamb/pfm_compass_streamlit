import pandas as pd
import glob
import os

print("🔍 Looking for FIXED retirement data parquet files...")
parquet_files = glob.glob('./pfm_compass_data/raw_parquet/**/*.parquet', recursive=True)
print(f"Found {len(parquet_files)} parquet files")

if parquet_files:
    print("📚 Reading and merging FIXED parquet files...")
    df_list = []
    for i, file in enumerate(parquet_files):
        print(f"  Reading {i+1}/{len(parquet_files)}: {file}")
        try:
            df = pd.read_parquet(file)
            df_list.append(df)
        except Exception as e:
            print(f"    ❌ Error reading {file}: {e}")
    
    if df_list:
        print("🔗 Concatenating all dataframes...")
        merged_df = pd.concat(df_list, ignore_index=True)
        
        print(f"✅ Merged FIXED data: {len(merged_df):,} rows, {len(merged_df.columns)} columns")
        
        # Save merged data
        output_file = './pfm_compass_data/retirement_scenarios_FIXED_v4.parquet'
        print(f"💾 Saving to: {output_file}")
        merged_df.to_parquet(output_file, index=False)
        
        print("🎯 FIXED retirement data ready for Streamlit app!")
        
        # Quick validation
        print(f"\n🔍 Quick validation:")
        print(f"  Status colors: {merged_df['status_color'].value_counts().to_dict()}")
        print(f"  Traditional grades: {merged_df['traditional_grade'].value_counts().to_dict()}")
        print(f"  Expected total: 1,382,400 records")
        print(f"  Actual total: {len(merged_df):,} records")
        print(f"  Match: {'✅' if len(merged_df) == 1382400 else '❌'}")
        
    else:
        print("❌ No valid dataframes to merge")
else:
    print("❌ No parquet files found")
