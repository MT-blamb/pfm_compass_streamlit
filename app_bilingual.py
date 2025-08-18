import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="PFM Compass - Retirement Planner | 退職計画シミュレーター",
    page_icon="🎯",
    layout="wide"
)

# Language selector at the top
col1, col2, col3 = st.columns([1, 1, 8])
with col1:
    lang = st.selectbox("🌐", ["English", "日本語"], key="language")
with col2:
    st.write("")  # Spacer

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-green { border-left-color: #28a745; background: #f8fff9; }
    .status-yellow { border-left-color: #ffc107; background: #fffef8; }
    .status-red { border-left-color: #dc3545; background: #fff8f8; }
</style>
""", unsafe_allow_html=True)

# Translations
TRANSLATIONS = {
    "English": {
        "title": "🎯 PFM Compass - Japanese Retirement Planner",
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

# User-friendly mappings (bilingual)
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
    """Load the parquet file"""
    try:
        df = pd.read_parquet('./pfm_compass_data/retirement_scenarios_FIXED_v4.parquet')
        return df
    except Exception as e:
        st.error(f"❌ Error loading data | データの読み込みに失敗しました: {e}")
        return None

def simple_lookup(df, age_bucket, current_savings_bucket, expected_expenses_bucket,
                 gender, household_size, housing_status, income_bucket, 
                 marital_status, monthly_savings_bucket, retirement_age_bucket):
    """Simple lookup using the exact sort key format"""
    sort_key = f"combo__{age_bucket}__{current_savings_bucket}__{expected_expenses_bucket}__{gender}__{household_size}__{housing_status}__{income_bucket}__{marital_status}__{monthly_savings_bucket}__{retirement_age_bucket}"
    result = df[df['sk'] == sort_key]
    return result.iloc[0].to_dict() if len(result) > 0 else None

def parse_timeline(timeline_data):
    """Parse the numpy array timeline data"""
    try:
        if hasattr(timeline_data, 'tolist'):
            timeline_list = timeline_data.tolist()
            return pd.DataFrame(timeline_list)
        return None
    except Exception as e:
        return None

def format_currency(amount):
    """Better currency formatting"""
    if amount >= 100_000_000:
        return f"{amount/100_000_000:.1f}億円"
    elif amount >= 10_000:
        return f"{amount/10_000:.0f}万円"
    else:
        return f"{amount:,.0f}円"

def get_status_message(result, lang):
    """Get user-friendly status message in selected language"""
    if result['status_color'] == 'green':
        return TRANSLATIONS[lang]["status_green"]
    elif result['status_color'] == 'yellow':
        return TRANSLATIONS[lang]["status_yellow"]
    else:
        return TRANSLATIONS[lang]["status_red"]

def get_advice(result, lang):
    """Get personalized advice in selected language"""
    advice = []
    
    if lang == "English":
        if result['fire_percentage'] < 50:
            advice.append("💰 Consider increasing savings or reducing expenses")
        
        if result['traditional_retirement_age'] > result['retirement_age_midpoint']:
            years_late = result['traditional_retirement_age'] - result['retirement_age_midpoint']
            advice.append(f"⏰ Expected retirement is {years_late:.0f} years later than target")
        
        if result['fire_grade'] in ['C', 'F']:
            advice.append("📈 Consider more aggressive investment strategies")
        
        if not advice:
            advice.append("✅ Your current plan looks good. Continue building your assets")
    else:  # Japanese
        if result['fire_percentage'] < 50:
            advice.append("💰 貯蓄額を増やすか、支出を削減することをお勧めします")
        
        if result['traditional_retirement_age'] > result['retirement_age_midpoint']:
            years_late = result['traditional_retirement_age'] - result['retirement_age_midpoint']
            advice.append(f"⏰ 目標より{years_late:.0f}年遅い退職になる見込みです")
        
        if result['fire_grade'] in ['C', 'F']:
            advice.append("📈 より積極的な投資戦略を検討してみてください")
        
        if not advice:
            advice.append("✅ 現在の計画は良好です。継続して資産形成を続けてください")
    
    return advice

# Header
st.markdown(f"""
<div class="main-header">
    <h1>{t['title']}</h1>
    <p>{t['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Load data
df = load_data()
if df is None:
    st.stop()

st.success(f"✅ {t['data_loaded']}: {len(df):,} {t['scenarios']}")

# Sidebar form with bilingual labels
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

if analyze_button:
    with st.spinner(t["analyzing"]):
        result = simple_lookup(
            df, age_bucket, current_savings_bucket, expected_expenses_bucket,
            gender, household_size, housing_status, income_bucket,
            marital_status, monthly_savings_bucket, retirement_age_bucket
        )
    
    if result:
        # Status message
        status_msg = get_status_message(result, lang)
        status_class = f"status-{result['status_color']}"
        
        st.markdown(f"""
        <div class="metric-card {status_class}">
            <h3>{status_msg}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fire_status = "Achievable | 達成可能" if result['fire_achievable'] else "Needs improvement | 要改善"
            st.metric(
                t["fire_achievement"],
                f"{result['fire_percentage']:.1f}%",
                f"Grade | グレード: {result['fire_grade']}"
            )
        
        with col2:
            if lang == "English":
                trad_status = "Early" if result.get('early_retirement_ready', 0) > 0 else "Delayed" if result.get('late_retirement', 0) > 0 else "On time"
            else:
                trad_status = "早期" if result.get('early_retirement_ready', 0) > 0 else "遅延" if result.get('late_retirement', 0) > 0 else "予定通り"
            
            st.metric(
                t["traditional_retirement"],
                f"{result['traditional_retirement_age']:.0f}" + (" years | 歳" if lang == "English" else "歳"),
                f"Grade | グレード: {result['traditional_grade']}"
            )
        
        with col3:
            st.metric(
                t["projected_wealth"],
                format_currency(result['projected_wealth']),
                t["at_retirement"]
            )
        
        with col4:
            st.metric(
                t["fire_required"],
                format_currency(result['fire_number']),
                t["years_living_expenses"]
            )
        
        # Detailed analysis
        st.markdown(t["detailed_analysis"])
        
        tab1, tab2, tab3 = st.tabs([t["wealth_timeline"], t["comparison"], t["advice"]])
        
        with tab1:
            timeline_df = parse_timeline(result['wealth_timeline'])
            
            if timeline_df is not None and len(timeline_df) > 0:
                fig = go.Figure()
                
                # Wealth projection line
                fig.add_trace(go.Scatter(
                    x=timeline_df['age'],
                    y=timeline_df['wealth'],
                    mode='lines+markers',
                    name='Wealth Timeline | 資産推移',
                    line=dict(color='#667eea', width=4),
                    marker=dict(size=8),
                    hovertemplate='Age | 年齢: %{x}<br>Wealth | 資産: ¥%{y:,.0f}<extra></extra>'
                ))
                
                # FIRE goal line
                fig.add_hline(
                    y=result['fire_number'],
                    line_dash="dash",
                    line_color="#dc3545",
                    annotation_text=f"FIRE Goal | FIRE目標: {format_currency(result['fire_number'])}"
                )
                
                # Traditional retirement line  
                if result['traditional_number'] > 0:
                    fig.add_hline(
                        y=result['traditional_number'],
                        line_dash="dot",
                        line_color="#28a745", 
                        annotation_text=f"Traditional Goal | 従来退職目標: {format_currency(result['traditional_number'])}"
                    )
                
                # Retirement age line
                retirement_age = result['traditional_retirement_age']
                if retirement_age and not pd.isna(retirement_age):
                    fig.add_vline(
                        x=retirement_age,
                        line_dash="dot",
                        line_color="#ffc107",
                        annotation_text=f"Retirement Age | 退職可能年齢: {retirement_age:.0f}"
                    )
                
                title_text = "Your Wealth Growth Timeline | あなたの資産形成推移"
                xaxis_title = "Age | 年齢"
                yaxis_title = "Wealth (¥) | 資産額 (円)"
                
                fig.update_layout(
                    title=title_text,
                    xaxis_title=xaxis_title,
                    yaxis_title=yaxis_title,
                    height=500,
                    yaxis=dict(tickformat=',.0f'),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                if lang == "English":
                    st.error("Failed to display timeline data")
                else:
                    st.error("タイムラインデータの表示に失敗しました")
        
        with tab2:
            # Comparison chart
            if lang == "English":
                comparison_data = {
                    'Strategy': ['FIRE', 'Traditional'],
                    'Required Amount': [result['fire_number'], result['traditional_number']],
                    'Achievement': [result['fire_percentage'], 100 if result['traditional_retirement_age'] <= result['retirement_age_midpoint'] else 0],
                    'Grade': [result['fire_grade'], result['traditional_grade']]
                }
                title_text = "FIRE vs Traditional Retirement Comparison"
                xaxis_title = "Retirement Strategy"
                yaxis_title = "Required Assets (¥)"
                table_title = "### Comparison Table"
            else:
                comparison_data = {
                    '項目': ['FIRE', '従来退職'],
                    '必要額': [result['fire_number'], result['traditional_number']],
                    '達成度': [result['fire_percentage'], 100 if result['traditional_retirement_age'] <= result['retirement_age_midpoint'] else 0],
                    'グレード': [result['fire_grade'], result['traditional_grade']]
                }
                title_text = "FIRE vs 従来退職 必要資産額比較"
                xaxis_title = "退職戦略"
                yaxis_title = "必要資産額 (円)"
                table_title = "### 比較表"
            
            comp_df = pd.DataFrame(comparison_data)
            
            fig_comp = go.Figure()
            
            x_col = list(comparison_data.keys())[0]
            y_col = list(comparison_data.keys())[1]
            
            fig_comp.add_trace(go.Bar(
                x=comp_df[x_col],
                y=comp_df[y_col],
                name='Required Assets | 必要資産額',
                marker_color=['#667eea', '#764ba2']
            ))
            
            fig_comp.update_layout(
                title=title_text,
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title,
                yaxis=dict(tickformat=',.0f')
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Comparison table
            st.markdown(table_title)
            st.dataframe(comp_df, use_container_width=True)
        
        with tab3:
            st.markdown(t["personalized_advice"])
            
            advice_list = get_advice(result, lang)
            for advice in advice_list:
                st.markdown(f"- {advice}")
            
            st.markdown(t["related_info"])
            
            if result['retirement_age_midpoint'] < 65:
                if lang == "English":
                    st.info("💡 You're considering early retirement before 65. You'll need to fund your lifestyle until pension benefits begin.")
                else:
                    st.info("💡 65歳前の早期退職をお考えですね。年金受給開始まで自己資金で生活する必要があります。")
            
            if result['fire_percentage'] > 80:
                if lang == "English":
                    st.success("🎉 You're close to FIRE achievement! Focus on consistent asset management.")
                else:
                    st.success("🎉 FIRE達成に近づいています！継続的な資産管理を心がけてください。")
            
            st.markdown(t["next_steps"])
            
            if lang == "English":
                st.markdown("""
                1. **Regular Review**: Review your plan 1-2 times per year
                2. **Diversify Investments**: Focus on risk diversification  
                3. **Consult Professionals**: Seek expert advice for detailed planning
                """)
            else:
                st.markdown("""
                1. **定期的な見直し**: 年に1-2回、計画を見直しましょう
                2. **投資の多様化**: リスク分散を心がけてください  
                3. **専門家相談**: より詳細な計画には専門家に相談しましょう
                """)
    
    else:
        if lang == "English":
            st.error("❌ No matching scenario found")
            st.info("💡 Try different parameter combinations")
        else:
            st.error("❌ 該当するシナリオが見つかりませんでした")
            st.info("💡 パラメータを変更してお試しください")

else:
    # Welcome screen
    st.markdown("""
    ## ようこそ！ 👋
    
    **PFM Compass**は、あなたの退職計画を科学的に分析するツールです。
    
    ### 🎯 このツールの特徴
    
    - **FIRE分析**: 経済的独立・早期退職の可能性を評価
    - **従来退職分析**: 一般的な退職計画との比較
    - **日本の年金制度対応**: 65歳からの年金受給を考慮
    - **現実的な生活費**: 日本の実際の生活費データに基づく分析
    
    ### 📊 使い方
    
    1. 左側のフォームにあなたの情報を入力
    2. 「分析開始」ボタンをクリック
    3. 結果とアドバイスを確認
    
    **まずは左側のフォームに情報を入力して、分析を開始してください！**
    """)
    
    # Sample data preview
    with st.expander("📈 サンプルデータプレビュー"):
        sample_data = []
        for color in ['green', 'yellow', 'red']:
            color_sample = df[df['status_color'] == color].sample(1)
            sample_data.append(color_sample)
        
        sample_df = pd.concat(sample_data)
        display_cols = ['status_color', 'age_bucket', 'income_bucket', 'fire_grade', 
                       'traditional_grade', 'projected_wealth']
        st.dataframe(sample_df[display_cols].rename(columns={
            'status_color': 'ステータス',
            'age_bucket': '年齢層', 
            'income_bucket': '収入',
            'fire_grade': 'FIREグレード',
            'traditional_grade': '従来退職グレード',
            'projected_wealth': '予想資産'
        }), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🚀 **PFM Compass** - あなたの退職計画をサポートします")