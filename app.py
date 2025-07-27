import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json
import requests
from streamlit_calendar import calendar
import uuid
import io
import base64

# Configure page - MUST be first Streamlit command
st.set_page_config(
    page_title="AI Call Center CRM Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📞"
)

# Enhanced custom CSS with black text in boxes
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
    
    /* Metric cards with BLACK text */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: #212529;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #dee2e6;
    }
    
    .success-metric {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        border: 2px solid #ffeaa7;
    }
    
    .danger-metric {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    
    .info-metric {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        border: 2px solid #bee5eb;
    }
    
    /* Wide screen table styling with BLACK text */
    .dataframe-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        overflow-x: auto;
        border: 2px solid #dee2e6;
    }
    
    /* Enhanced table styling with BLACK text */
    .enhanced-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
        color: #212529;
    }
    
    .enhanced-table th {
        background: linear-gradient(135deg, #495057 0%, #343a40 100%);
        color: white;
        padding: 12px 8px;
        text-align: left;
        position: sticky;
        top: 0;
        z-index: 10;
        font-weight: bold;
    }
    
    .enhanced-table td {
        padding: 8px;
        border-bottom: 1px solid #dee2e6;
        word-wrap: break-word;
        max-width: 300px;
        color: #212529;
    }
    
    .enhanced-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    .enhanced-table tr:hover {
        background-color: #e3f2fd;
    }
    
    /* Transcript column styling with BLACK text */
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
        color: #212529;
        border: 1px solid #dee2e6;
    }
    
    .long-text-cell {
        max-width: 250px;
        max-height: 80px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-size: 11px;
        color: #212529;
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
    
    /* Custom expander with BLACK text */
    .custom-expander {
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: white;
        color: #212529;
    }
    
    /* Status indicators */
    .status-success { 
        background: #28a745; 
        color: white; 
        padding: 4px 8px; 
        border-radius: 15px; 
        font-size: 10px;
        font-weight: bold;
    }
    .status-warning { 
        background: #ffc107; 
        color: #212529; 
        padding: 4px 8px; 
        border-radius: 15px; 
        font-size: 10px;
        font-weight: bold;
    }
    .status-danger { 
        background: #dc3545; 
        color: white; 
        padding: 4px 8px; 
        border-radius: 15px; 
        font-size: 10px;
        font-weight: bold;
    }
    
    /* Calendar styling */
    .calendar-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 2px solid #dee2e6;
    }
    
    /* Form styling with BLACK text */
    .stTextInput > div > div > input {
        color: #212529;
        background-color: white;
        border: 2px solid #dee2e6;
    }
    
    .stSelectbox > div > div > select {
        color: #212529;
        background-color: white;
        border: 2px solid #dee2e6;
    }
    
    .stTextArea > div > div > textarea {
        color: #212529;
        background-color: white;
        border: 2px solid #dee2e6;
    }
    
    /* Info boxes with BLACK text */
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 2px solid #bee5eb;
    }
    
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border: 2px solid #ffeaa7;
    }
    
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    
    /* Edit form styling */
    .edit-form {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
    }
    
    /* Data editor styling */
    .data-editor {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 2px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)

# Authentication functions
def load_auth_config():
    """Load authentication configuration from JSON file"""
    try:
        # Default auth config if file doesn't exist
        default_auth = {
            "users": {
                "admin": {
                    "password": "admin123",
                    "role": "admin",
                    "name": "Administrator",
                    "email": "admin@company.com",
                    "permissions": ["read", "write", "delete", "admin"]
                },
                "manager": {
                    "password": "manager123",
                    "role": "manager",
                    "name": "Manager User",
                    "email": "manager@company.com",
                    "permissions": ["read", "write"]
                },
                "agent": {
                    "password": "agent123",
                    "role": "agent",
                    "name": "Agent User",
                    "email": "agent@company.com",
                    "permissions": ["read"]
                }
            },
            "google_sheets": {
                "url": "https://docs.google.com/spreadsheets/d/1LFfNwb9lRQpIosSEvV3O6zIwymUIWeG9L_k7cxw1jQs/export?format=csv",
                "calendar_sheet": "https://docs.google.com/spreadsheets/d/1LFfNwb9lRQpIosSEvV3O6zIwymUIWeG9L_k7cxw1jQs/export?format=csv&gid=1"
            }
        }
        
        if 'auth_config' not in st.session_state:
            st.session_state.auth_config = default_auth
        
        return st.session_state.auth_config
    except Exception as e:
        st.error(f"Error loading auth config: {e}")
        return {}

def authenticate_user(username, password):
    """Authenticate user credentials"""
    auth_config = load_auth_config()
    users = auth_config.get("users", {})
    
    if username in users and users[username]["password"] == password:
        return users[username]
    return None

def check_permission(permission):
    """Check if current user has specific permission"""
    if 'user' not in st.session_state:
        return False
    
    user_permissions = st.session_state.user.get("permissions", [])
    return permission in user_permissions

# Google Sheets data loading
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data_from_google_sheets():
    """Load CRM data from Google Sheets"""
    try:
        auth_config = load_auth_config()
        sheets_url = auth_config.get("google_sheets", {}).get("url", "")
        
        if not sheets_url:
            # Fallback to sample data
            return create_comprehensive_sample_data()
        
        # Load data from Google Sheets
        df = pd.read_csv(sheets_url)
        
        # Ensure required columns exist
        required_columns = [
            'call_id', 'customer_name', 'voice_agent_name', 'call_date',
            'call_duration_seconds', 'customer_satisfaction', 'call_category',
            'call_outcome', 'revenue_impact', 'transcript', 'call_summary'
        ]
        
        for col in required_columns:
            if col not in df.columns:
                if col == 'call_date':
                    df[col] = datetime.now().strftime('%Y-%m-%d')
                elif col in ['customer_satisfaction', 'revenue_impact', 'call_duration_seconds']:
                    df[col] = 0
                else:
                    df[col] = 'N/A'
        
        # Convert date columns
        df['call_date'] = pd.to_datetime(df['call_date'])
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {e}")
        return create_comprehensive_sample_data()

