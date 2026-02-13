# 🛡️ ShieldBank Dashboard - User Guide

Welcome to the **ShieldBank: Financial Crime Detection** Command Center! This guide will help you navigate and use all the powerful features of your fraud detection dashboard.

## 🎯 Quick Start

### Starting the Dashboard

1. **Start the API Server** (required for predictions):
   ```bash
   make run_api
   # Or: uvicorn api.fastapi:app --reload --port 8000
   ```

2. **Launch the Dashboard**:
   ```bash
   make run_streamlit
   # Or: streamlit run streamlit_app/app.py
   ```

3. **Access the Dashboard**:
   - Browser will open automatically at `http://localhost:8501`
   - If not, navigate to that URL manually

## 📊 Dashboard Layout

### Sidebar Navigation

The left sidebar (in bank blue gradient) provides:

#### System Status
- 🟢 Model Status: Online/Offline indicator
- 🟢 API Connection: Backend connectivity
- ⏱️ Uptime: System availability percentage

#### Settings
- **Fraud Threshold**: Adjustable slider (0.0 - 1.0)
  - Default: 0.75
  - Higher = More strict (fewer false positives, but might miss some fraud)
  - Lower = More sensitive (catches more fraud, but more false positives)

#### Quick Stats
- Today's transaction count
- Current fraud rate
- Average API response time

## 📑 Three Main Tabs

### Tab 1: 📊 Executive Summary

**Purpose**: High-level overview for executives and managers

#### Top Metrics Row
Five key performance indicators:
1. **Total Transactions**: Cumulative count with today's delta
2. **Fraud Detected**: Number of flagged transactions with fraud rate %
3. **Fraud Prevented**: Successfully blocked fraudulent transactions
4. **False Positives**: Legitimate transactions incorrectly flagged (lower is better)
5. **Total Saved**: Financial impact of fraud prevention

#### Fraud Heatmap: Time vs Amount
**What it shows**: Where fraud clusters occur
- **X-axis**: Hour of day (00:00 - 23:00)
- **Y-axis**: Transaction amount ranges
- **Color**: Red intensity = fraud frequency

**How to read it**:
- Darker red = more fraud at that time/amount combination
- Common pattern: Late night (22:00-04:00) + higher amounts = more fraud
- Use this to identify:
  - High-risk time windows
  - Suspicious amount patterns
  - When to increase manual review

#### Risk Distribution Donut Chart
- **High Risk** (Red): Immediate fraud flags
- **Medium Risk** (Orange): Requires review
- **Low Risk** (Yellow): Minor concerns
- **Safe** (Green): Legitimate transactions

#### 7-Day Trend Line
- Shows fraud case count over the past week
- Helps identify:
  - Weekly patterns
  - Sudden spikes
  - Effectiveness of interventions

#### 🔴 Live Transaction Feed

**The Star Feature**: Real-time monitoring simulation

**How to use**:
1. Click **"▶️ Start Live Monitoring"**
2. Watch as transactions stream in real-time
3. Each transaction shows:
   - Transaction ID (TXN-XXXXXX)
   - Amount ($)
   - Timestamp
   - Risk Score (color-coded: 🟢 Safe, 🟡 Medium, 🔴 High)
   - Verdict (✅ SAFE or 🚨 FRAUD)

**Use cases**:
- Demonstrate live monitoring to stakeholders
- Simulate busy periods
- Test system responsiveness
- Train staff on pattern recognition

**Note**: This is a simulation for demonstration. In production, connect to your live transaction stream.

---

### Tab 2: 🔍 Fraud Deep Dive

**Purpose**: Analyze individual transactions in detail

#### Transaction Input Form

The form is organized into logical sections:

##### 💰 Financial Information
- **Income**: Annual income
- **Customer Age**: Age in years
- **Credit Risk Score**: Credit bureau score (0-850)
- **Proposed Credit Limit**: Requested credit line
- **Intended Balance Amount**: Expected balance

##### ⏱️ Behavioral Metrics
- **Session Length**: Minutes spent on the application
- **Days Since Request**: Time since initial request
- **Bank Months Count**: Customer tenure
- **Zip Count (4w)**: Unique zip codes in last 4 weeks

##### 🚀 Velocity Indicators
Critical fraud signals based on activity frequency:
- **Velocity 6h**: Transactions in last 6 hours
- **Velocity 24h**: Transactions in last 24 hours
- **Velocity 4w**: Transactions in last 4 weeks

**Red flags**: Unusually high velocity = possible account takeover or bot activity

