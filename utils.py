import pandas as pd
import streamlit as st
import json

# ---------- Data loading ----------

@st.cache_data(show_spinner=False)
def load_data():
    """Load the retirement scenarios data with optimized caching"""
    try:
        df = pd.read_parquet('./data/retirement_scenarios.parquet')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# ---------- Lookup & helpers ----------

def _norm_str(x: str) -> str:
    return str(x).strip().lower()

def _canon_ret_age(val: str) -> set:
    """
    Accept both '65' and '65+' etc. Returns a set of acceptable tokens (lowercased).
    """
    v = _norm_str(val)
    if v in {"65", "65+"}:
        return {"65", "65+"}
    if v in {"70", "70+"}:
        return {"70", "70+"}
    return {v}

def lookup_scenario(
    df,
    age_bucket,
    current_savings_bucket,
    expected_expenses_bucket,
    gender,
    household_size,
    housing_status,
    income_bucket,
    marital_status,
    monthly_savings_bucket,
    retirement_age_bucket,
):
    """
    Look up a specific retirement scenario based on user inputs.
    - Normalizes case so parquet values like 'A' match UI keys like 'a'.
    - Skips a filter if that column doesn't exist in the dataset (e.g., expected_expenses_bucket).
    """
    if df is None:
        return None

    mask = pd.Series(True, index=df.index)

    def add_str_eq(col, val):
        nonlocal mask
        if col in df.columns:
            mask &= df[col].astype(str).str.lower().eq(_norm_str(val))

    def add_ret_age_eq(col, val):
        nonlocal mask
        if col in df.columns:
            choices = _canon_ret_age(val)
            mask &= df[col].astype(str).str.lower().isin(choices)

    def add_num_eq(col, val):
        nonlocal mask
        if col in df.columns:
            mask &= (pd.to_numeric(df[col], errors="coerce") == val)

    # Apply filters (case-insensitive for strings)
    add_str_eq("age_bucket", age_bucket)
    add_str_eq("current_savings_bucket", current_savings_bucket)
    if "expected_expenses_bucket" in df.columns:
        add_str_eq("expected_expenses_bucket", expected_expenses_bucket)
    add_str_eq("gender", gender)
    add_num_eq("household_size", household_size)
    add_str_eq("housing_status", housing_status)
    add_str_eq("income_bucket", income_bucket)
    add_str_eq("marital_status", marital_status)
    add_str_eq("monthly_savings_bucket", monthly_savings_bucket)
    add_ret_age_eq("retirement_age_bucket", retirement_age_bucket)

    result_df = df[mask]
    if len(result_df) > 0:
        return result_df.iloc[0].to_dict()
    return None

# ---------- Formatting ----------

def format_currency(amount):
    """Format currency in Japanese Yen with appropriate suffixes"""
    if pd.isna(amount) or amount == 0:
        return "¥0"
    if amount >= 100_000_000:  # 1億円以上
        return f"¥{amount/100_000_000:.1f}億円"
    elif amount >= 10_000:  # 1万円以上
        return f"¥{amount/10_000:.0f}万円"
    else:
        return f"¥{amount:,.0f}"

def get_bucket_mappings():
    """Create mapping dictionaries for all bucket types (UI labels)"""
    return {
        'age_bucket': {
            "20-29": "20代 (20-29歳)",
            "30-34": "30代前半 (30-34歳)",
            "35-39": "30代後半 (35-39歳)",
            "40-44": "40代前半 (40-44歳)",
            "45-49": "40代後半 (45-49歳)",
            "50": "50代以上 (50歳〜)"   # Note: your parquet may use '50+' or '50-59'
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
            "65": "65歳 (Standard retirement)",   # parquet may use '65+'
            "70": "70歳 (Late retirement)"
        },
        'housing_status': {
            "rent": "賃貸 (Renting)",
            "own_paying": "ローン返済中 (Paying mortgage)",
            "own_paid": "持ち家完済 (Owned - paid off)",
            "planning": "購入予定 (Planning to buy)"
        }
    }

# ---------- Insights ----------

def get_status_insights(result):
    """Generate personalized insights based on scenario results"""
    insights = []

    # Status-based insights
    color = result.get('status_color', 'yellow')
    if color == 'green':
        insights.append("🎉 Great job! Your retirement planning is on track.")
        if result.get('early_retirement_ready', 0) > 5:
            insights.append(f"🌟 Excellent! You could retire {result['early_retirement_ready']:.1f} years early.")
    elif color == 'yellow':
        insights.append("⚠️ Your plan needs some adjustments. Consider increasing savings or extending timeline.")
        if result.get('late_retirement', 0) > 0:
            insights.append(f"⏰ Current plan might delay retirement by {result['late_retirement']:.1f} years.")
    else:
        insights.append("🚨 Your current plan needs significant changes to meet retirement goals.")
        if result.get('late_retirement', 0) > 0:
            insights.append(f"📈 Consider increasing savings or working {result['late_retirement']:.1f} years longer.")

    # FIRE-specific insights
    if result.get('fire_achievable', False):
        insights.append(f"🔥 FIRE achievable! You're {result.get('fire_percentage', 0):.1f}% ready for financial independence.")
    else:
        gap = 100 - float(result.get('fire_percentage', 0) or 0)
        if gap < 20:
            insights.append(f"🎯 Almost there! You need {gap:.1f}% more to reach FIRE.")
        else:
            insights.append("🎯 To reach FIRE, focus on increasing savings or reducing expenses.")

    # Grade-based insights
    fire_grade = result.get('fire_grade', '')
    traditional_grade = result.get('traditional_grade', '')
    if fire_grade == 'A+' and traditional_grade == 'A+':
        insights.append("🏆 Perfect score! You're a retirement planning champion.")
    elif fire_grade in ['A+', 'A'] or traditional_grade in ['A+', 'A']:
        insights.append("🌟 Strong performance in retirement planning!")

    return insights

