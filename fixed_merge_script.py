#!/usr/bin/env python3
import pandas as pd
import glob
import os
import re

print("🔍 Looking for FIXED retirement data parquet files...")
parquet_files = glob.glob('./pfm_compass_data/raw_parquet/**/*.parquet', recursive=True)
print(f"Found {len(parquet_files)} parquet files")

if parquet_files:
    print("📚 Reading and merging FIXED parquet files with partition reconstruction...")
    df_list = []
    
    for i, file in enumerate(parquet_files):
        print(f"  Reading {i+1}/{len(parquet_files)}: {file}")
        try:
            # Read the parquet file
            df = pd.read_parquet(file)
            
            # Extract partition information from file path
            # Expected structure: .../status_color=green/execution_date=2024-08-18/file.parquet
            path_parts = file.split('/')
            
            # Initialize partition values
            status_color = None
            execution_date = None
            
            # Look for partition directories in the path
            for part in path_parts:
                if part.startswith('status_color='):
                    status_color = part.split('=')[1]
                elif part.startswith('execution_date='):
                    execution_date = part.split('=')[1]
            
            # Add partition columns back to dataframe
            if status_color:
                df['status_color'] = status_color
            if execution_date:
                df['execution_date'] = execution_date
            
            df_list.append(df)
            
            # Show progress for first few files
            if i < 5:
                print(f"    📊 Columns: {len(df.columns)}, Rows: {len(df):,}")
                if status_color:
                    print(f"    🎨 Status color: {status_color}")
                if execution_date:
                    print(f"    📅 Execution date: {execution_date}")
            
        except Exception as e:
            print(f"    ❌ Error reading {file}: {e}")
    
    if df_list:
        print("🔗 Concatenating all dataframes...")
        merged_df = pd.concat(df_list, ignore_index=True)
        
        print(f"✅ Merged FIXED data: {len(merged_df):,} rows, {len(merged_df.columns)} columns")
        
        # Show all columns to verify we have status_color
        print(f"📋 Available columns: {list(merged_df.columns)}")
        
        # Save merged data
        output_file = './pfm_compass_data/retirement_scenarios_FIXED_v4.parquet'
        print(f"💾 Saving to: {output_file}")
        merged_df.to_parquet(output_file, index=False)
        
        print("🎯 FIXED retirement data ready for Streamlit app!")
        
        # Quick validation (now should work)
        print(f"\n🔍 Quick validation:")
        if 'status_color' in merged_df.columns:
            print(f"  Status colors: {merged_df['status_color'].value_counts().to_dict()}")
        else:
            print("  ❌ status_color column still missing")
            
        if 'traditional_grade' in merged_df.columns:
            print(f"  Traditional grades: {merged_df['traditional_grade'].value_counts().to_dict()}")
        else:
            print("  ❌ traditional_grade column missing")
            
        print(f"  Expected total: 1,382,400 records")
        print(f"  Actual total: {len(merged_df):,} records")
        print(f"  Match: {'✅' if len(merged_df) == 1382400 else '❌'}")
        
        # Show sample of reconstructed data
        print(f"\n🔬 Sample reconstructed data:")
        sample_cols = ['status_color', 'traditional_grade', 'fire_grade', 'age_bucket', 'income_bucket']
        available_sample_cols = [col for col in sample_cols if col in merged_df.columns]
        if available_sample_cols:
            print(merged_df[available_sample_cols].head(3).to_string())
        
    else:
        print("❌ No valid dataframes to merge")
else:
    print("❌ No parquet files found")

# Alternative approach using pandas directory reading
print(f"\n🔄 Alternative: Trying pandas directory-based reading...")
try:
    # This approach might work better for partitioned parquet
    df_alternative = pd.read_parquet('./pfm_compass_data/raw_parquet/', engine='pyarrow')
    print(f"✅ Alternative method: {len(df_alternative):,} rows, {len(df_alternative.columns)} columns")
    print(f"📋 Columns: {list(df_alternative.columns)}")
    
    if 'status_color' in df_alternative.columns:
        print(f"  Status colors: {df_alternative['status_color'].value_counts().to_dict()}")
        
        # Save this version too
        output_file_alt = './pfm_compass_data/retirement_scenarios_FIXED_v4_alternative.parquet'
        print(f"💾 Saving alternative version to: {output_file_alt}")
        df_alternative.to_parquet(output_file_alt, index=False)
        
except Exception as e:
    print(f"❌ Alternative method failed: {e}")

print(f"\n🎯 Summary:")
print(f"If main method worked: Use retirement_scenarios_FIXED_v4.parquet")
print(f"If alternative worked: Use retirement_scenarios_FIXED_v4_alternative.parquet")