##### 🏷️ Binary Flags
Simple yes/no indicators:
- **Email is Free**: Using Gmail/Yahoo vs. custom domain
- **Phone Home Valid**: Verified home phone number
- **Phone Mobile Valid**: Verified mobile number
- **Has Other Cards**: Existing credit cards
- **Foreign Request**: Application from outside home country
- **Keep Alive Session**: Persistent session indicator

##### 👤 Customer Profile
- **Employment Status**: employed | self-employed | unemployed | student
- **Housing Status**: rent | own | mortgage

##### 💳 Transaction Details
- **Payment Type**: credit_card | debit_card | bank_transfer
- **Source**: web | mobile

##### 📱 Device Information
- **Device OS**: android | ios | windows | mac
- **Month**: 1-12 (seasonal patterns)

##### 🏦 Account History
- **Bank Branch Count (8w)**: Branches visited in last 8 weeks
- **Device Distinct Emails (8w)**: Unique emails per device
- **DOB Distinct Emails (4w)**: Email changes with same DOB
- **Previous/Current Address Months**: Address stability

#### Analysis Results

After clicking **"🔍 Analyze Transaction"**, you'll see:

##### Main Verdict
- Large alert box: 🚨 **FRAUD DETECTED** or ✅ **TRANSACTION SAFE**

##### Risk Score Gauge
- Visual speedometer showing risk percentage
- Red threshold line at your configured fraud threshold
- Green/Yellow/Red zones for easy interpretation

##### Metrics
- **Fraud Risk**: Calculated probability (%)
- **Threshold**: Your configured cutoff
- **API Latency**: Response time in milliseconds

##### 🎯 SHAP Explanation: "Why was this flagged?"

**Most Important Feature**: This section answers the critical question every fraud analyst asks: *"Why did the model make this decision?"*

**How to read the SHAP chart**:
- **Horizontal bar chart** showing feature impacts
- **Red bars** (pointing right): Features pushing towards FRAUD
  - Longer red bar = stronger fraud signal
  - Example: High velocity_24h with red bar = suspicious rapid transactions

- **Green bars** (pointing left): Features pushing towards SAFE
  - Longer green bar = stronger legitimacy signal
  - Example: Long bank_months_count with green bar = trusted customer

**Practical use**:
1. Review the top 3-5 features
2. Check if the SHAP explanation makes business sense
3. Use for explaining decisions to:
   - Customers ("We flagged this because...")
   - Compliance teams
   - Auditors
   - Machine learning interpretability reports

**Example interpretation**:
```
velocity_24h: +0.23 (RED)
→ Customer made 15 transactions in 24 hours (normal is 2-3)
→ This strongly suggests fraud

bank_months_count: -0.11 (GREEN)
→ Customer has been with bank for 8 years
→ This suggests legitimate customer

Net effect: fraud_score = 0.82 → FRAUD
```

---

### Tab 3: 🎯 Model Performance

**Purpose**: Understand how well the model works (for data scientists, managers)

#### ROC Curve
- **What it shows**: Trade-off between catching fraud (true positives) and false alarms (false positives)
- **Y-axis**: True Positive Rate (% of fraud caught)
- **X-axis**: False Positive Rate (% of false alarms)
- **AUC = 0.89**: Excellent performance (1.0 = perfect, 0.5 = random guessing)

**How to use**:
- Compare against baseline (gray dashed line)
- Higher AUC = better model
- Use for reporting model quality to stakeholders

#### Precision-Recall Curve
- **Precision**: When model says "fraud", how often is it right?
- **Recall**: What % of actual fraud cases does the model catch?
- **Area under curve**: Overall model quality

#### Confusion Matrix
A 2x2 grid showing:
- **True Negatives** (top-left): Correctly identified safe transactions
- **False Positives** (top-right): Safe transactions incorrectly flagged as fraud
- **False Negatives** (bottom-left): Fraud that slipped through
- **True Positives** (bottom-right): Correctly caught fraud

**What to monitor**:
- **High false negatives**: Missing too much fraud → lower threshold
- **High false positives**: Too many false alarms → raise threshold

#### Performance Metrics Bar Chart
Four key metrics:
- **Accuracy**: Overall correctness
- **Precision**: Fraud flags that are correct
- **Recall**: Fraud cases caught
- **F1-Score**: Harmonic mean of precision and recall

#### 🎯 Global Feature Importance (SHAP)

**What it shows**: Which features matter most *across all transactions*

**Top features** (typical ranking):
1. **velocity_24h**: Transaction frequency (fraud pattern indicator)
2. **credit_risk_score**: Credit bureau assessment
3. **velocity_4w**: Monthly transaction volume
4. **foreign_request**: International vs. domestic
5. **velocity_6h**: Very short-term activity spikes

