# Quick test runner for the Streamlit app
import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    required = ['streamlit', 'pandas', 'plotly', 'pyarrow']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {missing}")
        print(f"📦 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True

def run_streamlit():
    """Run the Streamlit app"""
    if not os.path.exists('./data/retirement_scenarios.parquet'):
        print("❌ Data file not found: ./data/retirement_scenarios.parquet")
        return False
    
    print("🚀 Starting PFM Compass Streamlit app...")
    print("📊 Data file: ✅ Found")
    print("🌐 Opening: http://localhost:8501")
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running app: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if check_requirements():
        run_streamlit()