# ---------- Timeline parsing & generation ----------

def parse_wealth_timeline(timeline_str):
    """Parse wealth timeline JSON string safely - handles multiple formats"""
    try:
        if timeline_str is None or pd.isna(timeline_str):
            return None

        if not isinstance(timeline_str, str):
            timeline_str = str(timeline_str)

        if timeline_str.strip() in ("", "nan"):
            return None

        timeline_data = None
        try:
            timeline_data = json.loads(timeline_str)
        except json.JSONDecodeError:
            try:
                import ast
                timeline_data = ast.literal_eval(timeline_str)
            except (ValueError, SyntaxError):
                # Try key=value style → JSON-ish
                import re
                jsonish = re.sub(r'(\w+)=', r'"\1":', timeline_str)
                try:
                    timeline_data = json.loads(jsonish)
                except Exception:
                    return None

        if not isinstance(timeline_data, list) or not timeline_data:
            return None

        rows = []
        for item in timeline_data:
            if isinstance(item, dict):
                age = item.get("age")
                wealth = item.get("wealth")
                year = item.get("year")
                try:
                    age = float(age)
                    wealth = float(wealth)
                    year = None if year is None else float(year)
                except (TypeError, ValueError):
                    continue
                if pd.notna(age) and pd.notna(wealth):
                    rows.append({"age": age, "wealth": wealth, "year": year})

        if rows:
            df = pd.DataFrame(rows)
            # If year missing, synthesize a simple series
            if "year" not in df or df["year"].isna().all():
                start_year = 2024
                base_age = df["age"].min()
                df["year"] = (start_year + (df["age"] - base_age)).astype(int)
            return df

        return None
    except Exception:
        return None

def generate_wealth_timeline(result):
    """
    Generate a wealth timeline from scenario parameters (simple projection):
    - 7% annual return until retirement with annual contributions (monthly*12)
    - After retirement, 4% withdrawals (kept simple; you can refine later)
    - Points every 3 years
    """
    try:
        current_age = float(result.get('age_midpoint', 30) or 30)
        current_savings = float(result.get('current_savings_midpoint', 500_000) or 0)
        monthly_savings = float(result.get('monthly_savings_midpoint', 50_000) or 0)
        retirement_age = float(result.get('traditional_retirement_age', result.get('retirement_age_midpoint', 65)) or 65)

        annual_return = 0.07
        withdrawal_rate = 0.04
        annual_contrib = monthly_savings * 12
        start_year = 2024

        timeline = []
        wealth_now = current_savings
        end_age = min(retirement_age + 5, 80)

        # initial point
        timeline.append({"age": int(current_age), "wealth": int(wealth_now), "year": start_year})

        # 3-year steps
        total_years = int(end_age - current_age)
        for step in range(3, total_years + 1, 3):
            age = current_age + step
            year = start_year + step
            wealth = wealth_now

            for _ in range(3):
                if (current_age < retirement_age) and (age - (2 - _) > retirement_age):
                    # Crossing retirement inside the 3-year window → keep it simple (treat as retired if age exceeds)
                    pass
                if age - (2 - _) <= retirement_age:
                    # working years: invest + contribute
                    wealth = wealth * (1 + annual_return) + annual_contrib
                else:
                    # retired: invest then withdraw
                    wealth = wealth * (1 + annual_return) - (wealth * withdrawal_rate)
                    wealth = max(0, wealth)

            timeline.append({"age": int(age), "wealth": int(wealth), "year": int(year)})
            wealth_now = wealth

        # Ensure explicit retirement point exists
        if timeline[-1]["age"] < retirement_age:
            yrs = int(retirement_age - current_age)
            wealth = current_savings
            for _ in range(yrs):
                wealth = wealth * (1 + annual_return) + annual_contrib
            timeline.append({"age": int(retirement_age), "wealth": int(wealth), "year": start_year + yrs})

        return pd.DataFrame(timeline)
    except Exception:
        return None

def get_wealth_timeline(result):
    """
    Return a DataFrame with columns: age, wealth, year.
    Tries stored timeline first; falls back to simple generation.
    """
    df = parse_wealth_timeline(result.get("wealth_timeline", ""))
    if df is None or df.empty:
        df = generate_wealth_timeline(result)
    return df
