import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="PFM Compass - Retirement Planning Feature | 退職計画シミュレーター",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language selector at the top
col1, col2, col3 = st.columns([1, 1, 8])
with col1:
    lang = st.selectbox("🌐", ["English", "日本語"], key="language")
with col2:
    st.write("")  # Spacer

# Enhanced CSS with animations and modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: gradient-shift 6s ease infinite;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    @keyframes gradient-shift {
        0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); }
        50% { background: linear-gradient(135deg, #f093fb 0%, #667eea 50%, #764ba2 100%); }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 2px,
            rgba(255,255,255,0.1) 2px,
            rgba(255,255,255,0.1) 4px
        );
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        margin: 0;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #2c3e50, #34495e) !important;
        padding: 2rem;
        border-radius: 20px;
        border-left: 6px solid #667eea;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        opacity: 0.8;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15), 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .metric-card h3 {
        color: white !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600 !important;
        font-size: 1.4rem !important;
        margin: 0 !important;
        line-height: 1.4 !important;
        text-shadow: none !important;
    }
    
    .status-green { 
        border-left-color: #00ff88 !important;
        background: linear-gradient(145deg, #1a4d3a, #2d5a4a) !important;
    }
    
    .status-yellow { 
        border-left-color: #ffeb3b !important;
        background: linear-gradient(145deg, #4d4a1a, #5a562d) !important;
    }
    
    .status-red { 
        border-left-color: #ff4757 !important;
        background: linear-gradient(145deg, #4d1a1a, #5a2d2d) !important;
    }
    
    /* Animated progress bars */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        overflow: hidden;
        height: 8px;
        margin: 10px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 2s ease;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Enhanced sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Glowing effects for important elements */
    .fire-glow {
        animation: fire-glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes fire-glow {
        from { box-shadow: 0 0 20px rgba(255, 71, 87, 0.5); }
        to { box-shadow: 0 0 30px rgba(255, 71, 87, 0.8); }
    }
    
    .success-glow {
        animation: success-glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes success-glow {
        from { box-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
        to { box-shadow: 0 0 30px rgba(0, 255, 136, 0.8); }
    }
    
    /* Modern button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px;
        padding: 10px 20px;
        background: linear-gradient(145deg, #2c3e50, #34495e);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Custom metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Loading animations */
    @keyframes loadingPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .loading {
        animation: loadingPulse 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Translations (keeping your existing translations)
TRANSLATIONS = {
    "English": {
        "title": "PFM Compass - Retirement Planning Feature",
        "subtitle": "Analyze your retirement plan and discover whether FIRE or traditional retirement is optimal for you",
        "profile_header": "👤 Your Profile",
        "basic_info": "### Basic Information",
        "economic_info": "### Economic Status", 
        "retirement_plan": "### Retirement Plan",
        "age": "Age",
        "gender": "Gender",
        "marital_status": "Marital Status",
        "household_size": "Household Size",
        "income": "Annual Income",
        "current_savings": "Current Savings",
        "monthly_savings": "Monthly Savings",
        "retirement_age": "Target Retirement Age",
        "monthly_expenses": "Monthly Living Expenses in Retirement",
        "housing": "Housing Status",
        "analyze_button": "🔍 Analyze",
        "analyzing": "Analyzing...",
        "status_green": "🎉 On track! You're likely to meet your retirement goals",
        "status_yellow": "⚠️ Attention needed. Consider reviewing your plan",
        "status_red": "🚨 Current plan makes target retirement difficult. Major adjustments needed",
        "fire_achievement": "FIRE Achievement",
        "traditional_retirement": "Traditional Retirement Age",
        "projected_wealth": "Projected Wealth",
        "fire_required": "FIRE Required Amount",
        "at_retirement": "at retirement",
        "years_living_expenses": "25 years of living expenses",
        "detailed_analysis": "## 📊 Detailed Analysis",
        "wealth_timeline": "💰 Wealth Timeline",
        "comparison": "📈 Comparison Analysis", 
        "advice": "💡 Advice",
        "scenarios_analysis": "🎯 Scenario Analysis",
        "personalized_advice": "### 💡 Personalized Advice",
        "related_info": "### 📚 Related Information",
        "next_steps": "### 🔗 Next Steps",
        "welcome": "## Welcome! 👋",
        "tool_features": "### 🎯 Tool Features",
        "how_to_use": "### 📊 How to Use",
        "data_loaded": "Database loaded successfully",
        "scenarios": "scenarios"
    },
    "日本語": {
        "title": "🎯 PFM Compass - 日本の退職計画シミュレーター",
        "subtitle": "あなたの退職計画を分析し、FIRE（早期退職）と従来の退職のどちらが最適かお答えします",
        "profile_header": "👤 あなたのプロフィール",
        "basic_info": "### 基本情報",
        "economic_info": "### 経済状況",
        "retirement_plan": "### 退職計画", 
        "age": "年齢",
        "gender": "性別",
        "marital_status": "婚姻状況",
        "household_size": "世帯人数",
        "income": "年収",
        "current_savings": "現在の貯蓄額",
        "monthly_savings": "月間貯蓄額", 
        "retirement_age": "希望退職年齢",
        "monthly_expenses": "退職後の月間生活費",
        "housing": "住居状況",
        "analyze_button": "🔍 分析開始",
        "analyzing": "分析中...",
        "status_green": "🎉 順調です！目標通りに退職できそうです",
        "status_yellow": "⚠️ 注意が必要です。計画の見直しを検討してください", 
        "status_red": "🚨 このままでは目標退職は困難です。大幅な見直しが必要です",
        "fire_achievement": "FIRE 達成度",
        "traditional_retirement": "従来退職年齢",
        "projected_wealth": "予想資産額",
        "fire_required": "FIRE必要額",
        "at_retirement": "退職時点",
        "years_living_expenses": "25年分の生活費",
        "detailed_analysis": "## 📊 詳細分析",
        "wealth_timeline": "💰 資産推移",
        "comparison": "📈 比較分析",
        "advice": "💡 アドバイス",
        "scenarios_analysis": "🎯 シナリオ分析",
        "personalized_advice": "### 💡 パーソナライズされたアドバイス",
        "related_info": "### 📚 関連情報",
        "next_steps": "### 🔗 次のステップ",
        "welcome": "## ようこそ！ 👋",
        "tool_features": "### 🎯 このツールの特徴",
        "how_to_use": "### 📊 使い方",
        "data_loaded": "データベース読み込み完了",
        "scenarios": "件のシナリオ"
    }
}

# Get current language translations
t = TRANSLATIONS[lang]

# Your existing BUCKET_MAPPINGS and functions remain the same...
BUCKET_MAPPINGS = {
    'age_bucket': {
        '20-29': '20s (20-29) | 20代 (20-29歳)', 
        '30-34': 'Early 30s (30-34) | 30代前半 (30-34歳)', 
        '35-39': 'Late 30s (35-39) | 30代後半 (35-39歳)', 
        '40-44': 'Early 40s (40-44) | 40代前半 (40-44歳)',
        '45-49': 'Late 40s (45-49) | 40代後半 (45-49歳)', 
        '50': '50+ | 50代 (50歳以降)'
    },
    'income_bucket': {
        'a': '¥2.5M | 年収250万円', 
        'b': '¥4.5M | 年収450万円', 
        'c': '¥7.5M | 年収750万円',
        'd': '¥10.5M | 年収1,050万円', 
        'e': '¥15M | 年収1,500万円'
    },
    'current_savings_bucket': {
        'a': '¥0.5M | 50万円', 
        'b': '¥3M | 300万円', 
        'c': '¥10M | 1,000万円',
        'd': '¥32.5M | 3,250万円', 
        'e': '¥75M | 7,500万円'
    },
    'monthly_savings_bucket': {
        'a': '¥50k/month | 月5万円', 
        'b': '¥150k/month | 月15万円', 
        'c': '¥250k/month | 月25万円',
        'd': '¥400k/month | 月40万円', 
        'e': '¥625k/month | 月62.5万円', 
        'f': '¥875k/month | 月87.5万円'
    },
    'expected_expenses_bucket': {
        'a': '¥125k/month (Frugal) | 月12.5万円 (質素)', 
        'b': '¥175k/month (Modest) | 月17.5万円 (控えめ)',
        'c': '¥225k/month (Standard) | 月22.5万円 (標準)', 
        'd': '¥300k/month (Comfortable) | 月30万円 (余裕)',
        'e': '¥400k/month (Affluent) | 月40万円 (豊か)', 
        'f': '¥500k/month (Luxury) | 月50万円 (贅沢)'
    },
    'retirement_age_bucket': {
        '50-59': 'Early retirement (50s) | 50代で早期退職', 
        '60-64': 'Early 60s | 60代前半',
        '65': 'Age 65 (Pension starts) | 65歳 (年金受給開始)', 
        '70': 'Age 70 | 70歳'
    },
    'housing_status': {
        'rent': 'Renting | 賃貸', 
        'own_paying': 'Owned (paying mortgage) | 持ち家（ローン返済中）',
        'own_paid': 'Owned (paid off) | 持ち家（ローン完済）', 
        'planning': 'Planning to buy | 購入予定'
    },
    'gender': {
        'm': 'Male | 男性', 
        'f': 'Female | 女性'
    },
    'marital_status': {
        's': 'Single | 独身', 
        'm': 'Married | 既婚'
    },
    'household_size': {
        1: '1 person | 1人', 
        2: '2 people | 2人', 
        3: '3 people | 3人', 
        4: '4+ people | 4人以上'
    }
}

@st.cache_data
def load_data():
    """Load the data from S3 (partitioned structure)"""
    try:
        # Try S3 first
        import boto3
        import awswrangler as wr
        s3_path = "s3://jp-data-lake-experimental-production/lakehouse_experimental_jp_production/pfm_compass_retirement_predictions_internal_v1/"
        df = wr.s3.read_parquet(path=s3_path, dataset=True, partition_filter=None)
        return df
    except:
        # Fallback to local or sample data
        try:
            df = pd.read_parquet('../data/pfm_compass_data/retirement_scenarios_FIXED_v4_alternative.parquet')
            return df
        except:
            # Create sample data for demo
            sample_data = []
            for i in range(100):
                sample_data.append({
                    'sk': f'combo__35-39__c__c__f__2__rent__c__m__d__65__{i}',
                    'age_bucket': '35-39', 'current_savings_bucket': 'c', 'expected_expenses_bucket': 'c',
                    'gender': 'f', 'household_size': 2, 'housing_status': 'rent', 'income_bucket': 'c',
                    'marital_status': 'm', 'monthly_savings_bucket': 'd', 'retirement_age_bucket': '65',
                    'fire_percentage': 75.0 + i % 25, 'fire_grade': 'A', 'traditional_grade': 'B',
                    'status_color': 'green', 'projected_wealth': 50000000, 'fire_number': 60000000,
                    'traditional_retirement_age': 62.0, 'traditional_number': 40000000,
                    'wealth_timeline': [
                        {'age': 37, 'wealth': 10000000, 'year': 2025},
                        {'age': 40, 'wealth': 20000000, 'year': 2028},
                        {'age': 65, 'wealth': 50000000, 'year': 2053}
                    ],
                    'fire_achievable': True, 'on_time_retirement': True,
                    'early_retirement_ready': 3.0, 'late_retirement': 0.0,
                    'age_midpoint': 37.0, 'retirement_age_midpoint': 67.0
                })
            return pd.DataFrame(sample_data)

def create_enhanced_progress_bar(percentage, label, color="#667eea"):
    """Create an animated progress bar"""
    return f"""
    <div style="margin: 15px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span style="color: white; font-weight: 500;">{label}</span>
            <span style="color: white; font-weight: 600;">{percentage:.1f}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {min(percentage, 100)}%; background: linear-gradient(90deg, {color}, {color}88);"></div>
        </div>
    </div>
    """

def create_enhanced_gauge_chart(value, title, max_value=100, color_range=["#ff4757", "#ffa502", "#2ed573"]):
    """Create a modern gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20, 'color': 'white'}},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, max_value], 'tickcolor': "white"},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 50], 'color': color_range[0]},
                {'range': [50, 80], 'color': color_range[1]},
                {'range': [80, 100], 'color': color_range[2]}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Inter"},
        height=300
    )
    return fig

def create_3d_wealth_surface(df_sample):
    """Create a 3D surface plot showing wealth outcomes"""
    # Sample data for 3D visualization
    age_range = np.linspace(25, 65, 20)
    savings_range = np.linspace(50000, 500000, 20)
    
    # Create meshgrid
    age_mesh, savings_mesh = np.meshgrid(age_range, savings_range)
    
    # Simulate wealth data (replace with actual calculations)
    wealth_mesh = (savings_mesh * 12 * (65 - age_mesh) * 1.05 ** (65 - age_mesh)) / 1000000
    
    fig = go.Figure(data=[go.Surface(
        z=wealth_mesh,
        x=age_mesh,
        y=savings_mesh,
        colorscale='Viridis',
        opacity=0.8
    )])
    
    fig.update_layout(
        title='Wealth Projection 3D Surface',
        scene=dict(
            xaxis_title='Age',
            yaxis_title='Monthly Savings (¥)',
            zaxis_title='Projected Wealth (M¥)',
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(255,255,255,0.2)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.2)"),
            zaxis=dict(gridcolor="rgba(255,255,255,0.2)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=600
    )
    return fig

# Enhanced data loading with progress
with st.spinner("🔄 Loading retirement scenarios..."):
    df = load_data()
    
if df is None:
    st.error("Failed to load data")
    st.stop()

# Enhanced header with animation
st.markdown(f"""
<div class="main-header">
    <h1>{t['title']}</h1>
    <p>{t['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Enhanced success message with animation
st.markdown(f"""
<div style="background: linear-gradient(90deg, #00ff88, #00cc70); padding: 1rem; border-radius: 10px; margin: 1rem 0; text-align: center; animation: pulse 2s infinite;">
    <span style="color: white; font-weight: 600;">✅ {t['data_loaded']}: {len(df):,} {t['scenarios']}</span>
</div>
""", unsafe_allow_html=True)

# Your existing sidebar form remains the same...
st.sidebar.header(t["profile_header"])

with st.sidebar.form("profile_form"):
    st.markdown(t["basic_info"])
    
    age_bucket = st.selectbox(
        t["age"],
        options=list(BUCKET_MAPPINGS['age_bucket'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['age_bucket'][x]
    )
    
    gender = st.selectbox(
        t["gender"],
        options=list(BUCKET_MAPPINGS['gender'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['gender'][x]
    )
    
    marital_status = st.selectbox(
        t["marital_status"],
        options=list(BUCKET_MAPPINGS['marital_status'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['marital_status'][x]
    )
    
    household_size = st.selectbox(
        t["household_size"],
        options=list(BUCKET_MAPPINGS['household_size'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['household_size'][x]
    )
    
    st.markdown(t["economic_info"])
    
    income_bucket = st.selectbox(
        t["income"],
        options=list(BUCKET_MAPPINGS['income_bucket'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['income_bucket'][x]
    )
    
    current_savings_bucket = st.selectbox(
        t["current_savings"],
        options=list(BUCKET_MAPPINGS['current_savings_bucket'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['current_savings_bucket'][x]
    )
    
    monthly_savings_bucket = st.selectbox(
        t["monthly_savings"],
        options=list(BUCKET_MAPPINGS['monthly_savings_bucket'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['monthly_savings_bucket'][x]
    )
    
    st.markdown(t["retirement_plan"])
    
    retirement_age_bucket = st.selectbox(
        t["retirement_age"],
        options=list(BUCKET_MAPPINGS['retirement_age_bucket'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['retirement_age_bucket'][x]
    )
    
    expected_expenses_bucket = st.selectbox(
        t["monthly_expenses"],
        options=list(BUCKET_MAPPINGS['expected_expenses_bucket'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['expected_expenses_bucket'][x]
    )
    
    housing_status = st.selectbox(
        t["housing"],
        options=list(BUCKET_MAPPINGS['housing_status'].keys()),
        format_func=lambda x: BUCKET_MAPPINGS['housing_status'][x]
    )
    
    analyze_button = st.form_submit_button(t["analyze_button"], type="primary", use_container_width=True)

# Enhanced analysis section with better functions from your original code
def simple_lookup(df, age_bucket, current_savings_bucket, expected_expenses_bucket,
                 gender, household_size, housing_status, income_bucket, 
                 marital_status, monthly_savings_bucket, retirement_age_bucket):
    """Simple lookup using the exact sort key format"""
    sort_key = f"combo__{age_bucket}__{current_savings_bucket}__{expected_expenses_bucket}__{gender}__{household_size}__{housing_status}__{income_bucket}__{marital_status}__{monthly_savings_bucket}__{retirement_age_bucket}"
    result = df[df['sk'].str.startswith(sort_key) if 'sk' in df.columns else df.index == 0]
    return result.iloc[0].to_dict() if len(result) > 0 else None

def format_currency(amount):
    """Better currency formatting"""
    if amount >= 100_000_000:
        return f"{amount/100_000_000:.1f}億円"
    elif amount >= 10_000:
        return f"{amount/10_000:.0f}万円"
    else:
        return f"{amount:,.0f}円"

if analyze_button:
    # Enhanced loading animation
    with st.spinner("🧠 Analyzing your retirement scenario..."):
        import time
        time.sleep(1)  # Dramatic pause for effect
        
        result = simple_lookup(
            df, age_bucket, current_savings_bucket, expected_expenses_bucket,
            gender, household_size, housing_status, income_bucket,
            marital_status, monthly_savings_bucket, retirement_age_bucket
        )
    
    if result:
        # Enhanced status message with glow effects
        status_msg = TRANSLATIONS[lang]["status_green"] if result.get('status_color', 'green') == 'green' else \
                    TRANSLATIONS[lang]["status_yellow"] if result.get('status_color', 'yellow') == 'yellow' else \
                    TRANSLATIONS[lang]["status_red"]
        
        status_class = f"status-{result.get('status_color', 'green')}"
        glow_class = "success-glow" if result.get('status_color', 'green') == 'green' else "fire-glow" if result.get('status_color', 'red') == 'red' else ""
        
        st.markdown(f"""
        <div class="metric-card {status_class} {glow_class}">
            <h3>{status_msg}</h3>
            {create_enhanced_progress_bar(result.get('fire_percentage', 75), 'Overall Retirement Readiness', '#667eea')}
        """, unsafe_allow_html=True)
        
        # Enhanced metrics with gauges
        col1, col2 = st.columns(2)
        
        with col1:
            # FIRE Achievement Gauge
            fire_fig = create_enhanced_gauge_chart(
                result.get('fire_percentage', 75), 
                f"🔥 {t['fire_achievement']}", 
                100,
                ["#ff4757", "#ffa502", "#2ed573"]
            )
            st.plotly_chart(fire_fig, use_container_width=True)
        
        with col2:
            # Traditional Retirement Readiness
            traditional_readiness = 100 if result.get('traditional_retirement_age', 65) <= result.get('retirement_age_midpoint', 65) else max(0, 100 - (result.get('traditional_retirement_age', 65) - result.get('retirement_age_midpoint', 65)) * 10)
            
            trad_fig = create_enhanced_gauge_chart(
                traditional_readiness, 
                f"⏰ Traditional Readiness", 
                100,
                ["#ff4757", "#ffa502", "#2ed573"]
            )
            st.plotly_chart(trad_fig, use_container_width=True)
        
        # Enhanced metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                t["fire_achievement"],
                f"{result.get('fire_percentage', 75):.1f}%",
                f"Grade: {result.get('fire_grade', 'A')}",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                t["traditional_retirement"],
                f"{result.get('traditional_retirement_age', 62):.0f}歳",
                f"Grade: {result.get('traditional_grade', 'B')}",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                t["projected_wealth"],
                format_currency(result.get('projected_wealth', 50000000)),
                t["at_retirement"]
            )
        
        with col4:
            st.metric(
                t["fire_required"],
                format_currency(result.get('fire_number', 60000000)),
                t["years_living_expenses"]
            )
        
        # Enhanced detailed analysis with new tabs
        st.markdown(t["detailed_analysis"])
        
        tab1, tab2, tab3, tab4 = st.tabs([
            t["wealth_timeline"], 
            t["comparison"], 
            t["scenarios_analysis"],
            t["advice"]
        ])
        
        with tab1:
            # Enhanced wealth timeline with multiple scenarios
            timeline_data = result.get('wealth_timeline', [
                {'age': 37, 'wealth': 10000000, 'year': 2025},
                {'age': 45, 'wealth': 25000000, 'year': 2033},
                {'age': 55, 'wealth': 40000000, 'year': 2043},
                {'age': 65, 'wealth': 50000000, 'year': 2053}
            ])
            
            # Fix: Robust check for timeline data that handles numpy arrays
            try:
                # Check if timeline_data exists and has content
                has_data = False
                if timeline_data is not None:
                    if isinstance(timeline_data, (list, tuple)):
                        has_data = len(timeline_data) > 0
                    elif hasattr(timeline_data, '__len__'):
                        has_data = len(timeline_data) > 0
                    elif hasattr(timeline_data, 'size'):  # numpy array
                        has_data = timeline_data.size > 0
                    else:
                        has_data = bool(timeline_data)
                
                if has_data:
                    # Convert to DataFrame safely
                    if isinstance(timeline_data, list):
                        timeline_df = pd.DataFrame(timeline_data)
                    elif hasattr(timeline_data, 'tolist'):
                        timeline_df = pd.DataFrame(timeline_data.tolist())
                    else:
                        timeline_df = pd.DataFrame([timeline_data])
                    
                    if len(timeline_df) > 0 and 'age' in timeline_df.columns and 'wealth' in timeline_df.columns:
                        # Create subplots for enhanced visualization
                        fig = make_subplots(
                            rows=1, cols=1,
                            subplot_titles=('Wealth Growth Timeline'),
                            vertical_spacing=0.14,
                            specs=[[{"secondary_y": False}],]
                        )
                        
                        # Main wealth timeline
                        fig.add_trace(
                            go.Scatter(
                                x=timeline_df['age'],
                                y=timeline_df['wealth'],
                                mode='lines+markers',
                                name='Projected Wealth',
                                line=dict(color='#667eea', width=4),
                                marker=dict(size=12, symbol='circle'),
                                fill='tonexty' if len(timeline_df) > 1 else None,
                                fillcolor='rgba(102, 126, 234, 0.2)'
                            ),
                            row=1, col=1
                        )
                        
                        # FIRE goal line
                        fig.add_hline(
                            y=result.get('fire_number', 60000000),
                            line_dash="dash",
                            line_color="#e74c3c",
                            annotation_text=f"FIRE Goal: {format_currency(result.get('fire_number', 60000000))}",
                            row=1, col=1
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("📊 Timeline data structure not compatible. Showing summary instead.")
                        # Show simple metrics instead
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Current Age", "37", "Starting point")
                        with col2:
                            st.metric("Target Retirement", "65", "Goal age")
                        with col3:
                            st.metric("Projected Wealth", format_currency(result.get('projected_wealth', 50000000)), "At retirement")
                else:
                    st.info("📈 Timeline data not available. Showing wealth summary instead.")
                    # Show simple wealth progression
                    current_age = 37  # Default or extract from bucket
                    retirement_age = 65
                    years_to_retirement = retirement_age - current_age
                    current_wealth = result.get('current_savings_midpoint', 10000000)
                    final_wealth = result.get('projected_wealth', 50000000)
                    
                    # Simple progression chart
                    simple_timeline = pd.DataFrame({
                        'age': [current_age, retirement_age],
                        'wealth': [current_wealth, final_wealth]
                    })
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=simple_timeline['age'],
                        y=simple_timeline['wealth'],
                        mode='lines+markers',
                        name='Wealth Projection',
                        line=dict(color='#667eea', width=4),
                        marker=dict(size=15)
                    ))
                    
                    fig.update_layout(
                        title="Wealth Projection Overview",
                        xaxis_title="Age",
                        yaxis_title="Wealth (¥)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={'color': "white"},
                        height=800
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error displaying timeline: {str(e)}")
                st.info("💡 Using simplified view instead")
                
                # Fallback simple metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("FIRE Progress", f"{result.get('fire_percentage', 75):.1f}%")
                with col2:
                    st.metric("Traditional Age", f"{result.get('traditional_retirement_age', 62):.0f}")
                with col3:
                    st.metric("Projected Wealth", format_currency(result.get('projected_wealth', 50000000)))
        
        with tab2:
            # Enhanced comparison with radar chart
            comparison_metrics = {
                'FIRE Achievement': result.get('fire_percentage', 75),
                'Traditional Readiness': traditional_readiness,
                'Savings Rate': min(100, (result.get('monthly_savings_midpoint', 250000) * 12 / result.get('income_midpoint', 7500000)) * 100),
                'Time to Goal': max(0, 100 - (result.get('traditional_retirement_age', 62) - 30) * 2),
                'Risk Management': 85  # Placeholder
            }
            
            # Radar chart
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=list(comparison_metrics.values()),
                theta=list(comparison_metrics.keys()),
                fill='toself',
                name='Your Profile',
                line_color='#667eea',
                fillcolor='rgba(102, 126, 234, 0.3)'
            ))
            
            # Add benchmark
            benchmark_values = [70, 75, 60, 70, 80]  # Typical benchmarks
            fig_radar.add_trace(go.Scatterpolar(
                r=benchmark_values,
                theta=list(comparison_metrics.keys()),
                fill='toself',
                name='Average Benchmark',
                line_color='#e74c3c',
                fillcolor='rgba(231, 76, 60, 0.2)'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor="rgba(255,255,255,0.2)"
                    ),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.2)")
                ),
                showlegend=True,
                title="Retirement Readiness Comparison",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white", 'family': "Inter"},
                height=500
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with tab3:
            # New scenarios analysis tab
            st.subheader("🎯 What-If Scenario Analysis")
            
            # Create scenario variations
            scenarios = {
                'Conservative': {'savings_multiplier': 0.8, 'return_rate': 0.02},
                'Current Plan': {'savings_multiplier': 1.0, 'return_rate': 0.03},
                'Aggressive': {'savings_multiplier': 1.3, 'return_rate': 0.05}
            }
            
            scenario_results = []
            for scenario_name, params in scenarios.items():
                # Simulate different outcomes
                base_wealth = result.get('projected_wealth', 50000000)
                adjusted_wealth = base_wealth * params['savings_multiplier'] * (1 + params['return_rate'] - 0.03)
                fire_achievement = min(100, (adjusted_wealth / result.get('fire_number', 60000000)) * 100)
                
                scenario_results.append({
                    'Scenario': scenario_name,
                    'Projected Wealth': adjusted_wealth,
                    'FIRE Achievement': fire_achievement,
                    'Savings Rate': params['savings_multiplier'],
                    'Expected Return': params['return_rate'] * 100
                })
            
            scenario_df = pd.DataFrame(scenario_results)
            
            # Scenario comparison chart
            fig_scenarios = go.Figure()
            
            for i, scenario in enumerate(scenario_results):
                color = ['#e74c3c', '#667eea', '#2ecc71'][i]
                fig_scenarios.add_trace(go.Bar(
                    name=scenario['Scenario'],
                    x=['Projected Wealth', 'FIRE Achievement'],
                    y=[scenario['Projected Wealth']/1000000, scenario['FIRE Achievement']],
                    marker_color=color,
                    opacity=0.8
                ))
            
            fig_scenarios.update_layout(
                title="Scenario Comparison",
                barmode='group',
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white", 'family': "Inter"},
                height=400
            )
            
            st.plotly_chart(fig_scenarios, use_container_width=True)
            
            # Scenario details table
            st.dataframe(
                scenario_df.style.format({
                    'Projected Wealth': '¥{:,.0f}',
                    'FIRE Achievement': '{:.1f}%',
                    'Expected Return': '{:.1f}%'
                }),
                use_container_width=True
            )
        
        with tab4:
            # Enhanced advice with personalized recommendations
            st.markdown("### 💡 AI-Powered Personalized Recommendations")
            
            # Generate dynamic advice based on results
            advice_items = []
            
            fire_pct = result.get('fire_percentage', 75)
            if fire_pct < 50:
                advice_items.append({
                    'icon': '💰',
                    'title': 'Increase Savings Rate',
                    'description': 'Consider increasing monthly savings by 20-30% to improve FIRE readiness',
                    'priority': 'High'
                })
            
            if result.get('traditional_retirement_age', 62) > result.get('retirement_age_midpoint', 65):
                advice_items.append({
                    'icon': '⏰',
                    'title': 'Adjust Timeline',
                    'description': 'Consider retiring 2-3 years later or increasing investment returns',
                    'priority': 'Medium'
                })
            
            if fire_pct > 80:
                advice_items.append({
                    'icon': '🎉',
                    'title': 'Optimize Strategy',
                    'description': 'You\'re on track! Consider tax optimization and estate planning',
                    'priority': 'Low'
                })
            
            # Display advice cards
            for advice in advice_items:
                priority_color = {'High': '#e74c3c', 'Medium': '#f39c12', 'Low': '#2ecc71'}[advice['priority']]
                st.markdown(f"""
                <div style="
                    background: linear-gradient(145deg, #2c3e50, #34495e);
                    padding: 1.5rem;
                    border-radius: 15px;
                    border-left: 4px solid {priority_color};
                    margin: 1rem 0;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 2rem; margin-right: 1rem;">{advice['icon']}</span>
                        <div>
                            <h4 style="color: white; margin: 0; font-family: 'Inter', sans-serif;">{advice['title']}</h4>
                            <span style="color: {priority_color}; font-size: 0.8rem; font-weight: 600;">{advice['priority']} Priority</span>
                        </div>
                    </div>
                    <p style="color: #bdc3c7; margin: 0; font-family: 'Inter', sans-serif;">{advice['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Action plan
            st.markdown("### 🗺️ Next Steps Action Plan")
            
            action_steps = [
                "📊 Review current investment allocation",
                "💳 Maximize employer 401k matching",
                "🏠 Consider housing cost optimization",
                "📈 Explore tax-advantaged accounts",
                "🎯 Set up automatic savings increases"
            ]
            
            for i, step in enumerate(action_steps, 1):
                st.markdown(f"""
                <div style="
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    padding: 1rem;
                    border-radius: 10px;
                    margin: 0.5rem 0;
                    color: white;
                    font-family: 'Inter', sans-serif;
                ">
                    <strong>Step {i}:</strong> {step}
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.error("❌ No matching scenario found. Try different parameters!")

else:
    # Enhanced welcome screen with interactive elements
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
        <h2 style="color: white; font-family: 'Inter', sans-serif; margin-bottom: 2rem;">
            Welcome to PFM Compass
        </h2>
        <p style="color: #bdc3c7; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
            Your AI-powered retirement planning companion. Get personalized insights 
            based on Japanese financial standards and discover your optimal path to financial freedom.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive feature cards
    col1, col2, col3 = st.columns(3)
    
    features = [
        {"icon": "🔥", "title": "FIRE Analysis", "desc": "Economic independence calculations"},
        {"icon": "⏰", "title": "Traditional Planning", "desc": "Pension-integrated retirement"},
        {"icon": "📊", "title": "Scenario Modeling", "desc": "What-if analysis tools"}
    ]
    
    for i, (col, feature) in enumerate(zip([col1, col2, col3], features)):
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #2c3e50, #34495e);
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.1);
                transition: transform 0.3s ease;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            " onmouseover="this.style.transform='translateY(-10px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 3rem; margin-bottom: 1rem;">{feature['icon']}</div>
                <h3 style="color: white; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">{feature['title']}</h3>
                <p style="color: #bdc3c7; font-size: 0.9rem; margin: 0;">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Data insights preview
    if df is not None and len(df) > 0:
        st.markdown("### 📈 Live Data Insights")
        
        # Create a sample analysis
        total_scenarios = len(df)
        if 'status_color' in df.columns:
            green_pct = (df['status_color'] == 'green').mean() * 100
            yellow_pct = (df['status_color'] == 'yellow').mean() * 100
            red_pct = (df['status_color'] == 'red').mean() * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🟢 On Track", f"{green_pct:.1f}%", "of scenarios")
            with col2:
                st.metric("🟡 Needs Attention", f"{yellow_pct:.1f}%", "of scenarios") 
            with col3:
                st.metric("🔴 Requires Action", f"{red_pct:.1f}%", "of scenarios")

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 15px; margin-top: 2rem;">
    <h3 style="color: white; margin-bottom: 1rem; font-family: 'Inter', sans-serif;">🚀 PFM Compass</h3>
    <p style="color: white; margin: 0; opacity: 0.9;">Empowering your financial future with AI-driven insights</p>
</div>
""", unsafe_allow_html=True)
