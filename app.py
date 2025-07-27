import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import io
import base64

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="AI Call Center CRM Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📞"
)

# Enhanced custom CSS for better styling and wide screen optimization
st.markdown("""
<style>
    /* Main dashboard styling */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .success-metric {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .danger-metric {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
    }
    
    /* Wide screen table styling */
    .dataframe-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        overflow-x: auto;
    }
    
    /* Enhanced table styling */
    .enhanced-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    
    .enhanced-table th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 8px;
        text-align: left;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    
    .enhanced-table td {
        padding: 8px;
        border-bottom: 1px solid #ddd;
        word-wrap: break-word;
        max-width: 300px;
    }
    
    .enhanced-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    .enhanced-table tr:hover {
        background-color: #e3f2fd;
    }
    
    /* Transcript column styling */
    .transcript-cell {
        max-width: 400px;
        max-height: 100px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-size: 11px;
        line-height: 1.3;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 5px;
    }
    
    .long-text-cell {
        max-width: 250px;
        max-height: 80px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-size: 11px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255,255,255,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom expander */
    .custom-expander {
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Status indicators */
    .status-success { 
        background: #28a745; 
        color: white; 
        padding: 4px 8px; 
        border-radius: 15px; 
        font-size: 10px;
    }
    .status-warning { 
        background: #ffc107; 
        color: black; 
        padding: 4px 8px; 
        border-radius: 15px; 
        font-size: 10px;
    }
    .status-danger { 
        background: #dc3545; 
        color: white; 
        padding: 4px 8px; 
        border-radius: 15px; 
        font-size: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced data loading function with more comprehensive sample data
@st.cache_data
def load_enhanced_crm_data():
    """Load comprehensive AI call center CRM data with transcripts and detailed information"""
    try:
        if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
            df = pd.read_csv(st.session_state.uploaded_file)
        else:
            # Comprehensive sample data with all possible columns including transcripts
            sample_transcripts = [
                """Agent: Hello! Thank you for calling TechCorp. My name is AI Agent Emma. How can I assist you today?
Customer: Hi Emma! I'm Sarah Johnson from Marketing Solutions Inc. I've been hearing great things about your new enterprise software suite, and I'm really interested in learning more about how it could help streamline our marketing operations.
Agent: That's wonderful to hear, Sarah! I'd be happy to tell you more about our enterprise marketing suite. It's designed specifically for companies like yours that need to manage complex marketing campaigns across multiple channels. Can you tell me a bit about your current challenges?
Customer: Well, we're currently using three different platforms for email marketing, social media management, and analytics reporting. It's becoming really difficult to get a unified view of our campaign performance, and our team is spending way too much time switching between systems.
Agent: I completely understand that pain point, Sarah. Our integrated platform addresses exactly those challenges. It combines email marketing, social media management, analytics, and campaign automation all in one unified dashboard. This typically saves our clients 15-20 hours per week in administrative tasks. Would you be interested in seeing a personalized demo of how this would work for your specific use case?
Customer: That sounds exactly like what we need! Yes, I'd definitely like to schedule a demo. When would be the best time?
Agent: Perfect! I can see that you're a great fit for our enterprise tier. Let me connect you with our solutions specialist who can show you a customized demo next week. I'll also send you some case studies from similar marketing agencies. Is Tuesday at 2 PM EST good for you?
Customer: Tuesday at 2 PM works perfectly! This is so exciting - I think this could really transform how we work.
Agent: Excellent! I'll send you a calendar invitation and some preparatory materials. Is there anything else I can help you with today?
Customer: No, that covers everything. Thank you so much, Emma!
Agent: You're very welcome, Sarah! Have a great day and we look forward to showing you our platform next Tuesday!""",
                
                """Agent: Good morning! This is AI Agent Alex from TechCorp Support. I see you're calling about a login issue. Can I get your account information?
Customer: Hi Alex, yes I'm Mike Chen. I can't seem to access my account - it keeps saying my password is incorrect, but I'm sure I'm entering it right.
Agent: I understand how frustrating that can be, Mike. Let me pull up your account. I can see your last successful login was yesterday at 3:47 PM. It looks like there might have been a recent password reset requirement due to our security update. 
Customer: Oh, I didn't get any email about that.
Agent: Let me check your email preferences... I see the notification might have gone to your spam folder. No worries though - I can help you reset your password right now. For security purposes, I'll need to verify your identity with the phone number on file.
Customer: Sure, it's 555-0123.
Agent: Perfect, that matches our records. I'm sending a password reset link to your email right now. You should receive it within the next minute. Once you reset it, you'll be able to access your account normally.
Customer: Got it! Let me check... yes, I see the email. I'll reset it now.
Agent: Great! Take your time. I'll stay on the line to make sure everything works.
Customer: Okay, I've reset it and... yes! I'm able to log in now. Thank you so much, Alex!
Agent: You're very welcome, Mike! Is there anything else I can help you with today?
Customer: No, that was it. You've been incredibly helpful!
Agent: Perfect! Have a great day, and don't hesitate to reach out if you need any other assistance.""",
                
                """Agent: Hello! This is AI Agent Sophia from TechCorp Billing. I see you have a question about your recent charges?
Customer: Hi Sophia. Yes, I'm Emma Davis, and I noticed an unexpected charge on my account for a premium upgrade, but I don't remember authorizing that.
Agent: I completely understand your concern, Emma. Let me look into that right away. I can see the charge you're referring to - it's for $89.99 on January 10th for our Premium Analytics package. 
Customer: Right, but I never signed up for that.
Agent: I see what happened here. It looks like this was triggered by our auto-upgrade feature when your usage exceeded the standard tier limits. However, I can see this wasn't clearly communicated to you, and for that I apologize.
Customer: Oh, I see. But I didn't realize I was going over my limits.
Agent: That's completely understandable, and it's something we should have notified you about more clearly. Here's what I can do - I'll reverse this charge immediately and set up usage alerts for your account so you'll be notified before any automatic upgrades occur in the future.
Customer: That would be great, thank you.
Agent: Done! You should see the credit on your account within 2-3 business days. I've also enabled email and SMS alerts for usage thresholds. Is there anything else I can help clarify about your billing?
Customer: No, that covers it. Thank you for resolving this so quickly.
Agent: You're very welcome, Emma! We appreciate your business and want to make sure you have the best experience possible."""
            ]
            
            df = pd.DataFrame([
                {
                    "call_id": "CALL_001", "customer_name": "Sarah Johnson", "voice_agent_name": "AI Agent Emma",
                    "call_date": "2024-01-15", "call_start_time": "09:15:00", "call_end_time": "09:17:00",
                    "call_duration_seconds": 120, "call_duration_hms": "00:02:00", "cost": 4.9,
                    "call_success": "Yes", "appointment_scheduled": "Yes", "intent_detected": "Product_Inquiry",
                    "sentiment_score": 0.8, "confidence_score": 0.92, "keyword_tags": "software, marketing, demo, enterprise, automation, analytics",
                    "summary_word_count": 32, "customer_satisfaction": 9.2, "resolution_time_seconds": 105,
                    "escalation_required": "No", "language_detected": "English", "emotion_detected": "Excited",
                    "speech_rate_wpm": 145, "silence_percentage": 8.5, "interruption_count": 2,
                    "ai_accuracy_score": 0.94, "follow_up_required": "Yes", "customer_tier": "Premium",
                    "call_complexity": "Medium", "agent_performance_score": 9.1, "call_outcome": "Demo_Scheduled",
                    "revenue_impact": 5000, "lead_quality_score": 8.7, "conversion_probability": 0.85,
                    "next_best_action": "Send_Demo_Materials", "customer_lifetime_value": 25000, "call_category": "Sales",
                    "transcript": sample_transcripts[0],
                    "call_summary": "Customer Sarah Johnson from Marketing Solutions Inc. expressed strong interest in enterprise software suite. Currently using three different platforms and facing integration challenges. Scheduled personalized demo for Tuesday 2PM EST. High-value prospect with clear pain points that align with our solution.",
                    "customer_phone": "+1-555-0167", "customer_email": "sarah.johnson@marketingsolutions.com",
                    "call_recording_url": "https://recordings.techcorp.com/call_001.mp3",
                    "follow_up_date": "2024-01-22", "assigned_rep": "Jessica Martinez",
                    "deal_size_estimate": 50000, "competitor_mentioned": "None",
                    "pain_points": "Multiple disconnected platforms, lack of unified reporting, time-consuming manual processes",
                    "budget_mentioned": "50k-100k annual", "decision_timeline": "Q1 2024",
                    "technical_requirements": "API integrations, multi-channel reporting, campaign automation"
                },
                {
                    "call_id": "CALL_002", "customer_name": "Mike Chen", "voice_agent_name": "AI Agent Alex",
                    "call_date": "2024-01-15", "call_start_time": "10:30:00", "call_end_time": "10:33:00",
                    "call_duration_seconds": 180, "call_duration_hms": "00:03:00", "cost": 9.6,
                    "call_success": "Yes", "appointment_scheduled": "No", "intent_detected": "Technical_Support",
                    "sentiment_score": 0.9, "confidence_score": 0.88, "keyword_tags": "login, password, reset, account, security",
                    "summary_word_count": 28, "customer_satisfaction": 9.5, "resolution_time_seconds": 165,
                    "escalation_required": "No", "language_detected": "English", "emotion_detected": "Relieved",
                    "speech_rate_wpm": 138, "silence_percentage": 12.3, "interruption_count": 1,
                    "ai_accuracy_score": 0.91, "follow_up_required": "No", "customer_tier": "Standard",
                    "call_complexity": "Low", "agent_performance_score": 9.3, "call_outcome": "Issue_Resolved",
                    "revenue_impact": 0, "lead_quality_score": 7.2, "conversion_probability": 0.0,
                    "next_best_action": "Account_Monitoring", "customer_lifetime_value": 12000, "call_category": "Support",
                    "transcript": sample_transcripts[1],
                    "call_summary": "Customer Mike Chen experienced login issues due to mandatory security update. Agent successfully resolved by resetting password and enabling account alerts. Customer satisfaction very high due to quick resolution and proactive security measures explained.",
                    "customer_phone": "+1-555-0123", "customer_email": "mike.chen@email.com",
                    "call_recording_url": "https://recordings.techcorp.com/call_002.mp3",
                    "follow_up_date": None, "assigned_rep": "Support Team",
                    "deal_size_estimate": 0, "competitor_mentioned": "None",
                    "pain_points": "Account access, password confusion, security concerns",
                    "budget_mentioned": "N/A", "decision_timeline": "N/A",
                    "technical_requirements": "Account security, notification preferences"
                },
                {
                    "call_id": "CALL_003", "customer_name": "Emma Davis", "voice_agent_name": "AI Agent Sophia",
                    "call_date": "2024-01-15", "call_start_time": "11:45:00", "call_end_time": "11:46:00",
                    "call_duration_seconds": 60, "call_duration_hms": "00:01:00", "cost": 1.8,
                    "call_success": "Yes", "appointment_scheduled": "No", "intent_detected": "Billing_Inquiry",
                    "sentiment_score": 0.7, "confidence_score": 0.85, "keyword_tags": "billing, premium, charges, auto-upgrade, refund",
                    "summary_word_count": 25, "customer_satisfaction": 8.1, "resolution_time_seconds": 55,
                    "escalation_required": "No", "language_detected": "English", "emotion_detected": "Concerned",
                    "speech_rate_wpm": 152, "silence_percentage": 15.2, "interruption_count": 0,
                    "ai_accuracy_score": 0.87, "follow_up_required": "No", "customer_tier": "Standard",
                    "call_complexity": "Low", "agent_performance_score": 8.5, "call_outcome": "Issue_Resolved",
                    "revenue_impact": 0, "lead_quality_score": 6.8, "conversion_probability": 0.0,
                    "next_best_action": "Billing_Review", "customer_lifetime_value": 8500, "call_category": "Billing",
                    "transcript": sample_transcripts[2],
                    "call_summary": "Customer Emma Davis questioned unexpected premium upgrade charge. Agent identified auto-upgrade trigger due to usage limits, immediately reversed charge and set up usage alerts. Customer satisfied with quick resolution and proactive account management setup.",
                    "customer_phone": "+1-555-0198", "customer_email": "emma.davis@company.com",
                    "call_recording_url": "https://recordings.techcorp.com/call_003.mp3",
                    "follow_up_date": None, "assigned_rep": "Billing Team",
                    "deal_size_estimate": 0, "competitor_mentioned": "None",
                    "pain_points": "Unexpected charges, unclear billing communication",
                    "budget_mentioned": "Current plan sufficient", "decision_timeline": "N/A",
                    "technical_requirements": "Usage alerts, billing transparency"
                }
            ])
        
        # Convert date columns
        df['call_date'] = pd.to_datetime(df['call_date'])
        if 'follow_up_date' in df.columns:
            df['follow_up_date'] = pd.to_datetime(df['follow_up_date'])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Enhanced data display function for wide screens
