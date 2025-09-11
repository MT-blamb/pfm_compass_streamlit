**🌐 Language / 言語:** [English](README.md) | [日本語](README_JP.md)

# PFM Compass - Retirement Planning MVP 🎯

### **⚠️ Admin Privileges Required**
Before starting, you'll need temporary admin privileges to install required packages. 

**Request admin access by following this link:**
[Mac Admin Privileges Request Guide](https://moneytree-app.atlassian.net/wiki/spaces/ITKH/pages/2755887278/Mac+How+to+Request+Admin+Privileges?atlOrigin=eyJpIjoiNWFkZjNlMjQzM2EwNDhmOGJmOWZkMDFjMjAxZjMxMGYiLCJwIjoiY29uZmx1ZW5jZS1jaGF0cy1pbnQifQ)

- Contact IT if you need access to this page
- The admin privilege gives you a **5-minute window** to install packages
- You may need to refresh this privilege **multiple times** during installation

> ## 🚀 PFM Compass One-Click Installer
> 
> ### For Non-Technical Users
> This installer automatically sets up the entire PFM Compass application with a single command. **No technical knowledge required!**
> 
> #### Quick Start
> 
> **🍎 Mac/Linux Users:**
> ```bash
> # Download and run the installer
> curl -o install_pfm.sh https://raw.githubusercontent.com/MT-blamb/pfm_compass_streamlit/master/install_pfm.sh
> chmod +x install_pfm.sh
> ./install_pfm.sh
> ```
> 
> **🎮 Launch the application:**
> ```bash
> cd [installation-directory]/pfm_compass_streamlit
> ./launch_simple.sh      # For demos
> ./launch_advanced.sh    # For full features
> ```
> 
> *Choose your installation directory during setup - Desktop, current folder, or custom location!*

---

A comprehensive retirement planning tool for the Japanese market, part of PFM's 2025 product roadmap. This MVP provides instant financial planning insights to drive MILIZE partnership revenue through structured guest data and booking conversions.

## 📋 Overview

**What we're building:** AI & Data Science infrastructure for PFM Compass Life Planning Feature  
**Why:** Supports PFM's main monetization strategy - earning revenue per financial planning session booked with MILIZE  
**Success metrics:** Validated insights, deployed infrastructure, clean data via DynamoDB API, and PFM Team readiness

## 🎯 Key Features

### 🔥 **Dual Retirement Analysis**
- **FIRE Planning**: Financial Independence, Retire Early calculations
- **Traditional Planning**: Standard pension-age retirement with Japanese pension integration

### 🌐 **Bilingual Interface** 
- Complete Japanese/English UI for the Japanese market
- Cultural and financial context appropriate for Japanese users

### 📊 **Advanced Analytics**
- Real-time lookup from **1.38M pre-computed retirement scenarios**
- Interactive wealth timeline visualizations
- Comparative analysis against Japanese financial benchmarks
- What-if scenario modeling

### 💡 **Personalized Insights**
- AI-powered recommendations based on user profile
- Status-based action items and next steps
- Integration pathway for MILIZE specialist bookings

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git (for downloading the repository)
- Terminal/Command Prompt access

### Step 1: Download the Repository

1. **Open Terminal/Command Prompt**
2. **Navigate to your desired folder:**
   ```bash
   cd Desktop
   # or wherever you want to store the project
   ```
3. **Clone the repository:**
   ```bash
   git clone https://github.com/MT-blamb/pfm_compass_streamlit.git
   cd PFM_COMPASS_STREAMLIT
   ```

### Step 2: Set Up Python Environment

---

## 🍎 **Mac Installation Guide for Non-Technical Users**

**For stakeholders without development environments set up**, follow this complete installation guide:

### **⚠️ Admin Privileges Required**
Before starting, you'll need temporary admin privileges to install required packages. 

**Request admin access by following this link:**
[Mac Admin Privileges Request Guide](https://moneytree-app.atlassian.net/wiki/spaces/ITKH/pages/2755887278/Mac+How+to+Request+Admin+Privileges?atlOrigin=eyJpIjoiNWFkZjNlMjQzM2EwNDhmOGJmOWZkMDFjMjAxZjMxMGYiLCJwIjoiY29uZmx1ZW5jZS1jaGF0cy1pbnQifQ)

- Contact IT if you need access to this page
- The admin privilege gives you a **5-minute window** to install packages
- You may need to refresh this privilege **multiple times** during installation

### **📋 Step-by-Step Installation Order**

**1. Install Xcode Command Line Tools** (Required first)
```bash
xcode-select --install
```
- A popup will appear → click **Install**
- This provides basic compilers and tools required on macOS

**2. Install Homebrew** (Package manager for Mac)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- Follow the prompts, enter your Mac password when asked
- **Important:** At the end, copy and paste the lines it gives you to add to `.zprofile` or `.zshrc`
- Verify installation:
```bash
brew --version
```

**3. Install Python** (3.9 or 3.10 recommended)
```bash
brew install python@3.10
```
- Confirm installation:
```bash
python3 --version
```

**4. Install Git** (if not already installed)
```bash
brew install git
```
- Confirm installation:
```bash
git --version
```

**5. Install Virtual Environment Tool**
```bash
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
```

**6. Set Up Project Environment**
```bash
cd ~/Desktop/PFM_COMPASS_STREAMLIT   # Navigate to the downloaded repo
python3 -m venv venv                 # Create virtual environment
source venv/bin/activate             # Activate it
```

**7. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

**8. Run the Application**
- Simple bilingual app:
```bash
streamlit run app_bilingual.py
```
- Advanced version:
```bash
cd bling
streamlit run app.py
```

### **🛠️ Mac Troubleshooting**

**If `brew` command not found:**
- Restart Terminal and try again

**If `streamlit` command not found:**
- Ensure virtual environment is activated: `source venv/bin/activate`
- Re-run: `pip install -r requirements.txt`

**If port already in use:**
```bash
streamlit run app_bilingual.py --server.port 8502
```

**If you get permission errors:**
- Request admin privileges again (5-minute window expired)
- Contact IT for additional support

---

## 💻 **Standard Installation (For Technical Users)**

**Option A: Using pip (Recommended for most users)**
```bash
# Install required packages
pip install -r requirements.txt
```

**Option B: Using conda (If you have Anaconda/Miniconda)**
```bash
# Create new environment
conda create -n pfm-compass python=3.9
conda activate pfm-compass
pip install -r requirements.txt
```

---

## 🎮 Running the Applications

You have **two versions** to choose from:

### Version 1: Simple Bilingual App (Recommended for demos)
**Best for:** Quick demos, stakeholder presentations, basic functionality testing

```bash
streamlit run app_bilingual.py
```

**Features:**
- Clean, simple interface
- Japanese/English language toggle
- Core FIRE vs Traditional retirement analysis
- Essential metrics and visualizations

---

### Version 2: Advanced Feature-Rich App (Full MVP)
**Best for:** Complete testing, advanced analysis, full feature evaluation

```bash
cd bling
streamlit run app.py
```

**Features:**
- Enhanced UI with animations and modern styling
- Advanced scenario analysis and what-if modeling
- Detailed chart explanations and user guidance
- Comprehensive advice engine with actionable recommendations
- 90-day action plans
- MILIZE integration call-to-actions

---

## 🌐 Accessing the Applications

After running either command, you'll see output like:
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

**To use the app:**
1. Open your web browser
2. Go to `http://localhost:8501`
3. The application will load automatically

**To stop the app:** Press `Ctrl+C` (Windows/Linux) or `Cmd+C` (Mac) in the terminal

---

## 📊 Data Architecture

### Pre-computed Scenarios
- **1.38M retirement scenarios** stored locally in `/data/pfm_compass_data/`
- Partitioned by status color for optimized lookup
- No external S3 dependencies - all data included in repository

### Scenario Buckets
The system analyzes combinations of:
- **Age groups**: 20s, 30s (early/late), 40s (early/late), 50+
- **Income levels**: ¥2.5M to ¥15M annual income
- **Savings buckets**: ¥50K to ¥875K monthly savings
- **Expense levels**: ¥125K to ¥500K monthly retirement expenses
- **Demographics**: Gender, marital status, household size, housing status

---

## 🔧 Technical Architecture

### Frontend
- **Streamlit**: Interactive web application framework
- **Plotly**: Advanced data visualizations and charts
- **Custom CSS**: Enhanced UI with animations and modern styling

### Backend
- **Pandas**: Data processing and scenario lookup
- **NumPy**: Mathematical calculations and projections
- **Local Parquet files**: High-performance data storage

### Key Files
```
├── app_bilingual.py          # Simple version
├── bling/app.py             # Advanced version
├── data/pfm_compass_data/   # All scenario data
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🎯 Testing Scenarios

### For Stakeholder Demos
**Use app_bilingual.py** - cleaner interface, faster demos

**Sample Test Profiles:**
1. **Young Professional**: Age 30-34, ¥7.5M income, ¥250K monthly savings
2. **Mid-Career**: Age 35-39, ¥10.5M income, ¥400K monthly savings  
3. **Pre-Retirement**: Age 45-49, ¥15M income, ¥625K monthly savings

### For Complete Feature Testing
**Use bling/app.py** - full feature set, advanced analysis

**Test the flow:**
1. Enter profile information in sidebar
2. Click "Analyze" 
3. Review status and metrics
4. Explore all 4 tabs: Timeline, Comparison, Scenarios, Advice
5. Test language switching (English ↔ 日本語)

---

## 📈 Expected Outcomes

### For PFM Team
- **Instant insights** generation from user demographic input
- **Structured data** ready for DynamoDB API integration
- **MILIZE booking motivation** through gap analysis and recommendations

### For Users
- **FIRE feasibility** assessment with specific timeline
- **Traditional retirement** readiness evaluation
- **Personalized advice** with actionable next steps
- **Professional consultation** pathway for deeper guidance

---

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Port already in use:**
```bash
streamlit run app_bilingual.py --server.port 8502
```

**Data loading issues:**
- Ensure you're in the correct directory
- Check that `/data/pfm_compass_data/` folder exists
- Verify parquet files are present

**Permission errors on Windows:**
- Run Command Prompt as Administrator
- Or use PowerShell instead of Command Prompt

### Getting Help
- Check terminal output for error messages
- Ensure Python version is 3.8+
- Verify all files downloaded correctly from repository

---

## 🎯 Success Metrics For Demo

### Technical Validation
- [ ] App loads successfully on localhost
- [ ] Data lookup responds within 2 seconds
- [ ] All visualizations render correctly
- [ ] Language switching functions properly

### Business Validation
- [ ] Insights generated match expected quality
- [ ] User flow supports MILIZE booking motivation
- [ ] Scenarios cover target demographic ranges
- [ ] Advice recommendations are actionable

---

## 📞 Next Steps

### For PFM Integration
1. **API Development**: DynamoDB integration for real-time data exchange
2. **User Authentication**: Integration with PFM user management
3. **Booking Flow**: Direct MILIZE appointment scheduling
4. **Analytics**: User behavior tracking and conversion metrics

### For Production Deployment
1. **Cloud Infrastructure**: AWS deployment configuration
2. **Performance Optimization**: Caching and database optimization
4. **Monitoring**: Application health and usage analytics

---

## 🏗️ Development Team

**AI & Data Science Team** - Core development and delivery  
**PFM Team** - Integration and user experience  
**MILIZE Partnership** - Business logic and monetization strategy

---

## 🛑 **How to Stop the Application**

When you're finished using the PFM Compass demo, here's how to properly shut it down:

### **Stopping the Streamlit App**
1. **Go to your Terminal/Command Prompt** (where you ran the `streamlit run` command)
2. **Press the following keys:**
   - **Mac/Linux:** `Ctrl + C`
   - **Windows:** `Ctrl + C`
3. **You should see:** `Stopping...` or similar message
4. **The app will shut down** and return you to the command prompt

### **Deactivating the Virtual Environment** (If you used one)
After stopping the app, deactivate your Python virtual environment:
```bash
deactivate
```

### **Closing the Browser**
- Simply close the browser tab with `http://localhost:8501`
- Or close your entire browser if preferred

### **What This Does:**
- **Stops the local server** running your app
- **Frees up system resources** (CPU, memory)
- **Releases the port** (8501) for other applications
- **Returns Terminal** to normal command prompt

### **Troubleshooting Stop Issues**

**If `Ctrl + C` doesn't work:**
- Try pressing it multiple times
- Or close the Terminal/Command Prompt window entirely

**If port remains busy after stopping:**
```bash
# Find and kill the process using port 8501
lsof -ti:8501 | xargs kill -9
```

**If you need to restart the app:**
- Follow the same startup commands from the installation guide
- Make sure you're in the correct directory and virtual environment

---

*This MVP represents the data-side work owned by AI & Data Science Team, delivered in alignment with PFM Team requirements and MILIZE partnership objectives.*