**How to use this**:
- **Model improvement**: Focus data quality efforts on top features
- **Feature engineering**: Create new features similar to important ones
- **Business insights**: Understand what drives fraud in your domain
- **Compliance**: Document which factors influence decisions

#### Model Information Cards

Three summary cards:

##### 🤖 Model Info
- Algorithm type
- Version number
- Training date
- Feature count
- Training dataset size

##### ⚡ Performance
- Inference time (latency)
- Throughput (requests/second)
- AUC-ROC score
- Average precision
- Recall at threshold

##### 🎯 Business Impact
- Fraud prevention rate
- False positive rate
- Estimated savings
- Manual review reduction

---

## 🎨 Visual Design Features

### Bank Blue Theme
Professional color scheme:
- **Primary**: Dark blue (#003d82) - Trust and security
- **Accent**: Light blue (#00a3e0) - Energy and clarity
- **Success**: Green (#00c853) - Safe transactions
- **Danger**: Red (#d32f2f) - Fraud alerts

### Responsive Layout
- **Wide layout** for maximum data visibility
- **Multi-column** arrangement for efficient space usage
- **Plotly charts** for interactive exploration (hover, zoom, pan)

---

## 💡 Best Practices

### For Daily Operations
1. **Morning routine**:
   - Check Executive Summary metrics
   - Review overnight fraud patterns in heatmap
   - Adjust threshold if needed

2. **Investigation workflow**:
   - Use Fraud Deep Dive for suspicious cases
   - Always check SHAP explanation before final decision
   - Document reasons for overrides

3. **Performance monitoring**:
   - Weekly review of Model Performance tab
   - Track false positive rate trend
   - Retrain model if metrics degrade

### For Demonstrations
1. Start with **Executive Summary** to show business value
2. Run **Live Monitoring** simulation for impact
3. Use **Fraud Deep Dive** to show practical usage
4. Show **SHAP explanations** to demonstrate transparency
5. End with **Model Performance** to prove accuracy

### For Model Tuning
1. Monitor confusion matrix for imbalance
2. Adjust fraud threshold based on business priorities:
   - Financial services → lower threshold (catch more fraud)
   - E-commerce → higher threshold (reduce friction)
3. Review global SHAP to identify underutilized features

---

## 🔧 Customization Options

### Adjusting the Fraud Threshold
Located in the sidebar:
- **Default**: 0.75 (75% probability)
- **Conservative** (catch more fraud): 0.60-0.70
- **Balanced**: 0.75-0.80
- **Precision-focused** (fewer false alarms): 0.85-0.95

**Effect on metrics**:
- Lower threshold → Higher recall, more false positives
- Higher threshold → Higher precision, might miss some fraud

### Mock Data vs. Real Data
Current implementation uses simulated data for:
- Live transaction feed
- Heatmap patterns
- Performance metrics

**To connect to real data**:
1. Replace mock data generators with database queries
2. Connect to live transaction stream for monitoring
3. Load actual model metrics from MLflow/training logs
4. Update SHAP values from model's saved explainer

---

## ❓ FAQ

**Q: Why isn't the API connecting?**
A: Make sure you've started the FastAPI server first: `make run_api`

**Q: Can I change the threshold permanently?**
A: Yes, edit `FRAUD_THRESHOLD` in `src/config.py` (currently 0.75)

**Q: Where does the training data come from?**
A: `raw_data/Base.csv` - Feedzai banking transaction dataset

**Q: How often should I retrain the model?**
A: Monitor performance metrics monthly. Retrain if:
- Fraud patterns change
- False positive rate increases
- New fraud types emerge

**Q: Can I export the dashboards?**
A: Use Streamlit's built-in screenshot feature or integrate with reporting tools

**Q: Is this production-ready?**
A: The model and API are production-ready. Dashboard requires:
- Real-time data connection
- Authentication/authorization
- Audit logging
- User management

---

## 🚀 Next Steps

1. **Connect to real data**: Replace mock data with live database
2. **Add authentication**: Implement user login and role-based access
3. **Enable alerts**: Email/Slack notifications for high-risk transactions
4. **A/B testing**: Test different thresholds with champion/challenger models
5. **Expand features**: Add customer feedback loop, case management
6. **Deploy**: Containerize with Docker and deploy to cloud

---

## 📞 Support

For issues or questions:
- Check the main [README.md](README.md)
- Review the notebooks for model details
- Inspect `src/config.py` for feature definitions

---

**ShieldBank Version**: 2.0
**Last Updated**: February 2026
**Status**: Ready for deployment 🛡️