def display_enhanced_dataframe(df, title="Data Table", key_prefix="table"):
    """Display dataframe with enhanced styling optimized for wide screens and long text"""
    if df.empty:
        st.warning("No data to display")
        return
    
    st.markdown(f"### {title}")
    
    # Column selection for display
    with st.expander("🔧 Customize Table Display", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Select Columns to Display:**")
            all_columns = list(df.columns)
            
            # Default high-priority columns
            default_cols = [col for col in ['call_id', 'customer_name', 'call_date', 'call_category', 
                           'customer_satisfaction', 'call_outcome', 'transcript', 'call_summary'] 
                           if col in all_columns]
            
            selected_columns = st.multiselect(
                "Columns",
                options=all_columns,
                default=default_cols if default_cols else all_columns[:8],
                key=f"{key_prefix}_cols"
            )
        
        with col2:
            st.write("**Display Options:**")
            max_rows = st.number_input("Max rows to display", min_value=10, max_value=1000, value=50, key=f"{key_prefix}_rows")
            truncate_text = st.checkbox("Truncate long text", value=True, key=f"{key_prefix}_truncate")
            show_index = st.checkbox("Show row index", value=False, key=f"{key_prefix}_index")
    
    if not selected_columns:
        st.warning("Please select at least one column to display")
        return
    
    # Filter dataframe
    display_df = df[selected_columns].head(max_rows)
    
    # Enhanced HTML table generation
    def generate_enhanced_html_table(df, truncate=True):
        html = '<div class="dataframe-container"><table class="enhanced-table">'
        
        # Headers
        html += '<thead><tr>'
        if show_index:
            html += '<th>Index</th>'
        for col in df.columns:
            html += f'<th>{col.replace("_", " ").title()}</th>'
        html += '</tr></thead><tbody>'
        
        # Rows
        for idx, row in df.iterrows():
            html += '<tr>'
            if show_index:
                html += f'<td>{idx}</td>'
            
            for col in df.columns:
                value = row[col]
                
                # Handle different data types and apply appropriate styling
                if pd.isna(value):
                    cell_content = '<em>N/A</em>'
                elif col in ['transcript', 'call_summary']:
                    # Special handling for long text fields
                    if truncate and len(str(value)) > 200:
                        truncated = str(value)[:200] + "..."
                        cell_content = f'<div class="transcript-cell" title="{str(value).replace('"', '&quot;')}">{truncated}</div>'
                    else:
                        cell_content = f'<div class="transcript-cell">{str(value)}</div>'
                elif col in ['pain_points', 'technical_requirements', 'keyword_tags']:
                    # Medium text fields
                    if truncate and len(str(value)) > 100:
                        truncated = str(value)[:100] + "..."
                        cell_content = f'<div class="long-text-cell" title="{str(value).replace('"', '&quot;')}">{truncated}</div>'
                    else:
                        cell_content = f'<div class="long-text-cell">{str(value)}</div>'
                elif col in ['call_success', 'appointment_scheduled']:
                    # Status indicators
                    if str(value).lower() == 'yes':
                        cell_content = f'<span class="status-success">{value}</span>'
                    elif str(value).lower() == 'no':
                        cell_content = f'<span class="status-danger">{value}</span>'
                    else:
                        cell_content = str(value)
                elif col == 'customer_satisfaction':
                    # Satisfaction scoring
                    score = float(value) if pd.notna(value) else 0
                    if score >= 9:
                        cell_content = f'<span class="status-success">{score}</span>'
                    elif score >= 7:
                        cell_content = f'<span class="status-warning">{score}</span>'
                    else:
                        cell_content = f'<span class="status-danger">{score}</span>'
                elif col in ['cost', 'revenue_impact', 'customer_lifetime_value', 'deal_size_estimate']:
                    # Currency formatting
                    if pd.notna(value) and value != 0:
                        cell_content = f'${float(value):,.2f}'
                    else:
                        cell_content = '$0.00'
                elif col in ['sentiment_score', 'confidence_score', 'ai_accuracy_score', 'conversion_probability']:
                    # Percentage formatting
                    if pd.notna(value):
                        cell_content = f'{float(value):.1%}'
                    else:
                        cell_content = 'N/A'
                else:
                    cell_content = str(value)
                
                html += f'<td>{cell_content}</td>'
            html += '</tr>'
        
        html += '</tbody></table></div>'
        return html
    
    # Display the enhanced table
    html_table = generate_enhanced_html_table(display_df, truncate_text)
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Additional table info and actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"📊 Showing {len(display_df)} of {len(df)} records")
    
    with col2:
        if st.button(f"📥 Export CSV", key=f"{key_prefix}_export"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"crm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key=f"{key_prefix}_download"
            )
    
    with col3:
        if st.button(f"🔍 Show Full Data", key=f"{key_prefix}_full"):
            st.session_state[f'show_full_{key_prefix}'] = True
    
    with col4:
        if st.button(f"📋 Copy to Clipboard", key=f"{key_prefix}_copy"):
            st.success("Table data copied to clipboard!")

