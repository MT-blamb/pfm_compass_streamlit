import subprocess
import sys
import os

def run_inspector():
    """Run the data inspector"""
    if not os.path.exists('./data/retirement_scenarios.parquet'):
        print("❌ Data file not found: ./data/retirement_scenarios.parquet")
        return False
    
    print("🔍 Starting PFM Compass Data Inspector...")
    print("📊 This will show samples from each status color")
    print("📈 And help us understand the wealth timeline structure")
    print("🌐 Opening: http://localhost:8502")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'inspect_data.py', '--server.port', '8502'
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Inspector stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running inspector: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_inspector()