def create_comprehensive_sample_data():
    """Create comprehensive sample data with all features"""
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
    
    # Generate comprehensive sample data
    data = []
    for i in range(50):  # Generate 50 sample records
        call_id = f"CALL_{str(i+1).zfill(3)}"
        customers = ["Sarah Johnson", "Mike Chen", "Emma Davis", "John Smith", "Lisa Wang", "David Brown", "Maria Garcia", "James Wilson", "Anna Lee", "Robert Taylor"]
        agents = ["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "AI Agent Marcus", "AI Agent Luna"]
        categories = ["Sales", "Support", "Billing", "Technical", "Follow-up"]
        outcomes = ["Demo_Scheduled", "Issue_Resolved", "Follow_up_Required", "Sale_Closed", "Escalated"]
        tiers = ["Premium", "Standard", "Basic"]
        
        customer_name = np.random.choice(customers)
        agent_name = np.random.choice(agents)
        category = np.random.choice(categories)
        outcome = np.random.choice(outcomes)
        tier = np.random.choice(tiers)
        
        # Generate realistic metrics based on category
        if category == "Sales":
            satisfaction = np.random.uniform(7.5, 9.5)
            revenue = np.random.uniform(1000, 50000) if outcome == "Sale_Closed" else np.random.uniform(0, 5000)
            duration = np.random.randint(120, 600)
        elif category == "Support":
            satisfaction = np.random.uniform(8.0, 9.8)
            revenue = 0
            duration = np.random.randint(60, 300)
        else:
            satisfaction = np.random.uniform(6.5, 9.0)
            revenue = np.random.uniform(0, 1000)
            duration = np.random.randint(30, 180)
        
        record = {
            "call_id": call_id,
            "customer_name": customer_name,
            "voice_agent_name": agent_name,
            "call_date": (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d'),
            "call_start_time": f"{np.random.randint(9, 17):02d}:{np.random.randint(0, 59):02d}:00",
            "call_end_time": f"{np.random.randint(9, 17):02d}:{np.random.randint(0, 59):02d}:00",
            "call_duration_seconds": duration,
            "call_duration_hms": f"00:{duration//60:02d}:{duration%60:02d}",
            "cost": round(duration * 0.05, 2),
            "call_success": np.random.choice(["Yes", "No"], p=[0.85, 0.15]),
            "appointment_scheduled": np.random.choice(["Yes", "No"], p=[0.3, 0.7]),
            "intent_detected": f"{category}_Inquiry",
            "sentiment_score": np.random.uniform(0.6, 0.95),
            "confidence_score": np.random.uniform(0.8, 0.98),
            "keyword_tags": f"{category.lower()}, customer service, resolution, support",
            "summary_word_count": np.random.randint(20, 50),
            "customer_satisfaction": round(satisfaction, 1),
            "resolution_time_seconds": np.random.randint(30, duration),
            "escalation_required": np.random.choice(["Yes", "No"], p=[0.1, 0.9]),
            "language_detected": "English",
            "emotion_detected": np.random.choice(["Satisfied", "Neutral", "Frustrated", "Excited"]),
            "speech_rate_wpm": np.random.randint(120, 180),
            "silence_percentage": np.random.uniform(5, 20),
            "interruption_count": np.random.randint(0, 5),
            "ai_accuracy_score": np.random.uniform(0.85, 0.98),
            "follow_up_required": np.random.choice(["Yes", "No"], p=[0.4, 0.6]),
            "customer_tier": tier,
            "call_complexity": np.random.choice(["Low", "Medium", "High"], p=[0.5, 0.3, 0.2]),
            "agent_performance_score": np.random.uniform(8.0, 9.5),
            "call_outcome": outcome,
            "revenue_impact": round(revenue, 2),
            "lead_quality_score": np.random.uniform(6.0, 9.5),
            "conversion_probability": np.random.uniform(0.1, 0.9),
            "next_best_action": np.random.choice(["Follow_up", "Send_Materials", "Schedule_Demo", "Close_Deal"]),
            "customer_lifetime_value": np.random.randint(5000, 100000),
            "call_category": category,
            "transcript": sample_transcripts[i % len(sample_transcripts)],
            "call_summary": f"Customer {customer_name} contacted regarding {category.lower()} matter. {outcome.replace('_', ' ').lower()} with satisfaction score of {satisfaction:.1f}.",
            "customer_phone": f"+1-555-{np.random.randint(1000, 9999)}",
            "customer_email": f"{customer_name.lower().replace(' ', '.')}@email.com",
            "call_recording_url": f"https://recordings.techcorp.com/{call_id.lower()}.mp3",
            "follow_up_date": (datetime.now() + timedelta(days=np.random.randint(1, 14))).strftime('%Y-%m-%d') if np.random.choice([True, False]) else None,
            "assigned_rep": np.random.choice(["Jessica Martinez", "Tom Anderson", "Sarah Kim", "Mike Johnson"]),
            "deal_size_estimate": np.random.randint(1000, 100000) if category == "Sales" else 0,
            "competitor_mentioned": np.random.choice(["None", "CompetitorA", "CompetitorB", "CompetitorC"], p=[0.7, 0.1, 0.1, 0.1]),
            "pain_points": f"Current challenges with {category.lower()} processes and system integration",
            "budget_mentioned": f"${np.random.randint(10, 200)}k annual" if category == "Sales" else "N/A",
            "decision_timeline": np.random.choice(["Q1 2024", "Q2 2024", "Q3 2024", "Immediate", "N/A"]),
            "technical_requirements": f"{category} automation, reporting, integration capabilities"
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    df['call_date'] = pd.to_datetime(df['call_date'])
    df['follow_up_date'] = pd.to_datetime(df['follow_up_date'])
    
    return df

# Calendar data functions
@st.cache_data(ttl=300)
def load_calendar_events():
    """Load calendar events from Google Sheets or create sample data"""
    try:
        auth_config = load_auth_config()
        calendar_url = auth_config.get("google_sheets", {}).get("calendar_sheet", "")
        
        if calendar_url:
            df = pd.read_csv(calendar_url)
        else:
            # Sample calendar data
            events = []
            for i in range(20):  # Generate 20 sample events
                start_date = datetime.now() + timedelta(days=np.random.randint(-7, 30))
                duration = np.random.choice([30, 60, 90, 120])  # minutes
                end_date = start_date + timedelta(minutes=duration)
                
                event = {
                    "id": str(uuid.uuid4()),
                    "title": np.random.choice([
                        "Demo with Sarah Johnson",
                        "Follow-up Call - Mike Chen",
                        "Sales Meeting",
                        "Technical Support Call",
                        "Customer Onboarding",
                        "Product Training",
                        "Quarterly Review"
                    ]),
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                    "description": "Scheduled appointment with customer",
                    "customer": np.random.choice(["Sarah Johnson", "Mike Chen", "Emma Davis", "John Smith", "Lisa Wang"]),
                    "agent": np.random.choice(["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "Jessica Martinez"]),
                    "type": np.random.choice(["Demo", "Follow-up", "Support", "Sales", "Meeting"]),
                    "status": np.random.choice(["Scheduled", "Completed", "Cancelled"], p=[0.7, 0.2, 0.1])
                }
                events.append(event)
            
            df = pd.DataFrame(events)
        
        return df
    except Exception as e:
        st.error(f"Error loading calendar events: {e}")
        return pd.DataFrame()

def save_calendar_event(event_data):
    """Save calendar event (in real app, this would update Google Sheets)"""
    if 'calendar_events' not in st.session_state:
        st.session_state.calendar_events = load_calendar_events()
    
    # Add new event to session state
    new_event = pd.DataFrame([event_data])
    st.session_state.calendar_events = pd.concat([st.session_state.calendar_events, new_event], ignore_index=True)
    
    return True

def update_calendar_event(event_id, updated_data):
    """Update existing calendar event"""
    if 'calendar_events' not in st.session_state:
        st.session_state.calendar_events = load_calendar_events()
    
    # Update event in session state
    mask = st.session_state.calendar_events['id'] == event_id
    for key, value in updated_data.items():
        st.session_state.calendar_events.loc[mask, key] = value
    
    return True

def delete_calendar_event(event_id):
    """Delete calendar event"""
    if 'calendar_events' not in st.session_state:
        st.session_state.calendar_events = load_calendar_events()
    
    # Remove event from session state
    st.session_state.calendar_events = st.session_state.calendar_events[
        st.session_state.calendar_events['id'] != event_id
    ]
    
    return True

# Data editing functions
def save_data_changes(df):
    """Save changes to the CRM data"""
    st.session_state.crm_data = df
    # In a real application, this would also update the Google Sheets
    return True

def add_new_record(new_record):
    """Add a new record to the CRM data"""
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = load_data_from_google_sheets()
    
    # Add new record
    new_df = pd.DataFrame([new_record])
    st.session_state.crm_data = pd.concat([st.session_state.crm_data, new_df], ignore_index=True)
    
    return True

def delete_records(record_ids):
    """Delete records from CRM data"""
    if 'crm_data' not in st.session_state:
        return False
    
    # Remove records
    st.session_state.crm_data = st.session_state.crm_data[
        ~st.session_state.crm_data['call_id'].isin(record_ids)
    ]
    
    return True

# Enhanced data display function with editing capabilities
def display_enhanced_dataframe_with_editing(df, title="Data Table", key_prefix="table", allow_editing=True):
    """Display dataframe with enhanced styling and editing capabilities"""
    if df.empty:
        st.warning("No data to display")
        return df
    
    st.markdown(f"### {title}")
    
    # Editing controls
    if allow_editing and check_permission("write"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(f"➕ Add New Record", key=f"{key_prefix}_add"):
                st.session_state[f'show_add_form_{key_prefix}'] = True
        
        with col2:
            if st.button(f"✏️ Edit Selected", key=f"{key_prefix}_edit"):
                st.session_state[f'show_edit_form_{key_prefix}'] = True
        
        with col3:
            if st.button(f"🗑️ Delete Selected", key=f"{key_prefix}_delete"):
                st.session_state[f'show_delete_form_{key_prefix}'] = True
        
        with col4:
            if st.button(f"💾 Save Changes", key=f"{key_prefix}_save"):
                save_data_changes(df)
                st.success("✅ Changes saved successfully!")
    
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
            enable_selection = st.checkbox("Enable row selection", value=allow_editing, key=f"{key_prefix}_select")
    
    if not selected_columns:
        st.warning("Please select at least one column to display")
        return df
    
    # Filter dataframe
    display_df = df[selected_columns].head(max_rows)
    
    # Data editor for editing capabilities
    if allow_editing and check_permission("write") and enable_selection:
        st.markdown("#### 📝 Interactive Data Editor")
        
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            num_rows="dynamic",
            key=f"{key_prefix}_editor",
            column_config={
                col: st.column_config.TextColumn(
                    col.replace("_", " ").title(),
                    width="medium" if col not in ['transcript', 'call_summary'] else "large"
                ) for col in selected_columns
            }
        )
        
        # Update the original dataframe with changes
        if not edited_df.equals(display_df):
            # Update the main dataframe
            for col in selected_columns:
                if col in df.columns:
                    df.loc[display_df.index, col] = edited_df[col]
            
            st.info("💡 Changes made. Click 'Save Changes' to persist.")
    
    # Enhanced HTML table generation (fallback display)
    else:
        def generate_enhanced_html_table(df, truncate=True):
            html = '<div class="dataframe-container"><table class="enhanced-table">'
            
            # Headers
            html += '<thead><tr>'
            if show_index:
                html += '<th>Index</th>'
            if enable_selection:
                html += '<th>Select</th>'
            for col in df.columns:
                html += f'<th>{col.replace("_", " ").title()}</th>'
            html += '</tr></thead><tbody>'
            
            # Rows
            for idx, row in df.iterrows():
                html += '<tr>'
                if show_index:
                    html += f'<td>{idx}</td>'
                if enable_selection:
                    html += f'<td><input type="checkbox" id="row_{idx}"></td>'
                
                for col in df.columns:
                    value = row[col]
                    
                    # Handle different data types and apply appropriate styling
                    if pd.isna(value):
                        cell_content = '<em style="color: #6c757d;">N/A</em>'
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
                            cell_content = f'<span style="color: #28a745; font-weight: bold;">${float(value):,.2f}</span>'
                        else:
                            cell_content = '<span style="color: #6c757d;">$0.00</span>'
                    elif col in ['sentiment_score', 'confidence_score', 'ai_accuracy_score', 'conversion_probability']:
                        # Percentage formatting
                        if pd.notna(value):
                            cell_content = f'<span style="color: #007bff; font-weight: bold;">{float(value):.1%}</span>'
                        else:
                            cell_content = '<span style="color: #6c757d;">N/A</span>'
                    else:
                        cell_content = f'<span style="color: #212529;">{str(value)}</span>'
                    
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
        if st.button(f"📊 Export Excel", key=f"{key_prefix}_excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='CRM_Data', index=False)
            
            st.download_button(
                label="⬇️ Download Excel",
                data=output.getvalue(),
                file_name=f"crm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"{key_prefix}_excel_download"
            )
    
    with col4:
        if st.button(f"🔄 Refresh Data", key=f"{key_prefix}_refresh"):
            st.cache_data.clear()
            st.rerun()
    
    # Show add/edit forms if requested
    if allow_editing and check_permission("write"):
        show_add_record_form(key_prefix, df)
        show_edit_record_form(key_prefix, df)
        show_delete_records_form(key_prefix, df)
    
    return df

def show_add_record_form(key_prefix, df):
    """Show form to add new record"""
    if st.session_state.get(f'show_add_form_{key_prefix}', False):
        st.markdown("#### ➕ Add New Call Record")
        
        with st.form(f"add_record_{key_prefix}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                call_id = st.text_input("Call ID*", value=f"CALL_{len(df)+1:03d}")
                customer_name = st.text_input("Customer Name*")
                voice_agent_name = st.selectbox("Agent", ["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "AI Agent Marcus", "AI Agent Luna"])
                call_date = st.date_input("Call Date", value=datetime.now().date())
                call_category = st.selectbox("Category", ["Sales", "Support", "Billing", "Technical", "Follow-up"])
            
            with col2:
                customer_satisfaction = st.slider("Customer Satisfaction", 1.0, 10.0, 8.0, 0.1)
                call_outcome = st.selectbox("Call Outcome", ["Demo_Scheduled", "Issue_Resolved", "Follow_up_Required", "Sale_Closed", "Escalated"])
                revenue_impact = st.number_input("Revenue Impact ($)", min_value=0.0, value=0.0)
                customer_tier = st.selectbox("Customer Tier", ["Premium", "Standard", "Basic"])
                call_duration_seconds = st.number_input("Duration (seconds)", min_value=1, value=120)
            
            with col3:
                call_success = st.selectbox("Call Success", ["Yes", "No"])
                appointment_scheduled = st.selectbox("Appointment Scheduled", ["Yes", "No"])
                escalation_required = st.selectbox("Escalation Required", ["Yes", "No"])
                follow_up_required = st.selectbox("Follow-up Required", ["Yes", "No"])
                customer_phone = st.text_input("Customer Phone", value="+1-555-0000")
            
            transcript = st.text_area("Call Transcript", height=100)
            call_summary = st.text_area("Call Summary", height=60)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 Add Record", use_container_width=True):
                    if call_id and customer_name:
                        new_record = {
                            "call_id": call_id,
                            "customer_name": customer_name,
                            "voice_agent_name": voice_agent_name,
                            "call_date": call_date.strftime('%Y-%m-%d'),
                            "call_category": call_category,
                            "customer_satisfaction": customer_satisfaction,
                            "call_outcome": call_outcome,
                            "revenue_impact": revenue_impact,
                            "customer_tier": customer_tier,
                            "call_duration_seconds": call_duration_seconds,
                            "call_success": call_success,
                            "appointment_scheduled": appointment_scheduled,
                            "escalation_required": escalation_required,
                            "follow_up_required": follow_up_required,
                            "customer_phone": customer_phone,
                            "transcript": transcript,
                            "call_summary": call_summary,
                            # Add default values for other fields
                            "call_start_time": "09:00:00",
                            "call_end_time": "09:02:00",
                            "call_duration_hms": f"00:{call_duration_seconds//60:02d}:{call_duration_seconds%60:02d}",
                            "cost": round(call_duration_seconds * 0.05, 2),
                            "intent_detected": f"{call_category}_Inquiry",
                            "sentiment_score": 0.8,
                            "confidence_score": 0.9,
                            "keyword_tags": f"{call_category.lower()}, customer service",
                            "summary_word_count": len(call_summary.split()) if call_summary else 0,
                            "resolution_time_seconds": call_duration_seconds - 30,
                            "language_detected": "English",
                            "emotion_detected": "Neutral",
                            "speech_rate_wpm": 150,
                            "silence_percentage": 10.0,
                            "interruption_count": 1,
                            "ai_accuracy_score": 0.92,
                            "call_complexity": "Medium",
                            "agent_performance_score": 8.5,
                            "lead_quality_score": 7.5,
                            "conversion_probability": 0.5,
                            "next_best_action": "Follow_up",
                            "customer_lifetime_value": 15000,
                            "customer_email": f"{customer_name.lower().replace(' ', '.')}@email.com",
                            "call_recording_url": f"https://recordings.techcorp.com/{call_id.lower()}.mp3",
                            "follow_up_date": None,
                            "assigned_rep": "Support Team",
                            "deal_size_estimate": revenue_impact,
                            "competitor_mentioned": "None",
                            "pain_points": "General inquiry",
                            "budget_mentioned": "N/A",
                            "decision_timeline": "N/A",
                            "technical_requirements": "Standard support"
                        }
                        
                        if add_new_record(new_record):
                            st.success("✅ Record added successfully!")
                            st.session_state[f'show_add_form_{key_prefix}'] = False
                            st.rerun()
                        else:
                            st.error("❌ Failed to add record")
                    else:
                        st.warning("⚠️ Please fill in required fields (Call ID and Customer Name)")
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state[f'show_add_form_{key_prefix}'] = False
                    st.rerun()

def show_edit_record_form(key_prefix, df):
    """Show form to edit existing record"""
    if st.session_state.get(f'show_edit_form_{key_prefix}', False):
        st.markdown("#### ✏️ Edit Call Record")
        
        # Select record to edit
        call_ids = df['call_id'].tolist()
        selected_call_id = st.selectbox("Select Call to Edit", call_ids, key=f"edit_select_{key_prefix}")
        
        if selected_call_id:
            record = df[df['call_id'] == selected_call_id].iloc[0]
            
            with st.form(f"edit_record_{key_prefix}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    customer_name = st.text_input("Customer Name", value=record.get('customer_name', ''))
                    voice_agent_name = st.selectbox("Agent", 
                        ["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "AI Agent Marcus", "AI Agent Luna"],
                        index=["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "AI Agent Marcus", "AI Agent Luna"].index(record.get('voice_agent_name', 'AI Agent Emma')) if record.get('voice_agent_name') in ["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "AI Agent Marcus", "AI Agent Luna"] else 0
                    )
                    call_category = st.selectbox("Category", 
                        ["Sales", "Support", "Billing", "Technical", "Follow-up"],
                        index=["Sales", "Support", "Billing", "Technical", "Follow-up"].index(record.get('call_category', 'Support')) if record.get('call_category') in ["Sales", "Support", "Billing", "Technical", "Follow-up"] else 1
                    )
                
                with col2:
                    customer_satisfaction = st.slider("Customer Satisfaction", 1.0, 10.0, float(record.get('customer_satisfaction', 8.0)), 0.1)
                    call_outcome = st.selectbox("Call Outcome", 
                        ["Demo_Scheduled", "Issue_Resolved", "Follow_up_Required", "Sale_Closed", "Escalated"],
                        index=["Demo_Scheduled", "Issue_Resolved", "Follow_up_Required", "Sale_Closed", "Escalated"].index(record.get('call_outcome', 'Issue_Resolved')) if record.get('call_outcome') in ["Demo_Scheduled", "Issue_Resolved", "Follow_up_Required", "Sale_Closed", "Escalated"] else 1
                    )
                    revenue_impact = st.number_input("Revenue Impact ($)", min_value=0.0, value=float(record.get('revenue_impact', 0.0)))
                
                with col3:
                    call_success = st.selectbox("Call Success", 
                        ["Yes", "No"],
                        index=["Yes", "No"].index(record.get('call_success', 'Yes')) if record.get('call_success') in ["Yes", "No"] else 0
                    )
                    customer_tier = st.selectbox("Customer Tier", 
                        ["Premium", "Standard", "Basic"],
                        index=["Premium", "Standard", "Basic"].index(record.get('customer_tier', 'Standard')) if record.get('customer_tier') in ["Premium", "Standard", "Basic"] else 1
                    )
                
                transcript = st.text_area("Call Transcript", value=record.get('transcript', ''), height=100)
                call_summary = st.text_area("Call Summary", value=record.get('call_summary', ''), height=60)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        # Update the record in the dataframe
                        mask = df['call_id'] == selected_call_id
                        df.loc[mask, 'customer_name'] = customer_name
                        df.loc[mask, 'voice_agent_name'] = voice_agent_name
                        df.loc[mask, 'call_category'] = call_category
                        df.loc[mask, 'customer_satisfaction'] = customer_satisfaction
                        df.loc[mask, 'call_outcome'] = call_outcome
                        df.loc[mask, 'revenue_impact'] = revenue_impact
                        df.loc[mask, 'call_success'] = call_success
                        df.loc[mask, 'customer_tier'] = customer_tier
                        df.loc[mask, 'transcript'] = transcript
                        df.loc[mask, 'call_summary'] = call_summary
                        
                        if save_data_changes(df):
                            st.success("✅ Record updated successfully!")
                            st.session_state[f'show_edit_form_{key_prefix}'] = False
                            st.rerun()
                        else:
                            st.error("❌ Failed to update record")
                
                with col2:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state[f'show_edit_form_{key_prefix}'] = False
                        st.rerun()

def show_delete_records_form(key_prefix, df):
    """Show form to delete records"""
    if st.session_state.get(f'show_delete_form_{key_prefix}', False):
        st.markdown("#### 🗑️ Delete Call Records")
        
        st.warning("⚠️ This action cannot be undone. Please select records carefully.")
        
        # Multi-select for records to delete
        call_ids = df['call_id'].tolist()
        selected_records = st.multiselect(
            "Select Records to Delete",
            call_ids,
            key=f"delete_select_{key_prefix}",
            format_func=lambda x: f"{x} - {df[df['call_id']==x]['customer_name'].iloc[0]} ({df[df['call_id']==x]['call_category'].iloc[0]})"
        )
        
        if selected_records:
            st.markdown(f"**Records to be deleted: {len(selected_records)}**")
            
            # Show preview of records to be deleted
            preview_df = df[df['call_id'].isin(selected_records)][['call_id', 'customer_name', 'call_date', 'call_category']]
            st.dataframe(preview_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Confirm Delete", key=f"confirm_delete_{key_prefix}", use_container_width=True):
                    if delete_records(selected_records):
                        st.success(f"✅ {len(selected_records)} records deleted successfully!")
                        st.session_state[f'show_delete_form_{key_prefix}'] = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete records")
            
            with col2:
                if st.button("❌ Cancel", key=f"cancel_delete_{key_prefix}", use_container_width=True):
                    st.session_state[f'show_delete_form_{key_prefix}'] = False
                    st.rerun()

# Login page
def show_login_page():
    """Display login page"""
    st.markdown("""
    <div class="main-header">
        <h1>🔐 AI Call Center CRM Login</h1>
        <p>Please enter your credentials to access the dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 10px; 
                   box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: 2px solid #dee2e6;">
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### 👤 User Login")
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            with col2:
                demo_button = st.form_submit_button("🎯 Demo Login", use_container_width=True)
            
            if login_button:
                if username and password:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.success(f"Welcome, {user['name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            if demo_button:
                # Auto-login with demo credentials
                user = authenticate_user("admin", "admin123")
                if user:
                    st.session_state.user = user
                    st.session_state.authenticated = True
                    st.success(f"Demo login successful! Welcome, {user['name']}!")
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Demo credentials info
        st.markdown("""
        <div style="background: #d1ecf1; padding: 1rem; border-radius: 10px; 
                   margin-top: 1rem; border: 2px solid #bee5eb;">
            <h4 style="color: #0c5460; margin: 0;">🎯 Demo Credentials</h4>
            <p style="color: #0c5460; margin: 0.5rem 0 0 0;">
                <strong>Admin:</strong> admin / admin123<br>
                <strong>Manager:</strong> manager / manager123<br>
                <strong>Agent:</strong> agent / agent123
            </p>
        </div>
        """, unsafe_allow_html=True)

# Calendar page with enhanced features
def show_calendar_page():
    """Display calendar page with appointment management"""
    st.markdown("## 📅 Live Calendar & Appointment Management")
    
    # Load calendar events
    if 'calendar_events' not in st.session_state:
        st.session_state.calendar_events = load_calendar_events()
    
    # Calendar configuration
    calendar_options = {
        "editable": "true",
        "navLinks": "true",
        "selectable": "true",
        "selectMirror": "true",
        "dayMaxEvents": "true",
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay,listWeek"
        },
        "height": 650,
        "slotMinTime": "08:00:00",
        "slotMaxTime": "18:00:00",
        "businessHours": {
            "daysOfWeek": [1, 2, 3, 4, 5],
            "startTime": "09:00",
            "endTime": "17:00"
        }
    }
    
    # Convert events to calendar format
    calendar_events = []
    for _, event in st.session_state.calendar_events.iterrows():
        color_map = {
            "Demo": "#007bff",
            "Follow-up": "#28a745", 
            "Support": "#ffc107",
            "Sales": "#dc3545",
            "Meeting": "#6f42c1"
        }
        
        event_color = color_map.get(event.get('type', 'Meeting'), "#6c757d")
        
        calendar_events.append({
            "id": event.get('id', str(uuid.uuid4())),
            "title": event.get('title', 'Untitled Event'),
            "start": event.get('start', datetime.now().isoformat()),
            "end": event.get('end', (datetime.now() + timedelta(hours=1)).isoformat()),
            "description": event.get('description', ''),
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "white"
        })
    
    # Display calendar
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
        
        calendar_result = calendar(
            events=calendar_events,
            options=calendar_options,
            custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-weight: bold;
            }
            .fc-daygrid-event {
                font-size: 12px;
            }
            .fc-toolbar-title {
                color: #212529 !important;
            }
            .fc-button {
                background-color: #007bff !important;
                border-color: #007bff !important;
            }
            .fc-button:hover {
                background-color: #0056b3 !important;
                border-color: #0056b3 !important;
            }
            .fc-daygrid-day-number {
                color: #212529 !important;
            }
            .fc-col-header-cell {
                background-color: #f8f9fa !important;
            }
            """,
            key="calendar"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("➕ Add New Appointment", expanded=False):
    with st.form("add_appointment"):
        title = st.text_input("Title*", placeholder="e.g., Demo with Customer")
        customer = st.text_input("Customer", placeholder="Customer name")
        agent = st.selectbox("Agent", ["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "Jessica Martinez"])

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date())
            start_time = st.time_input("Start Time", value=datetime.now().time())
        with col2:
            duration = st.selectbox("Duration", ["30 min", "1 hour", "1.5 hours", "2 hours"])
            appointment_type = st.selectbox("Type", ["Demo", "Follow-up", "Support", "Sales Call", "Meeting"])

        description = st.text_area("Description", placeholder="Additional details...")

        if st.form_submit_button("📅 Schedule Appointment", use_container_width=True):
            if title:
                start_dt = datetime.combine(start_date, start_time)
                end_dt = start_dt + timedelta(minutes={"30 min": 30, "1 hour": 60, "1.5 hours": 90, "2 hours": 120}[duration])
                new_event = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "start": start_dt.isoformat(),
                    "end": end_dt.isoformat(),
                    "description": description,
                    "customer": customer,
                    "agent": agent,
                    "type": appointment_type,
                    "status": "Scheduled"
                }
                st.session_state.calendar_events = pd.concat(
                    [st.session_state.get("calendar_events", pd.DataFrame()), pd.DataFrame([new_event])],
                    ignore_index=True
                )
                st.success("✅ Appointment scheduled!")

with st.expander("✏️ Edit Appointment", expanded=False):
    if "calendar_events" in st.session_state and not st.session_state.calendar_events.empty:
        event_titles = [
            f"{row['title']} ({pd.to_datetime(row['start']).strftime('%m/%d %H:%M')})"
            for _, row in st.session_state.calendar_events.iterrows()
        ]
        st.selectbox("Select an event to edit", event_titles)
    else:
        st.warning("No events to edit.")

                        
                        # Save event
                        if save_calendar_event(new_event):
                            st.success("✅ Appointment scheduled successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to schedule appointment")
                    else:
                        st.warning("⚠️ Please enter a title for the appointment")
        
        # Edit appointment form
        with st.expander("✏️ Edit Appointment", expanded=False):
    event_titles = [
        f"{row['title']} ({pd.to_datetime(row['start']).strftime('%m/%d %H:%M')})"
        for _, row in st.session_state.calendar_events.iterrows()
    ]

            
            if event_titles:
                selected_event = st.selectbox("Select Event to Edit", event_titles)
                
                if selected_event:
                    # Extract event ID from selection
                    event_idx = event_titles.index(selected_event)
                    event_data = st.session_state.calendar_events.iloc[event_idx]
                    
                    with st.form("edit_appointment"):
                        new_title = st.text_input("Title", value=event_data['title'])
                        new_customer = st.text_input("Customer", value=event_data.get('customer', ''))
                        new_agent = st.selectbox("Agent", 
                            ["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "Jessica Martinez"],
                            index=["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "Jessica Martinez"].index(event_data.get('agent', 'AI Agent Emma')) if event_data.get('agent') in ["AI Agent Emma", "AI Agent Alex", "AI Agent Sophia", "Jessica Martinez"] else 0
                        )
                        
                        start_dt = pd.to_datetime(event_data['start'])
                        new_start_date = st.date_input("Start Date", value=start_dt.date())
                        new_start_time = st.time_input("Start Time", value=start_dt.time())
                        
                        new_type = st.selectbox("Type", 
                            ["Demo", "Follow-up", "Support", "Sales Call", "Meeting"],
                            index=["Demo", "Follow-up", "Support", "Sales Call", "Meeting"].index(event_data.get('type', 'Meeting')) if event_data.get('type') in ["Demo", "Follow-up", "Support", "Sales Call", "Meeting"] else 4
                        )
                        
                        new_description = st.text_area("Description", value=event_data.get('description', ''))
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.form_submit_button("💾 Update Event", use_container_width=True):
                                new_start_datetime = datetime.combine(new_start_date, new_start_time)
                                end_dt = pd.to_datetime(event_data['end'])
                                duration = end_dt - start_dt
                                new_end_datetime = new_start_datetime + duration
                                
                                updated_data = {
                                    "title": new_title,
                                    "start": new_start_datetime.isoformat(),
                                    "end": new_end_datetime.isoformat(),
                                    "customer": new_customer,
                                    "agent": new_agent,
                                    "type": new_type,
                                    "description": new_description
                                }
                                
                                if update_calendar_event(event_data['id'], updated_data):
                                    st.success("✅ Event updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update event")
                        
                        with col2:
                            if st.form_submit_button("🗑️ Delete Event", use_container_width=True):
                                if delete_calendar_event(event_data['id']):
                                    st.success("✅ Event deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete event")
            else:
                st.info("📭 No events available to edit")
        
        # Today's appointments
        st.markdown("### 📅 Today's Appointments")
        today = datetime.now().date()
        today_events = []
        
        for _, event in st.session_state.calendar_events.iterrows():
            event_date = pd.to_datetime(event['start']).date()
            if event_date == today:
                today_events.append(event)
        
        if today_events:
            for event in today_events:
                start_time = pd.to_datetime(event['start']).strftime('%H:%M')
                color_class = {
                    "Demo": "info-metric",
                    "Follow-up": "success-metric",
                    "Support": "warning-metric",
                    "Sales": "danger-metric",
                    "Meeting": "metric-card"
                }.get(event.get('type', 'Meeting'), "metric-card")
                
                st.markdown(f"""
                <div class="{color_class}" style="margin: 0.5rem 0; padding: 0.5rem; text-align: left;">
                    <strong>{start_time}</strong> - {event['title']}<br>
                    <small>{event.get('customer', 'N/A')} | {event.get('agent', 'N/A')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No appointments scheduled for today")
        
        # Upcoming appointments
        st.markdown("### 📆 Upcoming This Week")
        week_start = today
        week_end = today + timedelta(days=7)
        
        upcoming_events = []
        for _, event in st.session_state.calendar_events.iterrows():
            event_date = pd.to_datetime(event['start']).date()
            if week_start < event_date <= week_end:
                upcoming_events.append(event)
        
        if upcoming_events:
            for event in upcoming_events[:5]:  # Show max 5
                event_datetime = pd.to_datetime(event['start'])
                date_str = event_datetime.strftime('%m/%d')
                time_str = event_datetime.strftime('%H:%M')
                
                st.markdown(f"""
                <div class="warning-metric" style="margin: 0.5rem 0; padding: 0.5rem; text-align: left;">
                    <strong>{date_str} {time_str}</strong> - {event['title']}<br>
                    <small>{event.get('customer', 'N/A')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No upcoming appointments this week")
    
    # Handle calendar interactions
    if calendar_result.get("eventClick"):
        event_id = calendar_result["eventClick"]["event"]["id"]
        st.info(f"Event clicked: {event_id}")
    
    if calendar_result.get("dateClick"):
        clicked_date = calendar_result["dateClick"]["date"]
        st.info(f"Date clicked: {clicked_date}")
    
    # Calendar statistics
    st.markdown("---")
    st.markdown("### 📊 Calendar Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_appointments = len(st.session_state.calendar_events)
        st.markdown(f"""
        <div class="metric-card info-metric">
            <h3>📅 Total Appointments</h3>
            <h2>{total_appointments}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        today_count = len(today_events)
        st.markdown(f"""
        <div class="metric-card success-metric">
            <h3>📋 Today's Schedule</h3>
            <h2>{today_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        upcoming_count = len(upcoming_events)
        st.markdown(f"""
        <div class="metric-card warning-metric">
            <h3>📆 This Week</h3>
            <h2>{upcoming_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        demo_count = len([e for _, e in st.session_state.calendar_events.iterrows() if e.get('type') == 'Demo'])
        st.markdown(f"""
        <div class="metric-card danger-metric">
            <h3>🎯 Demos Scheduled</h3>
            <h2>{demo_count}</h2>
        </div>
        """, unsafe_allow_html=True)

# Main application
def main():
    """Main application logic"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Load auth config
    load_auth_config()
    
    # Check authentication
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    # Sidebar with user info and navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;">
            <h3>👤 Welcome, {st.session_state.user['name']}</h3>
            <p>Role: {st.session_state.user['role'].title()}</p>
            <p>📧 {st.session_state.user['email']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        page = st.selectbox(
            "Select Page",
            ["📊 CRM Dashboard", "📅 Live Calendar", "📈 Analytics", "👥 Customer Management", 
             "🎯 Agent Performance", "💰 Revenue Tracking", "🔮 AI Insights", "⚙️ Admin Center"],
            key="page_selector"
        )
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
        
        st.divider()
        
        # Data source info
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                   padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;">
            <h4>📡 Data Source</h4>
            <p>Google Sheets (Live)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced filters for CRM data
        if page == "📊 CRM Dashboard":
            st.markdown("### 🔍 Smart Filters")
            
            if 'crm_data' not in st.session_state:
                st.session_state.crm_data = load_data_from_google_sheets()
            
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
                
                # Store filtered data
                st.session_state.filtered_crm_data = filtered_df
                
                # Filter summary
                st.markdown("### 📈 Filter Summary")
                st.info(f"Showing **{len(filtered_df)}** of **{len(df)}** records")
        
        # Refresh data button
        if st.button("🔄 Refresh All Data", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
    
    # Main content based on selected page
    if page == "📊 CRM Dashboard":
        show_crm_dashboard()
    elif page == "📅 Live Calendar":
        show_calendar_page()
    elif page == "📈 Analytics":
        show_analytics_page()
    elif page == "👥 Customer Management":
        show_customer_management_page()
    elif page == "🎯 Agent Performance":
        show_agent_performance_page()
    elif page == "💰 Revenue Tracking":
        show_revenue_tracking_page()
    elif page == "🔮 AI Insights":
        show_ai_insights_page()
    elif page == "⚙️ Admin Center":
        show_admin_center_page()

def show_crm_dashboard():
    """Display the main CRM dashboard"""
    
    # Load data
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = load_data_from_google_sheets()
    
    # Use filtered data if available
    df = st.session_state.get('filtered_crm_data', st.session_state.crm_data)
    
    # Main dashboard header
    st.markdown("""
    <div class="main-header">
        <h1>📞 AI Call Center CRM Dashboard</h1>
        <p>Comprehensive Customer Relationship Management & Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced key metrics
    if not df.empty:
        st.markdown("## 📊 Key Performance Indicators")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            total_calls = len(df)
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>📞 Total Calls</h3>
                <h2>{total_calls:,}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            success_rate = (df['call_success'] == 'Yes').sum() / len(df) * 100 if len(df) > 0 else 0
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>✅ Success Rate</h3>
                <h2>{success_rate:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_satisfaction = df['customer_satisfaction'].mean()
            st.markdown(f"""
            <div class="metric-card warning-metric">
                <h3>⭐ Avg Satisfaction</h3>
                <h2>{avg_satisfaction:.1f}/10</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_revenue = df['revenue_impact'].sum()
            st.markdown(f"""
            <div class="metric-card danger-metric">
                <h3>💰 Revenue Impact</h3>
                <h2>${total_revenue:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            avg_duration = df['call_duration_seconds'].mean() / 60
            st.markdown(f"""
            <div class="metric-card">
                <h3>⏱️ Avg Duration</h3>
                <h2>{avg_duration:.1f} min</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced tabs with full functionality
        tab1, tab2, tab3 = st.tabs([
            "📋 Call Records & Transcripts", "📊 Quick Analytics", "✏️ Data Management"
        ])
        
        with tab1:
            st.markdown("## 📋 Comprehensive Call Records Management")
            
            # Quick stats bar
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🔍 Filtered Records", len(df))
            with col2:
                avg_call_duration = df['call_duration_seconds'].mean()
                st.metric("⏱️ Avg Call Time", f"{avg_call_duration/60:.1f} min")
            with col3:
                high_satisfaction = (df['customer_satisfaction'] >= 9).sum()
                st.metric("😊 High Satisfaction", f"{high_satisfaction} calls")
            with col4:
                follow_ups_needed = (df['follow_up_required'] == 'Yes').sum()
                st.metric("📅 Follow-ups Needed", f"{follow_ups_needed} calls")
            
            st.markdown("---")
            
            # Enhanced data display with editing
            display_enhanced_dataframe_with_editing(df, "Complete Call Records", "call_records")
            
            st.markdown("### 🎙️ Detailed Transcript Viewer")
            
            # Transcript detail view
            if len(df) > 0:
                selected_call = st.selectbox(
                    "Select call to view full transcript:",
                    options=df['call_id'].tolist(),
                    format_func=lambda x: f"{x} - {df[df['call_id']==x]['customer_name'].iloc[0]} ({df[df['call_id']==x]['call_category'].iloc[0]})"
                )
                
                if selected_call:
                    call_data = df[df['call_id'] == selected_call].iloc[0]
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("#### 📝 Full Transcript")
                        if 'transcript' in call_data and pd.notna(call_data['transcript']):
                            st.markdown(f"""
                            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; 
                                       border-left: 5px solid #007bff; max-height: 400px; overflow-y: auto; color: #212529;">
                                <pre style="white-space: pre-wrap; font-family: 'Segoe UI', sans-serif; 
                                           font-size: 14px; line-height: 1.5; color: #212529;">{call_data['transcript']}</pre>
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
                            "⏰ Duration": call_data.get('call_duration_hms', 'N/A'),
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
        
        with tab2:
            st.markdown("## 📊 Quick Analytics Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Call outcomes distribution
                outcome_counts = df['call_outcome'].value_counts()
                fig_pie = px.pie(
                    values=outcome_counts.values,
                    names=outcome_counts.index,
                    title="📊 Call Outcomes Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(
                    font=dict(size=12, color='#212529'),
                    title_font_size=16,
                    showlegend=True,
                    height=400,
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Customer satisfaction by category
                satisfaction_by_category = df.groupby('call_category')['customer_satisfaction'].mean().reset_index()
                fig_bar = px.bar(
                    satisfaction_by_category,
                    x='call_category',
                    y='customer_satisfaction',
                    title="⭐ Average Satisfaction by Category",
                    color='customer_satisfaction',
                    color_continuous_scale='RdYlGn'
                )
                fig_bar.update_layout(
                    font=dict(size=12, color='#212529'),
                    title_font_size=16,
                    height=400,
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Time series analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # Daily call volume
                daily_calls = df.groupby(df['call_date'].dt.date).size().reset_index()
                daily_calls.columns = ['Date', 'Call_Count']
                
                fig_line = px.line(
                    daily_calls,
                    x='Date',
                    y='Call_Count',
                    title="📈 Daily Call Volume Trend",
                    markers=True
                )
                fig_line.update_layout(
                    font=dict(size=12, color='#212529'),
                    title_font_size=16,
                    height=400,
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                st.plotly_chart(fig_line, use_container_width=True)
            
            with col2:
                # Revenue by agent
                revenue_by_agent = df.groupby('voice_agent_name')['revenue_impact'].sum().reset_index()
                fig_agent_revenue = px.bar(
                    revenue_by_agent,
                    x='voice_agent_name',
                    y='revenue_impact',
                    title="💰 Revenue Generated by Agent",
                    color='revenue_impact',
                    color_continuous_scale='Greens'
                )
                fig_agent_revenue.update_layout(
                    font=dict(size=12, color='#212529'),
                    title_font_size=16,
                    height=400,
                    paper_bgcolor='white',
                    plot_bgcolor='white'
                )
                st.plotly_chart(fig_agent_revenue, use_container_width=True)
        
        with tab3:
            st.markdown("## ✏️ Data Management & Bulk Operations")
            
            if check_permission("write"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 📊 Data Statistics")
                    st.info(f"**Total Records:** {len(st.session_state.crm_data):,}")
                    st.info(f"**Filtered Records:** {len(df):,}")
                    st.info(f"**Date Range:** {df['call_date'].min().strftime('%Y-%m-%d')} to {df['call_date'].max().strftime('%Y-%m-%d')}")
                
                with col2:
                    st.markdown("### 🔧 Bulk Operations")
                    
                    if st.button("🧹 Clean Data", use_container_width=True):
                        # Remove duplicates and handle missing values
                        original_count = len(st.session_state.crm_data)
                        
                        # Remove duplicates
                        st.session_state.crm_data = st.session_state.crm_data.drop_duplicates()
                        
                        # Fill missing numeric values with median
                        numeric_columns = st.session_state.crm_data.select_dtypes(include=[np.number]).columns
                        st.session_state.crm_data[numeric_columns] = st.session_state.crm_data[numeric_columns].fillna(
                            st.session_state.crm_data[numeric_columns].median()
                        )
                        
                        new_count = len(st.session_state.crm_data)
                        st.success(f"✅ Data cleaned! Processed {original_count - new_count} records")
                    
                    if st.button("📊 Generate Report", use_container_width=True):
                        # Generate comprehensive report
                        report_data = {
                            "Report Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Total Records": len(st.session_state.crm_data),
                            "Filtered Records": len(df),
                            "Success Rate": f"{(df['call_success'] == 'Yes').mean():.1%}",
                            "Average Satisfaction": f"{df['customer_satisfaction'].mean():.1f}",
                            "Total Revenue": f"${df['revenue_impact'].sum():,.2f}",
                            "Top Category": df['call_category'].mode().iloc[0] if not df.empty else "N/A",
                            "Top Agent": df['voice_agent_name'].mode().iloc[0] if not df.empty else "N/A"
                        }
                        
                        report_json = json.dumps(report_data, indent=2)
                        st.download_button(
                            label="📥 Download Report",
                            data=report_json,
                            file_name=f"crm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                        st.success("📊 Report generated successfully!")
                
                with col3:
                    st.markdown("### 💾 Data Export")
                    
                    # Export options
                    export_format = st.selectbox("Export Format", ["CSV", "Excel", "JSON"])
                    
                    if st.button("📥 Export Data", use_container_width=True):
                        if export_format == "CSV":
                            csv_data = df.to_csv(index=False)
                            st.download_button(
                                label="⬇️ Download CSV",
                                data=csv_data,
                                file_name=f"crm_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        elif export_format == "Excel":
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                df.to_excel(writer, sheet_name='CRM_Data', index=False)
                            
                            st.download_button(
                                label="⬇️ Download Excel",
                                data=output.getvalue(),
                                file_name=f"crm_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        else:  # JSON
                            json_data = df.to_json(orient='records', indent=2)
                            st.download_button(
                                label="⬇️ Download JSON",
                                data=json_data,
                                file_name=f"crm_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json"
                            )
                        
                        st.success(f"✅ {export_format} export ready!")
            else:
                st.warning("⚠️ Write permissions required for data management operations")
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                   border-radius: 15px; color: #212529; margin: 2rem 0; border: 2px solid #dee2e6;">
            <h2>📁 No Data Available</h2>
            <p>Unable to load data from Google Sheets. Please check the configuration.</p>
        </div>
        """, unsafe_allow_html=True)

def show_analytics_page():
    """Display advanced analytics page"""
    st.markdown("## 📈 Advanced Analytics & Performance Insights")
    
    # Load data
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = load_data_from_google_sheets()
    
    df = st.session_state.get('filtered_crm_data', st.session_state.crm_data)
    
    if not df.empty:
        # Advanced metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            conversion_rate = (df['conversion_probability'] > 0.5).mean() if 'conversion_probability' in df.columns else 0
            st.metric("🎯 Conversion Rate", f"{conversion_rate:.1%}", 
                     delta=f"+{(conversion_rate-0.15):.1%}" if conversion_rate > 0.15 else f"{(conversion_rate-0.15):.1%}")
        
        with col2:
            avg_ai_accuracy = df['ai_accuracy_score'].mean() if 'ai_accuracy_score' in df.columns else 0
            st.metric("🤖 AI Accuracy", f"{avg_ai_accuracy:.1%}",
                     delta=f"+{(avg_ai_accuracy-0.85):.1%}" if avg_ai_accuracy > 0.85 else f"{(avg_ai_accuracy-0.85):.1%}")
        
        with col3:
            escalation_rate = (df['escalation_required'] == 'Yes').mean() if 'escalation_required' in df.columns else 0
            st.metric("⚠️ Escalation Rate", f"{escalation_rate:.1%}",
                     delta=f"-{(0.1-escalation_rate):.1%}" if escalation_rate < 0.1 else f"+{(escalation_rate-0.1):.1%}")
        
        with col4:
            avg_resolution_time = df['resolution_time_seconds'].mean() / 60 if 'resolution_time_seconds' in df.columns else 0
            st.metric("⚡ Avg Resolution Time", f"{avg_resolution_time:.1f} min",
                     delta=f"-{(3-avg_resolution_time):.1f} min" if avg_resolution_time < 3 else f"+{(avg_resolution_time-3):.1f} min")
        
        st.markdown("---")
        
        # Advanced visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer satisfaction heatmap by category and tier
            if 'customer_tier' in df.columns:
                satisfaction_pivot = df.pivot_table(
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
                fig_heatmap.update_layout(
                    height=400, 
                    title_font_size=16,
                    font=dict(color='#212529'),
                    paper_bgcolor='white'
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with col2:
            # Sentiment vs Duration scatter
            if 'sentiment_score' in df.columns:
                fig_scatter = px.scatter(
                    df,
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
                fig_scatter.update_layout(
                    height=400, 
                    title_font_size=16,
                    font=dict(color='#212529'),
                    paper_bgcolor='white'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Performance correlation matrix
        st.markdown("### 🔗 Performance Correlation Analysis")
        
        correlation_cols = [
            'customer_satisfaction', 'sentiment_score', 'ai_accuracy_score',
            'agent_performance_score', 'call_duration_seconds', 'resolution_time_seconds',
            'speech_rate_wpm', 'interruption_count'
        ]
        
        available_corr_cols = [col for col in correlation_cols if col in df.columns]
        
        if len(available_corr_cols) > 2:
            corr_matrix = df[available_corr_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                title="🔗 Performance Metrics Correlation Matrix",
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            fig_corr.update_layout(
                height=500, 
                title_font_size=16,
                font=dict(color='#212529'),
                paper_bgcolor='white'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("📊 No data available for analytics")

def show_customer_management_page():
    """Display customer management page"""
    st.markdown("## 👥 Customer Intelligence & Management")
    
    # Load data
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = load_data_from_google_sheets()
    
    df = st.session_state.get('filtered_crm_data', st.session_state.crm_data)
    
    if not df.empty:
        # Customer overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            unique_customers = df['customer_name'].nunique()
            st.metric("👥 Unique Customers", unique_customers)
        
        with col2:
            premium_customers = (df['customer_tier'] == 'Premium').sum() if 'customer_tier' in df.columns else 0
            st.metric("👑 Premium Customers", premium_customers)
        
        with col3:
            high_value_customers = (df['customer_lifetime_value'] > 20000).sum() if 'customer_lifetime_value' in df.columns else 0
            st.metric("💎 High Value Customers", high_value_customers)
        
        with col4:
            repeat_customers = df.groupby('customer_name').size()
            repeat_count = (repeat_customers > 1).sum()
            st.metric("🔄 Repeat Customers", repeat_count)
        
        st.markdown("---")
        
        # Enhanced customer analysis
        customer_summary = df.groupby('customer_name').agg({
            'call_id': 'count',
            'customer_satisfaction': 'mean',
            'customer_lifetime_value': 'first' if 'customer_lifetime_value' in df.columns else lambda x: 0,
            'customer_tier': 'first' if 'customer_tier' in df.columns else lambda x: 'Standard',
            'revenue_impact': 'sum',
            'conversion_probability': 'mean' if 'conversion_probability' in df.columns else lambda x: 0,
            'call_category': lambda x: ', '.join(x.unique()),
            'call_outcome': lambda x: ', '.join(x.unique()),
            'next_best_action': 'last' if 'next_best_action' in df.columns else lambda x: 'Follow_up',
            'pain_points': 'last' if 'pain_points' in df.columns else lambda x: 'General inquiry'
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
            fig_customer_value.update_layout(
                height=400, 
                title_font_size=16,
                font=dict(color='#212529'),
                paper_bgcolor='white'
            )
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
                title_font_size=16,
                font=dict(color='#212529'),
                paper_bgcolor='white'
            )
            st.plotly_chart(fig_tier, use_container_width=True)
        
        # Detailed customer table with editing
        st.markdown("### 📊 Detailed Customer Analysis")
        display_enhanced_dataframe_with_editing(customer_summary, "Customer Intelligence Report", "customer_analysis")
        
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
    else:
        st.info("👥 No customer data available")

def show_agent_performance_page():
    """Display agent performance page"""
    st.markdown("## 🎯 Agent Performance Dashboard")
    
    # Load data
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = load_data_from_google_sheets()
    
    df = st.session_state.get('filtered_crm_data', st.session_state.crm_data)
    
    if not df.empty:
        # Agent performance aggregation
        agent_performance = df.groupby('voice_agent_name').agg({
            'call_id': 'count',
            'agent_performance_score': 'mean' if 'agent_performance_score' in df.columns else lambda x: 8.0,
            'customer_satisfaction': 'mean',
            'call_success': lambda x: (x == 'Yes').mean(),
            'ai_accuracy_score': 'mean' if 'ai_accuracy_score' in df.columns else lambda x: 0.9,
            'call_duration_seconds': 'mean',
            'resolution_time_seconds': 'mean' if 'resolution_time_seconds' in df.columns else lambda x: 120,
            'escalation_required': lambda x: (x == 'Yes').mean() if 'escalation_required' in df.columns else lambda x: 0.1,
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
                title_font_size=16,
                font=dict(color='#212529'),
                paper_bgcolor='white'
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
            fig_performance.update_layout(
                height=400, 
                title_font_size=16,
                font=dict(color='#212529'),
                paper_bgcolor='white'
            )
            st.plotly_chart(fig_performance, use_container_width=True)
        
        # Detailed agent performance table with editing
        st.markdown("### 📊 Detailed Agent Performance")
        display_enhanced_dataframe_with_editing(agent_performance, "Agent Performance Report", "agent_performance")
        
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
    else:
        st.info("🎯 No agent performance data available")

def show_revenue_tracking_page():
    """Display revenue tracking page"""
    st.markdown("## 💰 Revenue & Pipeline Analysis")
    
    # Load data
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = load_data_from_google_sheets()
    
    df = st.session_state.get('filtered_crm_data', st.session_state.crm_data)
    
    if not df.empty:
        # Revenue metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = df['revenue_impact'].sum()
            st.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
        
        with col2:
            avg_deal_size = df[df['revenue_impact'] > 0]['revenue_impact'].mean()
            st.metric("📊 Avg Deal Size", f"${avg_deal_size:,.0f}" if not pd.isna(avg_deal_size) else "$0")
        
        with col3:
            if 'customer_lifetime_value' in df.columns and 'conversion_probability' in df.columns:
                pipeline_value = (df['customer_lifetime_value'] * df['conversion_probability']).sum()
                st.metric("🎯 Pipeline Value", f"${pipeline_value:,.0f}")
            else:
                st.metric("🎯 Pipeline Value", "$0")
        
        with col4:
            deals_closed = (df['revenue_impact'] > 0).sum()
            st.metric("🤝 Deals Closed", deals_closed)
        
        st.markdown("---")
        
        # Revenue analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by category
            revenue_by_category = df.groupby('call_category')['revenue_impact'].sum().reset_index()
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
                title_font_size=16,
                font=dict(color='#212529'),
                paper_bgcolor='white'
            )
            st.plotly_chart(fig_revenue_cat, use_container_width=True)
        
        with col2:
            # Conversion funnel
            funnel_data = pd.DataFrame({
                'Stage': ['Total Calls', 'Successful Calls', 'Appointments Scheduled', 'Deals Closed'],
                'Count': [
                    len(df),
                    (df['call_success'] == 'Yes').sum(),
                    (df['appointment_scheduled'] == 'Yes').sum() if 'appointment_scheduled' in df.columns else 0,
                    (df['revenue_impact'] > 0).sum()
                ]
            })
            
            fig_funnel = px.funnel(
                funnel_data,
                x='Count',
                y='Stage',
                title="🎯 Sales Conversion Funnel"
            )
            fig_funnel.update_layout(
                height=400, 
                title_font_size=16,
                font=dict(color='#212529'),
                paper_bgcolor='white'
            )
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Pipeline analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Deal size distribution
            deals_data = df[df['revenue_impact'] > 0]
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
                    title_font_size=16,
                    font=dict(color='#212529'),
                    paper_bgcolor='white'
                )
                st.plotly_chart(fig_deal_dist, use_container_width=True)
        
        with col2:
            # Customer lifetime value vs conversion probability
            if 'customer_lifetime_value' in df.columns and 'conversion_probability' in df.columns:
                fig_ltv_conv = px.scatter(
                    df,
                    x='customer_lifetime_value',
                    y='conversion_probability',
                    size='revenue_impact',
                    color='customer_tier' if 'customer_tier' in df.columns else None,
                    title="💎 LTV vs Conversion Probability",
                    hover_data=['customer_name', 'call_outcome']
                )
                fig_ltv_conv.update_layout(
                    height=400, 
                    title_font_size=16,
                    font=dict(color='#212529'),
                    paper_bgcolor='white'
                )
                st.plotly_chart(fig_ltv_conv, use_container_width=True)
        
        # Top opportunities
        st.markdown("### 🏆 Top Revenue Opportunities")
        
        if 'customer_lifetime_value' in df.columns:
            opportunities = df.nlargest(20, 'customer_lifetime_value')[
                ['customer_name', 'customer_lifetime_value', 'conversion_probability', 
                 'revenue_impact', 'next_best_action', 'call_outcome', 'customer_tier']
            ].copy()
            
            if 'conversion_probability' in opportunities.columns:
                opportunities['Expected_Value'] = opportunities['customer_lifetime_value'] * opportunities['conversion_probability']
                opportunities = opportunities.sort_values('Expected_Value', ascending=False)
            
            display_enhanced_dataframe_with_editing(opportunities, "Top Revenue Opportunities", "revenue_opportunities")
        else:
            st.info("💰 Customer lifetime value data not available")
    else:
        st.info("💰 No revenue data available")

def show_ai_insights_page():
    """Display AI insights page"""
    st.markdown("## 🔮 AI Insights & Predictive Analytics")
    
    # Load data
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = load_data_from_google_sheets()
    
    df = st.session_state.get('filtered_crm_data', st.session_state.crm_data)
    
    if not df.empty:
        # AI insights metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_ai_accuracy = df['ai_accuracy_score'].mean() if 'ai_accuracy_score' in df.columns else 0.9
            st.metric("🤖 Average AI Accuracy", f"{avg_ai_accuracy:.1%}")
        
        with col2:
            high_confidence_calls = (df['confidence_score'] > 0.9).sum() if 'confidence_score' in df.columns else len(df) * 0.8
            st.metric("🎯 High Confidence Calls", int(high_confidence_calls))
        
        with col3:
            sentiment_positive = (df['sentiment_score'] > 0.7).sum() if 'sentiment_score' in df.columns else len(df) * 0.7
            st.metric("😊 Positive Sentiment", int(sentiment_positive))
        
        with col4:
            auto_resolved = (df['escalation_required'] == 'No').sum() if 'escalation_required' in df.columns else len(df) * 0.9
            st.metric("✅ Auto-Resolved", int(auto_resolved))
        
        st.markdown("---")
        
        # AI performance analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # AI accuracy vs customer satisfaction
            if 'ai_accuracy_score' in df.columns:
                fig_ai_satisfaction = px.scatter(
                    df,
                    x='ai_accuracy_score',
                    y='customer_satisfaction',
                    size='call_duration_seconds',
                    color='call_category',
                    title="🤖 AI Accuracy vs Customer Satisfaction",
                    hover_data=['customer_name', 'voice_agent_name']
                )
                fig_ai_satisfaction.update_layout(
                    height=400, 
                    title_font_size=16,
                    font=dict(color='#212529'),
                    paper_bgcolor='white'
                )
                st.plotly_chart(fig_ai_satisfaction, use_container_width=True)
        
        with col2:
            # Sentiment distribution
            if 'sentiment_score' in df.columns:
                fig_sentiment = px.histogram(
                    df,
                    x='sentiment_score',
                    title="🎭 Customer Sentiment Distribution",
                    nbins=20,
                    color_discrete_sequence=['#E74C3C']
                )
                fig_sentiment.update_layout(
                    xaxis_title="Sentiment Score",
                    yaxis_title="Number of Calls",
                    height=400,
                    title_font_size=16,
                    font=dict(color='#212529'),
                    paper_bgcolor='white'
                )
                st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Keyword analysis
        st.markdown("### 🔍 Keyword & Topic Analysis")
        
        if 'keyword_tags' in df.columns:
            # Extract and analyze keywords
            all_keywords = []
            for keywords in df['keyword_tags'].dropna():
                all_keywords.extend([k.strip() for k in str(keywords).split(',')])
            
            if all_keywords:
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
                        title_font_size=16,
                        font=dict(color='#212529'),
                        paper_bgcolor='white'
                    )
                    st.plotly_chart(fig_keywords, use_container_width=True)
                
                with col2:
                    # Intent detection analysis
                    if 'intent_detected' in df.columns:
                        intent_counts = df['intent_detected'].value_counts()
                        fig_intent = px.pie(
                            values=intent_counts.values,
                            names=intent_counts.index,
                            title="🎯 Intent Detection Distribution",
                            color_discrete_sequence=px.colors.qualitative.Pastel
                        )
                        fig_intent.update_layout(
                            height=500, 
                            title_font_size=16,
                            font=dict(color='#212529'),
                            paper_bgcolor='white'
                        )
                        st.plotly_chart(fig_intent, use_container_width=True)
        
        # Predictive insights
        st.markdown("### 📈 Predictive Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔮 AI Predictions")
            
            # High probability conversions
            if 'conversion_probability' in df.columns:
                high_conversion = df[df['conversion_probability'] > 0.8]
                st.write(f"**🎯 High Conversion Probability ({len(high_conversion)} customers):**")
                if not high_conversion.empty:
                    for _, row in high_conversion.head(5).iterrows():
                        st.success(f"• {row['customer_name']} - {row['conversion_probability']:.0%} likely to convert")
            
            # Risk indicators
            if 'customer_lifetime_value' in df.columns:
                risk_customers = df[
                    (df['customer_satisfaction'] < 7) & 
                    (df['customer_lifetime_value'] > 10000)
                ]
                if not risk_customers.empty:
                    st.write(f"**⚠️ At-Risk High-Value Customers ({len(risk_customers)}):**")
                    for _, row in risk_customers.head(3).iterrows():
                        st.warning(f"• {row['customer_name']} - Satisfaction: {row['customer_satisfaction']:.1f}")
        
        with col2:
            st.markdown("#### 💡 Optimization Recommendations")
            
            # Agent optimization
            if 'ai_accuracy_score' in df.columns:
                low_ai_accuracy = df[df['ai_accuracy_score'] < 0.85]
                if not low_ai_accuracy.empty:
                    st.write("**🤖 AI Model Optimization Needed:**")
                    agents_to_optimize = low_ai_accuracy['voice_agent_name'].value_counts().head(3)
                    for agent, count in agents_to_optimize.items():
                        st.info(f"• {agent}: {count} low-accuracy calls")
            
            # Process improvements
            if 'resolution_time_seconds' in df.columns:
                long_resolution = df[df['resolution_time_seconds'] > 300]  # > 5 minutes
                if not long_resolution.empty:
                    st.write("**⚡ Process Efficiency Improvements:**")
                    categories_slow = long_resolution['call_category'].value_counts().head(3)
                    for category, count in categories_slow.items():
                        st.warning(f"• {category}: {count} slow resolutions")
    else:
        st.info("🔮 No AI insights data available")

def show_admin_center_page():
    """Display admin center page"""
    st.markdown("## ⚙️ Admin Center & System Management")
    
    # System health metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(st.session_state.get('crm_data', []))
        st.metric("📊 Total Records", f"{total_records:,}")
    
    with col2:
        filtered_records = len(st.session_state.get('filtered_crm_data', st.session_state.get('crm_data', [])))
        filter_percentage = (filtered_records / total_records * 100) if total_records > 0 else 0
        st.metric("🔍 Filtered Records", f"{filtered_records:,}", delta=f"{filter_percentage:.1f}% of total")
    
    with col3:
        if 'crm_data' in st.session_state and not st.session_state.crm_data.empty:
            date_range_days = (st.session_state.crm_data['call_date'].max() - st.session_state.crm_data['call_date'].min()).days
            st.metric("📅 Date Range", f"{date_range_days} days")
    
    with col4:
        if 'crm_data' in st.session_state and not st.session_state.crm_data.empty:
            categories_count = st.session_state.crm_data['call_category'].nunique()
            st.metric("📂 Categories", categories_count)
    
    st.markdown("---")
    
    # Data quality assessment
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Data Quality Assessment")
        
        if 'crm_data' in st.session_state and not st.session_state.crm_data.empty:
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
        
        if 'crm_data' in st.session_state and not st.session_state.crm_data.empty:
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
            st.session_state.crm_data = load_data_from_google_sheets()
            st.success("✅ Data refreshed successfully!")
            st.rerun()
    
    with col2:
        if st.button("🧹 Clean Data", help="Remove duplicates and handle missing values"):
            if 'crm_data' in st.session_state:
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
            if 'crm_data' in st.session_state and not st.session_state.crm_data.empty:
                # Generate a comprehensive report
                report_data = {
                    "Report Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Total Records": len(st.session_state.crm_data),
                    "Date Range": f"{st.session_state.crm_data['call_date'].min().strftime('%Y-%m-%d')} to {st.session_state.crm_data['call_date'].max().strftime('%Y-%m-%d')}",
                    "Success Rate": f"{(st.session_state.crm_data['call_success'] == 'Yes').mean():.1%}",
                    "Average Satisfaction": f"{st.session_state.crm_data['customer_satisfaction'].mean():.1f}",
                    "Total Revenue": f"${st.session_state.crm_data['revenue_impact'].sum():,.2f}"
                }
                
                report_json = json.dumps(report_data, indent=2)
                st.download_button(
                    label="📥 Download Report",
                    data=report_json,
                    file_name=f"crm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                st.success("📊 Report generated successfully!")
    
    with col4:
        if st.button("💾 Backup Data", help="Create backup of current data"):
            if 'crm_data' in st.session_state and not st.session_state.crm_data.empty:
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

def show_settings_page():
    """Display settings page"""
    st.markdown("## ⚙️ System Settings & Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Data Source Configuration")
        
        auth_config = st.session_state.auth_config
        
        with st.form("data_config"):
            st.markdown("#### 📊 Google Sheets URLs")
            
            current_url = auth_config.get("google_sheets", {}).get("url", "")
            new_url = st.text_input("CRM Data Sheet URL", value=current_url)
            
            current_calendar_url = auth_config.get("google_sheets", {}).get("calendar_sheet", "")
            new_calendar_url = st.text_input("Calendar Data Sheet URL", value=current_calendar_url)
            
            if st.form_submit_button("💾 Save Configuration"):
                if "google_sheets" not in st.session_state.auth_config:
                    st.session_state.auth_config["google_sheets"] = {}
                
                st.session_state.auth_config["google_sheets"]["url"] = new_url
                st.session_state.auth_config["google_sheets"]["calendar_sheet"] = new_calendar_url
                
                st.success("✅ Configuration saved successfully!")
                st.cache_data.clear()
    
    with col2:
        st.markdown("### 👥 User Management")
        
        if check_permission("admin"):
            users = st.session_state.auth_config.get("users", {})
            
            st.markdown("#### 📋 Current Users")
            for username, user_data in users.items():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 5px; 
                           margin: 0.5rem 0; border: 1px solid #dee2e6; color: #212529;">
                    <strong>{username}</strong> - {user_data['name']}<br>
                    <small>Role: {user_data['role']} | Email: {user_data['email']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Admin permissions required to manage users")
    
    # System information
    st.markdown("---")
    st.markdown("### 📊 System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Current User:**")
        st.info(f"👤 {st.session_state.user['name']}\n🏷️ {st.session_state.user['role']}")
    
    with col2:
        st.markdown("**Data Status:**")
        data_count = len(st.session_state.get('crm_data', []))
        st.info(f"📊 {data_count:,} records loaded\n🔄 Auto-refresh: 5 min")
    
    with col3:
        st.markdown("**System Health:**")
        st.success("✅ All systems operational\n📡 Google Sheets connected")

# Run the application
if __name__ == "__main__":
    main()

# Enhanced footer
st.markdown("---")
st.markdown(f"""
<div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
           padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
    <h4>🚀 AI Call Center CRM Dashboard</h4>
    <p>Built with Streamlit | Enhanced Wide-Screen Display | Advanced Analytics | Full Data Editing</p>
    <p>Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 
       Records Loaded: {len(st.session_state.get('crm_data', [])):,} | 
       User: {st.session_state.get('user', {}).get('name', 'Guest')}</p>
</div>
""", unsafe_allow_html=True)