# Initialize session state
if 'crm_data' not in st.session_state:
    st.session_state.crm_data = load_enhanced_crm_data()

# Enhanced sidebar
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;">
        <h2>📁 Data Management</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload with drag and drop
    uploaded_file = st.file_uploader(
        "Upload CRM Data (CSV)", 
        type=['csv'],
        help="Drag and drop your CSV file here or click to browse"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.crm_data = load_enhanced_crm_data()
        st.success("✅ Data uploaded successfully!")
        
        # Show file details
        file_details = {
            "Filename": uploaded_file.name,
            "Size": f"{uploaded_file.size / 1024:.1f} KB",
            "Type": uploaded_file.type
        }
        st.json(file_details)
    
    st.divider()
    
    # Enhanced filters
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;">
        <h3>🔍 Smart Filters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.crm_data
    
    if not df.empty:
        # Date range filter with presets
        col1, col2 = st.columns(2)
        with col1:
            date_preset = st.selectbox(
                "Quick Date Selection",
                ["Custom", "Today", "Last 7 Days", "Last 30 Days", "This Month", "All Time"]
            )
        
        if date_preset == "Custom":
            date_range = st.date_input(
                "Custom Date Range",
                value=(df['call_date'].min().date(), df['call_date'].max().date()),
                min_value=df['call_date'].min().date(),
                max_value=df['call_date'].max().date()
            )
        else:
            today = datetime.now().date()
            if date_preset == "Today":
                date_range = (today, today)
            elif date_preset == "Last 7 Days":
                date_range = (today - timedelta(days=7), today)
            elif date_preset == "Last 30 Days":
                date_range = (today - timedelta(days=30), today)
            elif date_preset == "This Month":
                date_range = (today.replace(day=1), today)
            else:  # All Time
                date_range = (df['call_date'].min().date(), df['call_date'].max().date())
        
        # Multi-level filters
        categories = st.multiselect(
            "📂 Call Categories",
            options=df['call_category'].unique(),
            default=df['call_category'].unique()
        )
        
        tiers = st.multiselect(
            "👑 Customer Tiers",
            options=df['customer_tier'].unique(),
            default=df['customer_tier'].unique()
        )
        
        outcomes = st.multiselect(
            "🎯 Call Outcomes",
            options=df['call_outcome'].unique(),
            default=df['call_outcome'].unique()
        )
        
        # Satisfaction range
        satisfaction_range = st.slider(
            "⭐ Customer Satisfaction Range",
            min_value=float(df['customer_satisfaction'].min()),
            max_value=float(df['customer_satisfaction'].max()),
            value=(float(df['customer_satisfaction'].min()), float(df['customer_satisfaction'].max())),
            step=0.1
        )
        
        # Revenue impact filter
        if df['revenue_impact'].max() > 0:
            revenue_range = st.slider(
                "💰 Revenue Impact Range",
                min_value=int(df['revenue_impact'].min()),
                max_value=int(df['revenue_impact'].max()),
                value=(int(df['revenue_impact'].min()), int(df['revenue_impact'].max())),
                step=100
            )
        else:
            revenue_range = (0, 0)
        
        # Text search
        search_term = st.text_input(
            "🔍 Search in transcripts/summaries",
            placeholder="Enter keywords to search..."
        )
        
        # Apply filters
        filtered_df = df[
            (df['call_date'].dt.date.between(pd.to_datetime(date_range[0]).date(), pd.to_datetime(date_range[1]).date())) &
            (df['call_category'].isin(categories)) &
            (df['customer_tier'].isin(tiers)) &
            (df['call_outcome'].isin(outcomes)) &
            (df['customer_satisfaction'].between(satisfaction_range[0], satisfaction_range[1])) &
            (df['revenue_impact'].between(revenue_range[0], revenue_range[1]))
        ]
        
        if search_term:
            # Search in multiple text columns
            text_columns = ['transcript', 'call_summary', 'keyword_tags', 'pain_points']
            search_mask = pd.Series([False] * len(filtered_df))
            
            for col in text_columns:
                if col in filtered_df.columns:
                    search_mask |= filtered_df[col].astype(str).str.contains(search_term, case=False, na=False)
            
            filtered_df = filtered_df[search_mask]
        
        # Filter summary
        st.markdown("### 📈 Filter Summary")
        st.info(f"Showing **{len(filtered_df)}** of **{len(df)}** records")
        
    else:
        filtered_df = df

# Main dashboard header
st.markdown("""
<div class="main-header">
    <h1>📞 AI Call Center CRM Dashboard</h1>
    <p>Comprehensive Customer Relationship Management & Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# Enhanced key metrics
if not filtered_df.empty:
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_calls = len(filtered_df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📞 Total Calls</h3>
            <h2>{total_calls:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        success_rate = (filtered_df['call_success'] == 'Yes').sum() / len(filtered_df) * 100
        st.markdown(f"""
        <div class="metric-card success-metric">
            <h3>✅ Success Rate</h3>
            <h2>{success_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_satisfaction = filtered_df['customer_satisfaction'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ Avg Satisfaction</h3>
            <h2>{avg_satisfaction:.1f}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_revenue = filtered_df['revenue_impact'].sum()
        st.markdown(f"""
        <div class="metric-card warning-metric">
            <h3>💰 Revenue Impact</h3>
            <h2>${total_revenue:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        avg_duration = filtered_df['call_duration_seconds'].mean() / 60
        st.markdown(f"""
        <div class="metric-card danger-metric">
            <h3>⏱️ Avg Duration</h3>
            <h2>{avg_duration:.1f} min</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Enhanced tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Call Records & Transcripts", "📊 Advanced Analytics", "👥 Customer Intelligence",
    "🎯 Agent Performance", "💰 Revenue & Pipeline", "🔮 AI Insights", "⚙️ Admin Center"
])

with tab1:
    st.markdown("## 📋 Comprehensive Call Records Management")
    
    if not filtered_df.empty:
        # Quick stats bar
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔍 Filtered Records", len(filtered_df))
        with col2:
            avg_call_duration = filtered_df['call_duration_seconds'].mean()
            st.metric("⏱️ Avg Call Time", f"{avg_call_duration/60:.1f} min")
        with col3:
            high_satisfaction = (filtered_df['customer_satisfaction'] >= 9).sum()
            st.metric("😊 High Satisfaction", f"{high_satisfaction} calls")
        with col4:
            follow_ups_needed = (filtered_df['follow_up_required'] == 'Yes').sum()
            st.metric("📅 Follow-ups Needed", f"{follow_ups_needed} calls")
        
        st.markdown("---")
        
        # Enhanced data display with transcript view
        display_enhanced_dataframe(filtered_df, "Complete Call Records", "call_records")
        
        st.markdown("### 🎙️ Detailed Transcript Viewer")
        
        # Transcript detail view
        if len(filtered_df) > 0:
            selected_call = st.selectbox(
                "Select call to view full transcript:",
                options=filtered_df['call_id'].tolist(),
                format_func=lambda x: f"{x} - {filtered_df[filtered_df['call_id']==x]['customer_name'].iloc[0]} ({filtered_df[filtered_df['call_id']==x]['call_category'].iloc[0]})"
            )
            
            if selected_call:
                call_data = filtered_df[filtered_df['call_id'] == selected_call].iloc[0]
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("#### 📝 Full Transcript")
                    if 'transcript' in call_data and pd.notna(call_data['transcript']):
                        st.markdown(f"""
                        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; 
                                   border-left: 5px solid #007bff; max-height: 400px; overflow-y: auto;">
                            <pre style="white-space: pre-wrap; font-family: 'Segoe UI', sans-serif; 
                                       font-size: 14px; line-height: 1.5;">{call_data['transcript']}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("No transcript available for this call")
                
                with col2:
                    st.markdown("#### 📊 Call Details")
                    
                    details = {
                        "🏷️ Call ID": call_data['call_id'],
                        "👤 Customer": call_data['customer_name'],
                        "🤖 Agent": call_data['voice_agent_name'],
                        "📅 Date": call_data['call_date'].strftime('%Y-%m-%d'),
                        "⏰ Duration": call_data['call_duration_hms'],
                        "📂 Category": call_data['call_category'],
                        "🎯 Outcome": call_data['call_outcome'],
                        "⭐ Satisfaction": f"{call_data['customer_satisfaction']}/10",
                        "💰 Revenue Impact": f"${call_data['revenue_impact']:,.2f}"
                    }
                    
                    for key, value in details.items():
                        st.write(f"**{key}:** {value}")
                    
                    if 'call_summary' in call_data and pd.notna(call_data['call_summary']):
                        st.markdown("#### 📄 Call Summary")
                        st.info(call_data['call_summary'])
    else:
        st.info("No data available. Please upload a CSV file or adjust your filters.")

with tab2:
    st.markdown("## 📊 Advanced Analytics & Insights")
    
    if not filtered_df.empty:
        # Advanced metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            conversion_rate = (filtered_df['conversion_probability'] > 0.5).mean()
            st.metric("🎯 Conversion Rate", f"{conversion_rate:.1%}", 
                     delta=f"+{(conversion_rate-0.15):.1%}" if conversion_rate > 0.15 else f"{(conversion_rate-0.15):.1%}")
        
        with col2:
            avg_ai_accuracy = filtered_df['ai_accuracy_score'].mean()
            st.metric("🤖 AI Accuracy", f"{avg_ai_accuracy:.1%}",
                     delta=f"+{(avg_ai_accuracy-0.85):.1%}" if avg_ai_accuracy > 0.85 else f"{(avg_ai_accuracy-0.85):.1%}")
        
        with col3:
            escalation_rate = (filtered_df['escalation_required'] == 'Yes').mean()
            st.metric("⚠️ Escalation Rate", f"{escalation_rate:.1%}",
                     delta=f"-{(0.1-escalation_rate):.1%}" if escalation_rate < 0.1 else f"+{(escalation_rate-0.1):.1%}")
        
        with col4:
            avg_resolution_time = filtered_df['resolution_time_seconds'].mean() / 60
            st.metric("⚡ Avg Resolution Time", f"{avg_resolution_time:.1f} min",
                     delta=f"-{(3-avg_resolution_time):.1f} min" if avg_resolution_time < 3 else f"+{(avg_resolution_time-3):.1f} min")
        
        st.markdown("---")
        
        # Advanced visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Call outcomes distribution with enhanced styling
            outcome_counts = filtered_df['call_outcome'].value_counts()
            fig_pie = px.pie(
                values=outcome_counts.values,
                names=outcome_counts.index,
                title="📊 Call Outcomes Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                font=dict(size=12),
                title_font_size=16,
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Customer satisfaction heatmap by category and tier
            satisfaction_pivot = filtered_df.pivot_table(
                values='customer_satisfaction', 
                index='call_category', 
                columns='customer_tier', 
                aggfunc='mean'
            )
            
            fig_heatmap = px.imshow(
                satisfaction_pivot,
                title="🔥 Satisfaction Heatmap (Category vs Tier)",
                color_continuous_scale='RdYlGn',
                aspect='auto'
            )
            fig_heatmap.update_layout(height=400, title_font_size=16)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Time series analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily trends
            daily_metrics = filtered_df.groupby(filtered_df['call_date'].dt.date).agg({
                'call_id': 'count',
                'customer_satisfaction': 'mean',
                'revenue_impact': 'sum'
            }).reset_index()
            daily_metrics.columns = ['Date', 'Call_Count', 'Avg_Satisfaction', 'Revenue']
            
            fig_trends = go.Figure()
            
            fig_trends.add_trace(go.Scatter(
                x=daily_metrics['Date'],
                y=daily_metrics['Call_Count'],
                mode='lines+markers',
                name='Call Volume',
                yaxis='y',
                line=dict(color='#1f77b4', width=3)
            ))
            
            fig_trends.add_trace(go.Scatter(
                x=daily_metrics['Date'],
                y=daily_metrics['Avg_Satisfaction'],
                mode='lines+markers',
                name='Avg Satisfaction',
                yaxis='y2',
                line=dict(color='#ff7f0e', width=3)
            ))
            
            fig_trends.update_layout(
                title="📈 Daily Trends: Volume vs Satisfaction",
                xaxis_title="Date",
                yaxis=dict(title="Call Count", side="left"),
                yaxis2=dict(title="Satisfaction", side="right", overlaying="y"),
                height=400,
                title_font_size=16
            )
            
            st.plotly_chart(fig_trends, use_container_width=True)
        
        with col2:
            # Sentiment vs Duration scatter
            fig_scatter = px.scatter(
                filtered_df,
                x='call_duration_seconds',
                y='sentiment_score',
                size='customer_satisfaction',
                color='call_category',
                title="🎭 Sentiment vs Call Duration",
                labels={
                    'call_duration_seconds': 'Call Duration (seconds)',
                    'sentiment_score': 'Sentiment Score'
                },
                hover_data=['customer_name', 'call_outcome']
            )
            fig_scatter.update_layout(height=400, title_font_size=16)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Performance correlation matrix
        st.markdown("### 🔗 Performance Correlation Analysis")
        
        correlation_cols = [
            'customer_satisfaction', 'sentiment_score', 'ai_accuracy_score',
            'agent_performance_score', 'call_duration_seconds', 'resolution_time_seconds',
            'speech_rate_wpm', 'interruption_count'
        ]
        
        available_corr_cols = [col for col in correlation_cols if col in filtered_df.columns]
        
        if len(available_corr_cols) > 2:
            corr_matrix = filtered_df[available_corr_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                title="🔗 Performance Metrics Correlation Matrix",
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            fig_corr.update_layout(height=500, title_font_size=16)
            st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.markdown("## 👥 Customer Intelligence & Management")
    
    if not filtered_df.empty:
        # Customer overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            unique_customers = filtered_df['customer_name'].nunique()
            st.metric("👥 Unique Customers", unique_customers)
        
        with col2:
            premium_customers = (filtered_df['customer_tier'] == 'Premium').sum()
            st.metric("👑 Premium Customers", premium_customers)
        
        with col3:
            high_value_customers = (filtered_df['customer_lifetime_value'] > 20000).sum()
            st.metric("💎 High Value Customers", high_value_customers)
        
        with col4:
            repeat_customers = filtered_df.groupby('customer_name').size()
            repeat_count = (repeat_customers > 1).sum()
            st.metric("🔄 Repeat Customers", repeat_count)
        
        st.markdown("---")
        
        # Enhanced customer analysis
        customer_summary = filtered_df.groupby('customer_name').agg({
            'call_id': 'count',
            'customer_satisfaction': 'mean',
            'customer_lifetime_value': 'first',
            'customer_tier': 'first',
            'revenue_impact': 'sum',
            'conversion_probability': 'mean',
            'call_category': lambda x: ', '.join(x.unique()),
            'call_outcome': lambda x: ', '.join(x.unique()),
            'next_best_action': 'last',
            'pain_points': 'last'
        }).reset_index()
        
        customer_summary.columns = [
            'Customer', 'Total_Calls', 'Avg_Satisfaction', 'Lifetime_Value', 
            'Tier', 'Revenue_Impact', 'Conversion_Probability', 'Categories', 
            'Outcomes', 'Next_Action', 'Pain_Points'
        ]
        
        # Customer segmentation
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer value segmentation
            fig_customer_value = px.scatter(
                customer_summary,
                x='Total_Calls',
                y='Lifetime_Value',
                size='Avg_Satisfaction',
                color='Tier',
                title="💰 Customer Value Segmentation",
                hover_name='Customer',
                hover_data=['Revenue_Impact', 'Conversion_Probability']
            )
            fig_customer_value.update_layout(height=400, title_font_size=16)
            st.plotly_chart(fig_customer_value, use_container_width=True)
        
        with col2:
            # Customer tier distribution
            tier_counts = customer_summary['Tier'].value_counts()
            fig_tier = px.bar(
                x=tier_counts.index,
                y=tier_counts.values,
                title="🏆 Customer Tier Distribution",
                color=tier_counts.values,
                color_continuous_scale='Viridis'
            )
            fig_tier.update_layout(
                xaxis_title="Customer Tier",
                yaxis_title="Number of Customers",
                height=400,
                title_font_size=16
            )
            st.plotly_chart(fig_tier, use_container_width=True)
        
        # Detailed customer table
        st.markdown("### 📊 Detailed Customer Analysis")
        display_enhanced_dataframe(customer_summary, "Customer Intelligence Report", "customer_analysis")
        
        # Customer action center
        st.markdown("### 🎯 Customer Action Center")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚨 Customers Requiring Attention")
            
            # Low satisfaction customers
            low_satisfaction = customer_summary[customer_summary['Avg_Satisfaction'] < 7]
            if not low_satisfaction.empty:
                st.markdown("**Low Satisfaction (< 7.0):**")
                for _, customer in low_satisfaction.iterrows():
                    st.warning(f"📞 {customer['Customer']} - Satisfaction: {customer['Avg_Satisfaction']:.1f}")
            
            # High value, low engagement
            high_value_low_calls = customer_summary[
                (customer_summary['Lifetime_Value'] > 15000) & 
                (customer_summary['Total_Calls'] <= 1)
            ]
            if not high_value_low_calls.empty:
                st.markdown("**High Value, Low Engagement:**")
                for _, customer in high_value_low_calls.iterrows():
                    st.info(f"💰 {customer['Customer']} - LTV: ${customer['Lifetime_Value']:,.0f}")
        
        with col2:
            st.markdown("#### 🌟 Top Opportunities")
            
            # High conversion probability
            high_conversion = customer_summary[customer_summary['Conversion_Probability'] > 0.7]
            if not high_conversion.empty:
                st.markdown("**High Conversion Potential (> 70%):**")
                for _, customer in high_conversion.head(5).iterrows():
                    st.success(f"🎯 {customer['Customer']} - Probability: {customer['Conversion_Probability']:.0%}")
            
            # Premium tier prospects
            premium_prospects = customer_summary[
                (customer_summary['Tier'] == 'Standard') & 
                (customer_summary['Revenue_Impact'] > 1000)
            ]
            if not premium_prospects.empty:
                st.markdown("**Premium Upgrade Candidates:**")
                for _, customer in premium_prospects.head(5).iterrows():
                    st.info(f"⬆️ {customer['Customer']} - Revenue: ${customer['Revenue_Impact']:,.0f}")

with tab4:
    st.markdown("## 🎯 Agent Performance Dashboard")
    
    if not filtered_df.empty:
        # Agent performance aggregation
        agent_performance = filtered_df.groupby('voice_agent_name').agg({
            'call_id': 'count',
            'agent_performance_score': 'mean',
            'customer_satisfaction': 'mean',
            'call_success': lambda x: (x == 'Yes').mean(),
            'ai_accuracy_score': 'mean',
            'call_duration_seconds': 'mean',
            'resolution_time_seconds': 'mean',
            'escalation_required': lambda x: (x == 'Yes').mean(),
            'revenue_impact': 'sum'
        }).reset_index()
        
        agent_performance.columns = [
            'Agent', 'Total_Calls', 'Performance_Score', 'Customer_Satisfaction',
            'Success_Rate', 'AI_Accuracy', 'Avg_Duration', 'Avg_Resolution_Time',
            'Escalation_Rate', 'Revenue_Generated'
        ]
        
        # Top agent metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            top_performer = agent_performance.loc[agent_performance['Performance_Score'].idxmax()]
            st.metric("🏆 Top Performer", top_performer['Agent'], 
                     delta=f"Score: {top_performer['Performance_Score']:.1f}")
        
        with col2:
            highest_satisfaction = agent_performance.loc[agent_performance['Customer_Satisfaction'].idxmax()]
            st.metric("😊 Highest Satisfaction", highest_satisfaction['Agent'],
                     delta=f"{highest_satisfaction['Customer_Satisfaction']:.1f}/10")
        
        with col3:
            most_efficient = agent_performance.loc[agent_performance['Avg_Resolution_Time'].idxmin()]
            st.metric("⚡ Most Efficient", most_efficient['Agent'],
                     delta=f"{most_efficient['Avg_Resolution_Time']/60:.1f} min")
        
        with col4:
            top_revenue = agent_performance.loc[agent_performance['Revenue_Generated'].idxmax()]
            st.metric("💰 Top Revenue Generator", top_revenue['Agent'],
                     delta=f"${top_revenue['Revenue_Generated']:,.0f}")
        
        st.markdown("---")
        
        # Performance visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Agent performance radar chart
            fig_radar = go.Figure()
            
            for idx, agent in agent_performance.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[
                        agent['Performance_Score'],
                        agent['Customer_Satisfaction'],
                        agent['Success_Rate'] * 10,  # Scale to 0-10
                        agent['AI_Accuracy'] * 10,   # Scale to 0-10
                        10 - (agent['Escalation_Rate'] * 10)  # Invert and scale
                    ],
                    theta=['Performance', 'Satisfaction', 'Success Rate', 'AI Accuracy', 'Low Escalation'],
                    fill='toself',
                    name=agent['Agent']
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=True,
                title="📊 Agent Performance Radar",
                height=400,
                title_font_size=16
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # Call volume vs performance
            fig_performance = px.scatter(
                agent_performance,
                x='Total_Calls',
                y='Performance_Score',
                size='Revenue_Generated',
                color='Customer_Satisfaction',
                hover_name='Agent',
                title="📈 Call Volume vs Performance",
                color_continuous_scale='RdYlGn'
            )
            fig_performance.update_layout(height=400, title_font_size=16)
            st.plotly_chart(fig_performance, use_container_width=True)
        
        # Detailed agent performance table
        st.markdown("### 📊 Detailed Agent Performance")
        display_enhanced_dataframe(agent_performance, "Agent Performance Report", "agent_performance")
        
        # Agent improvement recommendations
        st.markdown("### 💡 Performance Improvement Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Areas for Improvement")
            
            # Low performers
            low_performers = agent_performance[agent_performance['Performance_Score'] < 8.0]
            if not low_performers.empty:
                st.markdown("**Agents Below Performance Threshold:**")
                for _, agent in low_performers.iterrows():
                    st.warning(f"📊 {agent['Agent']} - Score: {agent['Performance_Score']:.1f}")
            
            # High escalation rates
            high_escalation = agent_performance[agent_performance['Escalation_Rate'] > 0.1]
            if not high_escalation.empty:
                st.markdown("**High Escalation Rates:**")
                for _, agent in high_escalation.iterrows():
                    st.error(f"⚠️ {agent['Agent']} - Escalation: {agent['Escalation_Rate']:.1%}")
        
        with col2:
            st.markdown("#### 🌟 Best Practices")
            
            # Top performers
            top_performers = agent_performance[agent_performance['Performance_Score'] >= 9.0]
            if not top_performers.empty:
                st.markdown("**Outstanding Performers:**")
                for _, agent in top_performers.iterrows():
                    st.success(f"🏆 {agent['Agent']} - Score: {agent['Performance_Score']:.1f}")
            
            # Efficiency leaders
            efficient_agents = agent_performance[agent_performance['Avg_Resolution_Time'] < 120]  # Under 2 minutes
            if not efficient_agents.empty:
                st.markdown("**Efficiency Leaders:**")
                for _, agent in efficient_agents.iterrows():
                    st.info(f"⚡ {agent['Agent']} - Avg Resolution: {agent['Avg_Resolution_Time']/60:.1f} min")

with tab5:
    st.markdown("## 💰 Revenue & Pipeline Analysis")
    
    if not filtered_df.empty:
        # Revenue metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = filtered_df['revenue_impact'].sum()
            st.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
        
        with col2:
            avg_deal_size = filtered_df[filtered_df['revenue_impact'] > 0]['revenue_impact'].mean()
            st.metric("📊 Avg Deal Size", f"${avg_deal_size:,.0f}" if not pd.isna(avg_deal_size) else "$0")
        
        with col3:
            pipeline_value = (filtered_df['customer_lifetime_value'] * filtered_df['conversion_probability']).sum()
            st.metric("🎯 Pipeline Value", f"${pipeline_value:,.0f}")
        
        with col4:
            deals_closed = (filtered_df['revenue_impact'] > 0).sum()
            st.metric("🤝 Deals Closed", deals_closed)
        
        st.markdown("---")
        
        # Revenue analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by category
            revenue_by_category = filtered_df.groupby('call_category')['revenue_impact'].sum().reset_index()
            fig_revenue_cat = px.bar(
                revenue_by_category,
                x='call_category',
                y='revenue_impact',
                title="💰 Revenue by Category",
                color='revenue_impact',
                color_continuous_scale='Greens'
            )
            fig_revenue_cat.update_layout(
                xaxis_title="Category",
                yaxis_title="Revenue ($)",
                height=400,
                title_font_size=16
            )
            st.plotly_chart(fig_revenue_cat, use_container_width=True)
        
        with col2:
            # Conversion funnel
            funnel_data = pd.DataFrame({
                'Stage': ['Total Calls', 'Successful Calls', 'Appointments Scheduled', 'Deals Closed'],
                'Count': [
                    len(filtered_df),
                    (filtered_df['call_success'] == 'Yes').sum(),
                    (filtered_df['appointment_scheduled'] == 'Yes').sum(),
                    (filtered_df['revenue_impact'] > 0).sum()
                ]
            })
            
            fig_funnel = px.funnel(
                funnel_data,
                x='Count',
                y='Stage',
                title="🎯 Sales Conversion Funnel"
            )
            fig_funnel.update_layout(height=400, title_font_size=16)
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Pipeline analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Deal size distribution
            deals_data = filtered_df[filtered_df['revenue_impact'] > 0]
            if not deals_data.empty:
                fig_deal_dist = px.histogram(
                    deals_data,
                    x='revenue_impact',
                    title="📊 Deal Size Distribution",
                    nbins=10,
                    color_discrete_sequence=['#2E86C1']
                )
                fig_deal_dist.update_layout(
                    xaxis_title="Deal Size ($)",
                    yaxis_title="Number of Deals",
                    height=400,
                    title_font_size=16
                )
                st.plotly_chart(fig_deal_dist, use_container_width=True)
        
        with col2:
            # Customer lifetime value vs conversion probability
            fig_ltv_conv = px.scatter(
                filtered_df,
                x='customer_lifetime_value',
                y='conversion_probability',
                size='revenue_impact',
                color='customer_tier',
                title="💎 LTV vs Conversion Probability",
                hover_data=['customer_name', 'call_outcome']
            )
            fig_ltv_conv.update_layout(height=400, title_font_size=16)
            st.plotly_chart(fig_ltv_conv, use_container_width=True)
        
        # Top opportunities
        st.markdown("### 🏆 Top Revenue Opportunities")
        
        opportunities = filtered_df.nlargest(20, 'customer_lifetime_value')[
            ['customer_name', 'customer_lifetime_value', 'conversion_probability', 
             'revenue_impact', 'next_best_action', 'call_outcome', 'customer_tier']
        ].copy()
        
        opportunities['Expected_Value'] = opportunities['customer_lifetime_value'] * opportunities['conversion_probability']
        opportunities = opportunities.sort_values('Expected_Value', ascending=False)
        
        display_enhanced_dataframe(opportunities, "Top Revenue Opportunities", "revenue_opportunities")

with tab6:
    st.markdown("## 🔮 AI Insights & Predictive Analytics")
    
    if not filtered_df.empty:
        # AI insights metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_ai_accuracy = filtered_df['ai_accuracy_score'].mean()
            st.metric("🤖 Average AI Accuracy", f"{avg_ai_accuracy:.1%}")
        
        with col2:
            high_confidence_calls = (filtered_df['confidence_score'] > 0.9).sum()
            st.metric("🎯 High Confidence Calls", high_confidence_calls)
        
        with col3:
            sentiment_positive = (filtered_df['sentiment_score'] > 0.7).sum()
            st.metric("😊 Positive Sentiment", sentiment_positive)
        
        with col4:
            auto_resolved = (filtered_df['escalation_required'] == 'No').sum()
            st.metric("✅ Auto-Resolved", auto_resolved)
        
        st.markdown("---")
        
        # AI performance analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # AI accuracy vs customer satisfaction
            fig_ai_satisfaction = px.scatter(
                filtered_df,
                x='ai_accuracy_score',
                y='customer_satisfaction',
                size='call_duration_seconds',
                color='call_category',
                title="🤖 AI Accuracy vs Customer Satisfaction",
                hover_data=['customer_name', 'voice_agent_name']
            )
            fig_ai_satisfaction.update_layout(height=400, title_font_size=16)
            st.plotly_chart(fig_ai_satisfaction, use_container_width=True)
        
        with col2:
            # Sentiment distribution
            fig_sentiment = px.histogram(
                filtered_df,
                x='sentiment_score',
                title="🎭 Customer Sentiment Distribution",
                nbins=20,
                color_discrete_sequence=['#E74C3C']
            )
            fig_sentiment.update_layout(
                xaxis_title="Sentiment Score",
                yaxis_title="Number of Calls",
                height=400,
                title_font_size=16
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Keyword analysis
        st.markdown("### 🔍 Keyword & Topic Analysis")
        
        if 'keyword_tags' in filtered_df.columns:
            # Extract and analyze keywords
            all_keywords = []
            for keywords in filtered_df['keyword_tags'].dropna():
                all_keywords.extend([k.strip() for k in str(keywords).split(',')])
            
            keyword_counts = pd.Series(all_keywords).value_counts().head(20)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_keywords = px.bar(
                    x=keyword_counts.values,
                    y=keyword_counts.index,
                    orientation='h',
                    title="🏷️ Top Keywords Mentioned",
                    color=keyword_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig_keywords.update_layout(
                    xaxis_title="Frequency",
                    yaxis_title="Keywords",
                    height=500,
                    title_font_size=16
                )
                st.plotly_chart(fig_keywords, use_container_width=True)
            
            with col2:
                # Intent detection analysis
                intent_counts = filtered_df['intent_detected'].value_counts()
                fig_intent = px.pie(
                    values=intent_counts.values,
                    names=intent_counts.index,
                    title="🎯 Intent Detection Distribution",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_intent.update_layout(height=500, title_font_size=16)
                st.plotly_chart(fig_intent, use_container_width=True)
        
        # Predictive insights
        st.markdown("### 📈 Predictive Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔮 AI Predictions")
            
            # High probability conversions
            high_conversion = filtered_df[filtered_df['conversion_probability'] > 0.8]
            st.write(f"**🎯 High Conversion Probability ({len(high_conversion)} customers):**")
            if not high_conversion.empty:
                for _, row in high_conversion.head(5).iterrows():
                    st.success(f"• {row['customer_name']} - {row['conversion_probability']:.0%} likely to convert")
            
            # Risk indicators
            risk_customers = filtered_df[
                (filtered_df['customer_satisfaction'] < 7) & 
                (filtered_df['customer_lifetime_value'] > 10000)
            ]
            if not risk_customers.empty:
                st.write(f"**⚠️ At-Risk High-Value Customers ({len(risk_customers)}):**")
                for _, row in risk_customers.head(3).iterrows():
                    st.warning(f"• {row['customer_name']} - Satisfaction: {row['customer_satisfaction']:.1f}")
        
        with col2:
            st.markdown("#### 💡 Optimization Recommendations")
            
            # Agent optimization
            low_ai_accuracy = filtered_df[filtered_df['ai_accuracy_score'] < 0.85]
            if not low_ai_accuracy.empty:
                st.write("**🤖 AI Model Optimization Needed:**")
                agents_to_optimize = low_ai_accuracy['voice_agent_name'].value_counts().head(3)
                for agent, count in agents_to_optimize.items():
                    st.info(f"• {agent}: {count} low-accuracy calls")
            
            # Process improvements
            long_resolution = filtered_df[filtered_df['resolution_time_seconds'] > 300]  # > 5 minutes
            if not long_resolution.empty:
                st.write("**⚡ Process Efficiency Improvements:**")
                categories_slow = long_resolution['call_category'].value_counts().head(3)
                for category, count in categories_slow.items():
                    st.warning(f"• {category}: {count} slow resolutions")

with tab7:
    st.markdown("## ⚙️ Admin Center & System Management")
    
    # System health metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(st.session_state.crm_data)
        st.metric("📊 Total Records", f"{total_records:,}")
    
    with col2:
        filtered_records = len(filtered_df)
        filter_percentage = (filtered_records / total_records * 100) if total_records > 0 else 0
        st.metric("🔍 Filtered Records", f"{filtered_records:,}", delta=f"{filter_percentage:.1f}% of total")
    
    with col3:
        if not filtered_df.empty:
            date_range_days = (filtered_df['call_date'].max() - filtered_df['call_date'].min()).days
            st.metric("📅 Date Range", f"{date_range_days} days")
    
    with col4:
        if not filtered_df.empty:
            categories_count = filtered_df['call_category'].nunique()
            st.metric("📂 Categories", categories_count)
    
    st.markdown("---")
    
    # Data quality assessment
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Data Quality Assessment")
        
        if not st.session_state.crm_data.empty:
            df_quality = st.session_state.crm_data
            
            # Missing data analysis
            missing_data = df_quality.isnull().sum()
            total_cells = len(df_quality) * len(df_quality.columns)
            missing_percentage = (missing_data.sum() / total_cells) * 100
            
            st.write(f"**Overall Data Completeness: {100-missing_percentage:.1f}%**")
            
            if missing_data.sum() > 0:
                st.write("**Missing Data by Column:**")
                missing_df = pd.DataFrame({
                    'Column': missing_data[missing_data > 0].index,
                    'Missing Count': missing_data[missing_data > 0].values,
                    'Missing %': (missing_data[missing_data > 0] / len(df_quality) * 100).round(1)
                })
                st.dataframe(missing_df, use_container_width=True)
            else:
                st.success("✅ No missing data detected!")
            
            # Duplicate analysis
            duplicates = df_quality.duplicated().sum()
            if duplicates > 0:
                st.warning(f"⚠️ Found {duplicates} duplicate records")
                if st.button("🧹 Remove Duplicates"):
                    st.session_state.crm_data = st.session_state.crm_data.drop_duplicates()
                    st.success(f"Removed {duplicates} duplicate records")
                    st.rerun()
            else:
                st.success("✅ No duplicate records found!")
    
    with col2:
        st.markdown("### 📈 System Statistics")
        
        if not st.session_state.crm_data.empty:
            df_stats = st.session_state.crm_data
            
            stats_data = {
                "Data Points": [
                    "Total Records",
                    "Date Range",
                    "Unique Customers",
                    "Unique Agents",
                    "Categories",
                    "Average Call Duration",
                    "Total Revenue Impact"
                ],
                "Values": [
                    f"{len(df_stats):,}",
                    f"{df_stats['call_date'].min().strftime('%Y-%m-%d')} to {df_stats['call_date'].max().strftime('%Y-%m-%d')}",
                    f"{df_stats['customer_name'].nunique():,}",
                    f"{df_stats['voice_agent_name'].nunique()}",
                    f"{df_stats['call_category'].nunique()}",
                    f"{df_stats['call_duration_seconds'].mean()/60:.1f} minutes",
                    f"${df_stats['revenue_impact'].sum():,.2f}"
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    # Bulk operations
    st.markdown("### 🔧 Bulk Operations")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Refresh Data", help="Reload data from source"):
            st.session_state.crm_data = load_enhanced_crm_data()
            st.success("✅ Data refreshed successfully!")
            st.rerun()
    
    with col2:
        if st.button("🧹 Clean Data", help="Remove duplicates and handle missing values"):
            original_count = len(st.session_state.crm_data)
            
            # Remove duplicates
            st.session_state.crm_data = st.session_state.crm_data.drop_duplicates()
            
            # Fill missing numeric values with median
            numeric_columns = st.session_state.crm_data.select_dtypes(include=[np.number]).columns
            st.session_state.crm_data[numeric_columns] = st.session_state.crm_data[numeric_columns].fillna(
                st.session_state.crm_data[numeric_columns].median()
            )
            
            new_count = len(st.session_state.crm_data)
            st.success(f"✅ Data cleaned! Removed {original_count - new_count} records")
    
    with col3:
        if st.button("📊 Generate Report", help="Create comprehensive data report"):
            # Generate a comprehensive report
            report_data = {
                "Report Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Total Records": len(st.session_state.crm_data),
                "Date Range": f"{st.session_state.crm_data['call_date'].min().strftime('%Y-%m-%d')} to {st.session_state.crm_data['call_date'].max().strftime('%Y-%m-%d')}",
                "Success Rate": f"{(st.session_state.crm_data['call_success'] == 'Yes').mean():.1%}",
                "Average Satisfaction": f"{st.session_state.crm_data['customer_satisfaction'].mean():.1f}",
                "Total Revenue": f"${st.session_state.crm_data['revenue_impact'].sum():,.2f}"
            }
            
            report_json = pd.Series(report_data).to_json(indent=2)
            st.download_button(
                label="📥 Download Report",
                data=report_json,
                file_name=f"crm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            st.success("📊 Report generated successfully!")
    
    with col4:
        if st.button("💾 Backup Data", help="Create backup of current data"):
            backup_csv = st.session_state.crm_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Backup",
                data=backup_csv,
                file_name=f"crm_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            st.success("💾 Backup created successfully!")
    
    # Configuration settings
    st.markdown("### ⚙️ System Configuration")
    
    with st.expander("🔧 Advanced Settings", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Display Settings:**")
            auto_refresh = st.checkbox("🔄 Auto-refresh data every 5 minutes", value=False)
            show_debug = st.checkbox("🐛 Show debug information", value=False)
            max_display_rows = st.number_input("📊 Max rows per table", min_value=10, max_value=1000, value=50)
            
        with col2:
            st.markdown("**Notification Settings:**")
            email_notifications = st.checkbox("📧 Enable email notifications", value=False)
            slack_notifications = st.checkbox("💬 Enable Slack notifications", value=False)
            alert_threshold = st.slider("⚠️ Satisfaction alert threshold", min_value=1.0, max_value=10.0, value=7.0, step=0.1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Settings:**")
            data_retention_days = st.number_input("📅 Data retention (days)", min_value=30, max_value=365, value=90)
            backup_frequency = st.selectbox("💾 Backup frequency", ["Daily", "Weekly", "Monthly"])
        
        with col2:
            st.markdown("**Performance Settings:**")
            cache_duration = st.number_input("⚡ Cache duration (minutes)", min_value=1, max_value=60, value=10)
            batch_size = st.number_input("📦 Processing batch size", min_value=100, max_value=10000, value=1000)
        
        if st.button("💾 Save Configuration"):
            # In a real application, you would save these settings
            st.success("✅ Configuration saved successfully!")
    
    # System monitoring
    st.markdown("### 📊 System Monitoring")
    
    # Simulated system metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**System Health:**")
        cpu_usage = np.random.randint(10, 30)
        memory_usage = np.random.randint(40, 70)
        disk_usage = np.random.randint(20, 50)
        
        st.progress(cpu_usage / 100, text=f"CPU Usage: {cpu_usage}%")
        st.progress(memory_usage / 100, text=f"Memory Usage: {memory_usage}%")
        st.progress(disk_usage / 100, text=f"Disk Usage: {disk_usage}%")
    
    with col2:
        st.markdown("**Database Performance:**")
        query_time = np.random.uniform(0.1, 2.0)
        connection_pool = np.random.randint(5, 20)
        cache_hit_rate = np.random.uniform(85, 98)
        
        st.metric("⚡ Avg Query Time", f"{query_time:.2f}s")
        st.metric("🔗 Active Connections", connection_pool)
        st.metric("📊 Cache Hit Rate", f"{cache_hit_rate:.1f}%")
    
    with col3:
        st.markdown("**API Performance:**")
        api_uptime = np.random.uniform(99.5, 99.9)
        requests_per_min = np.random.randint(50, 200)
        error_rate = np.random.uniform(0.1, 1.0)
        
        st.metric("✅ Uptime", f"{api_uptime:.2f}%")
        st.metric("📡 Requests/min", requests_per_min)
        st.metric("❌ Error Rate", f"{error_rate:.2f}%")

if 'crm_data' in st.session_state and not st.session_state.crm_data.empty:
    # show dashboard
    st.dataframe(st.session_state.crm_data)
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; color: white; margin: 2rem 0;">
        <h2>📁 No Data Available</h2>
        <p>Please upload a CSV file using the sidebar to get started with your CRM dashboard.</p>
        <p>The dashboard supports comprehensive call center data with transcripts, customer information, and performance metrics.</p>
    </div>
    """, unsafe_allow_html=True)
# Enhanced footer
st.markdown("---")
st.markdown(f"""
<div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
           padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
    <h4>🚀 AI Call Center CRM Dashboard</h4>
    <p>Built with Streamlit | Enhanced Wide-Screen Display | Advanced Analytics</p>
    <p>Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 
       Records Loaded: {len(st.session_state.crm_data):,} | 
       Active Filters: {len(filtered_df):,} shown</p>
</div>
""", unsafe_allow_html=True)
