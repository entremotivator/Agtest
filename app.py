import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configure page
st.set_page_config(
    page_title="AI Call Center CRM Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📞"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_crm_data():
    """Load the AI call center CRM data"""
    try:
        # Try to read from uploaded file first
        if 'uploaded_file' in st.session_state:
            df = pd.read_csv(st.session_state.uploaded_file)
        else:
            # Fallback sample data based on your CSV structure
            df = pd.DataFrame([
                {
                    "call_id": "CALL_001", "customer_name": "Sarah Johnson", "voice_agent_name": "AI Agent Emma",
                    "call_date": "2024-01-15", "call_start_time": "09:15:00", "call_end_time": "09:17:00",
                    "call_duration_seconds": 120, "call_duration_hms": "00:02:00", "cost": 4.9,
                    "call_success": "Yes", "appointment_scheduled": "Yes", "intent_detected": "Product_Inquiry",
                    "sentiment_score": 0.8, "confidence_score": 0.92, "keyword_tags": "software, marketing, demo, enterprise",
                    "summary_word_count": 32, "customer_satisfaction": 9.2, "resolution_time_seconds": 105,
                    "escalation_required": "No", "language_detected": "English", "emotion_detected": "Excited",
                    "speech_rate_wpm": 145, "silence_percentage": 8.5, "interruption_count": 2,
                    "ai_accuracy_score": 0.94, "follow_up_required": "Yes", "customer_tier": "Premium",
                    "call_complexity": "Medium", "agent_performance_score": 9.1, "call_outcome": "Demo_Scheduled",
                    "revenue_impact": 5000, "lead_quality_score": 8.7, "conversion_probability": 0.85,
                    "next_best_action": "Send_Demo_Materials", "customer_lifetime_value": 25000, "call_category": "Sales"
                },
                {
                    "call_id": "CALL_002", "customer_name": "Mike Chen", "voice_agent_name": "AI Agent Alex",
                    "call_date": "2024-01-15", "call_start_time": "10:30:00", "call_end_time": "10:33:00",
                    "call_duration_seconds": 180, "call_duration_hms": "00:03:00", "cost": 9.6,
                    "call_success": "Yes", "appointment_scheduled": "No", "intent_detected": "Technical_Support",
                    "sentiment_score": 0.9, "confidence_score": 0.88, "keyword_tags": "login, password, reset, account",
                    "summary_word_count": 28, "customer_satisfaction": 9.5, "resolution_time_seconds": 165,
                    "escalation_required": "No", "language_detected": "English", "emotion_detected": "Relieved",
                    "speech_rate_wpm": 138, "silence_percentage": 12.3, "interruption_count": 1,
                    "ai_accuracy_score": 0.91, "follow_up_required": "No", "customer_tier": "Standard",
                    "call_complexity": "Low", "agent_performance_score": 9.3, "call_outcome": "Issue_Resolved",
                    "revenue_impact": 0, "lead_quality_score": 7.2, "conversion_probability": 0.0,
                    "next_best_action": "Account_Monitoring", "customer_lifetime_value": 12000, "call_category": "Support"
                },
                {
                    "call_id": "CALL_003", "customer_name": "Emma Davis", "voice_agent_name": "AI Agent Sophia",
                    "call_date": "2024-01-15", "call_start_time": "11:45:00", "call_end_time": "11:46:00",
                    "call_duration_seconds": 60, "call_duration_hms": "00:01:00", "cost": 1.8,
                    "call_success": "Yes", "appointment_scheduled": "No", "intent_detected": "Billing_Inquiry",
                    "sentiment_score": 0.7, "confidence_score": 0.85, "keyword_tags": "billing, premium, charges, auto-upgrade",
                    "summary_word_count": 25, "customer_satisfaction": 8.1, "resolution_time_seconds": 55,
                    "escalation_required": "No", "language_detected": "English", "emotion_detected": "Concerned",
                    "speech_rate_wpm": 152, "silence_percentage": 15.2, "interruption_count": 0,
                    "ai_accuracy_score": 0.87, "follow_up_required": "No", "customer_tier": "Standard",
                    "call_complexity": "Low", "agent_performance_score": 8.5, "call_outcome": "Issue_Resolved",
                    "revenue_impact": 0, "lead_quality_score": 6.8, "conversion_probability": 0.0,
                    "next_best_action": "Billing_Review", "customer_lifetime_value": 8500, "call_category": "Billing"
                }
            ])
        
        # Convert date columns
        df['call_date'] = pd.to_datetime(df['call_date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Initialize session state
if 'crm_data' not in st.session_state:
    st.session_state.crm_data = load_crm_data()

# Sidebar for file upload and filters
with st.sidebar:
    st.header("📁 Data Management")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CRM Data (CSV)", type=['csv'])
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.crm_data = load_crm_data()
        st.success("Data uploaded successfully!")
    
    st.divider()
    
    # Filters
    st.header("🔍 Filters")
    df = st.session_state.crm_data
    
    if not df.empty:
        # Date range filter
        date_range = st.date_input(
            "Date Range",
            value=(df['call_date'].min(), df['call_date'].max()),
            min_value=df['call_date'].min(),
            max_value=df['call_date'].max()
        )
        
        # Category filter
        categories = st.multiselect(
            "Call Categories",
            options=df['call_category'].unique(),
            default=df['call_category'].unique()
        )
        
        # Customer tier filter
        tiers = st.multiselect(
            "Customer Tiers",
            options=df['customer_tier'].unique(),
            default=df['customer_tier'].unique()
        )
        
        # Call outcome filter
        outcomes = st.multiselect(
            "Call Outcomes",
            options=df['call_outcome'].unique(),
            default=df['call_outcome'].unique()
        )
        
        # Apply filters
        filtered_df = df[
            (df['call_date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))) &
            (df['call_category'].isin(categories)) &
            (df['customer_tier'].isin(tiers)) &
            (df['call_outcome'].isin(outcomes))
        ]
    else:
        filtered_df = df

# Main dashboard
st.title("📞 AI Call Center CRM Dashboard")
st.markdown("---")

# Key metrics row
if not filtered_df.empty:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_calls = len(filtered_df)
        st.metric("Total Calls", total_calls)
    
    with col2:
        success_rate = (filtered_df['call_success'] == 'Yes').sum() / len(filtered_df) * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    with col3:
        avg_satisfaction = filtered_df['customer_satisfaction'].mean()
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}")
    
    with col4:
        total_revenue = filtered_df['revenue_impact'].sum()
        st.metric("Revenue Impact", f"${total_revenue:,.0f}")
    
    with col5:
        avg_duration = filtered_df['call_duration_seconds'].mean() / 60
        st.metric("Avg Duration", f"{avg_duration:.1f} min")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Call Records", "📊 Analytics", "👥 Customer Management", 
    "🎯 Performance", "💰 Revenue Tracking", "⚙️ Admin Panel"
])

with tab1:
    st.header("Call Records Management")
    
    if not filtered_df.empty:
        # Configure AgGrid
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_default_column(
            editable=True, 
            filter=True, 
            sortable=True, 
            resizable=True,
            minWidth=100
        )
        gb.configure_selection("multiple", use_checkbox=True)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
        gb.configure_side_bar()
        
        # Custom cell styling
        success_style = JsCode("""
        function(params) {
            if (params.value === 'Yes') {
                return {'color': 'white', 'backgroundColor': '#28a745'}
            } else if (params.value === 'No') {
                return {'color': 'white', 'backgroundColor': '#dc3545'}
            }
        }
        """)
        
        satisfaction_style = JsCode("""
        function(params) {
            if (params.value >= 9) {
                return {'color': 'white', 'backgroundColor': '#28a745'}
            } else if (params.value >= 7) {
                return {'color': 'black', 'backgroundColor': '#ffc107'}
            } else {
                return {'color': 'white', 'backgroundColor': '#dc3545'}
            }
        }
        """)
        
        gb.configure_column("call_success", cellStyle=success_style)
        gb.configure_column("appointment_scheduled", cellStyle=success_style)
        gb.configure_column("customer_satisfaction", cellStyle=satisfaction_style)
        
        # Priority columns
        gb.configure_column("call_id", pinned="left", width=100)
        gb.configure_column("customer_name", pinned="left", width=150)
        gb.configure_column("call_date", width=120)
        gb.configure_column("call_category", width=100)
        gb.configure_column("customer_satisfaction", width=120)
        gb.configure_column("revenue_impact", width=120, type="numericColumn", valueFormatter="value.toLocaleString()")
        
        grid_options = gb.build()
        
        # Display grid
        grid_response = AgGrid(
            filtered_df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=False,
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True,
            height=600,
            width='100%'
        )
        
        updated_df = grid_response["data"]
        selected_rows = grid_response["selected_rows"]
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Export to CSV"):
                csv = updated_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"crm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if selected_rows and st.button("🗑️ Delete Selected"):
                # Remove selected rows
                selected_ids = [row['call_id'] for row in selected_rows]
                st.session_state.crm_data = st.session_state.crm_data[
                    ~st.session_state.crm_data['call_id'].isin(selected_ids)
                ]
                st.success(f"Deleted {len(selected_rows)} record(s)")
                st.rerun()
        
        with col3:
            if st.button("💾 Save Changes"):
                st.session_state.crm_data = updated_df
                st.success("Changes saved successfully!")
    else:
        st.info("No data available. Please upload a CSV file or check your filters.")

with tab2:
    st.header("Analytics Dashboard")
    
    if not filtered_df.empty:
        # Charts row 1
        col1, col2 = st.columns(2)
        
        with col1:
            # Call outcomes pie chart
            outcome_counts = filtered_df['call_outcome'].value_counts()
            fig_pie = px.pie(
                values=outcome_counts.values,
                names=outcome_counts.index,
                title="Call Outcomes Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Customer satisfaction by category
            satisfaction_by_category = filtered_df.groupby('call_category')['customer_satisfaction'].mean().reset_index()
            fig_bar = px.bar(
                satisfaction_by_category,
                x='call_category',
                y='customer_satisfaction',
                title="Average Satisfaction by Category",
                color='customer_satisfaction',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Charts row 2
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily call volume
            daily_calls = filtered_df.groupby('call_date').size().reset_index(name='call_count')
            fig_line = px.line(
                daily_calls,
                x='call_date',
                y='call_count',
                title="Daily Call Volume",
                markers=True
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            # Revenue by customer tier
            revenue_by_tier = filtered_df.groupby('customer_tier')['revenue_impact'].sum().reset_index()
            fig_bar2 = px.bar(
                revenue_by_tier,
                x='customer_tier',
                y='revenue_impact',
                title="Revenue Impact by Customer Tier",
                color='revenue_impact',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_bar2, use_container_width=True)
        
        # Performance metrics
        st.subheader("Performance Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_duration = filtered_df['call_duration_seconds'].mean()
            st.metric("Avg Call Duration", f"{avg_duration/60:.1f} min")
        
        with col2:
            avg_ai_accuracy = filtered_df['ai_accuracy_score'].mean()
            st.metric("AI Accuracy", f"{avg_ai_accuracy:.2%}")
        
        with col3:
            escalation_rate = (filtered_df['escalation_required'] == 'Yes').mean()
            st.metric("Escalation Rate", f"{escalation_rate:.1%}")
        
        with col4:
            follow_up_rate = (filtered_df['follow_up_required'] == 'Yes').mean()
            st.metric("Follow-up Rate", f"{follow_up_rate:.1%}")

with tab3:
    st.header("Customer Management")
    
    if not filtered_df.empty:
        # Customer overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Customer List")
            customer_summary = filtered_df.groupby('customer_name').agg({
                'call_id': 'count',
                'customer_satisfaction': 'mean',
                'customer_lifetime_value': 'first',
                'customer_tier': 'first',
                'revenue_impact': 'sum'
            }).reset_index()
            customer_summary.columns = ['Customer', 'Total Calls', 'Avg Satisfaction', 'Lifetime Value', 'Tier', 'Revenue Impact']
            
            # Customer grid
            gb_customers = GridOptionsBuilder.from_dataframe(customer_summary)
            gb_customers.configure_default_column(sortable=True, filter=True, resizable=True)
            gb_customers.configure_column("Lifetime Value", type="numericColumn", valueFormatter="'$' + value.toLocaleString()")
            gb_customers.configure_column("Revenue Impact", type="numericColumn", valueFormatter="'$' + value.toLocaleString()")
            gb_customers.configure_column("Avg Satisfaction", type="numericColumn", precision=1)
            
            customer_grid = AgGrid(
                customer_summary,
                gridOptions=gb_customers.build(),
                height=400,
                fit_columns_on_grid_load=True
            )
        
        with col2:
            st.subheader("Quick Stats")
            unique_customers = filtered_df['customer_name'].nunique()
            st.metric("Unique Customers", unique_customers)
            
            premium_customers = (filtered_df['customer_tier'] == 'Premium').sum()
            st.metric("Premium Customers", premium_customers)
            
            high_value_customers = (filtered_df['customer_lifetime_value'] > 50000).sum()
            st.metric("High Value Customers", high_value_customers)
        
        # Add new customer form
        st.subheader("Add New Customer")
        with st.expander("Add Customer"):
            with st.form("add_customer"):
                col1, col2 = st.columns(2)
                with col1:
                    new_customer_name = st.text_input("Customer Name")
                    new_customer_tier = st.selectbox("Customer Tier", ["Standard", "Premium", "Enterprise"])
                    new_lifetime_value = st.number_input("Lifetime Value", min_value=0, value=10000)
                
                with col2:
                    new_phone = st.text_input("Phone Number")
                    new_email = st.text_input("Email")
                    new_category = st.selectbox("Primary Category", ["Sales", "Support", "Billing", "Success"])
                
                if st.form_submit_button("Add Customer"):
                    # Add logic to create new customer record
                    st.success(f"Customer {new_customer_name} added successfully!")

with tab4:
    st.header("Agent Performance")
    
    if not filtered_df.empty:
        # Agent performance metrics
        agent_performance = filtered_df.groupby('voice_agent_name').agg({
            'call_id': 'count',
            'agent_performance_score': 'mean',
            'customer_satisfaction': 'mean',
            'call_success': lambda x: (x == 'Yes').mean(),
            'ai_accuracy_score': 'mean',
            'call_duration_seconds': 'mean'
        }).reset_index()
        
        agent_performance.columns = [
            'Agent', 'Total Calls', 'Performance Score', 
            'Customer Satisfaction', 'Success Rate', 'AI Accuracy', 'Avg Duration'
        ]
        
        # Display agent performance grid
        gb_agents = GridOptionsBuilder.from_dataframe(agent_performance)
        gb_agents.configure_default_column(sortable=True, filter=True, resizable=True)
        gb_agents.configure_column("Performance Score", type="numericColumn", precision=1)
        gb_agents.configure_column("Customer Satisfaction", type="numericColumn", precision=1)
        gb_agents.configure_column("Success Rate", type="numericColumn", valueFormatter="(value * 100).toFixed(1) + '%'")
        gb_agents.configure_column("AI Accuracy", type="numericColumn", valueFormatter="(value * 100).toFixed(1) + '%'")
        gb_agents.configure_column("Avg Duration", type="numericColumn", valueFormatter="(value / 60).toFixed(1) + ' min'")
        
        st.subheader("Agent Performance Overview")
        AgGrid(
            agent_performance,
            gridOptions=gb_agents.build(),
            height=300,
            fit_columns_on_grid_load=True
        )
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_agent_perf = px.scatter(
                agent_performance,
                x='Performance Score',
                y='Customer Satisfaction',
                size='Total Calls',
                hover_name='Agent',
                title="Agent Performance vs Customer Satisfaction"
            )
            st.plotly_chart(fig_agent_perf, use_container_width=True)
        
        with col2:
            fig_agent_calls = px.bar(
                agent_performance,
                x='Agent',
                y='Total Calls',
                title="Calls Handled by Agent",
                color='Performance Score',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_agent_calls, use_container_width=True)

with tab5:
    st.header("Revenue Tracking")
    
    if not filtered_df.empty:
        # Revenue metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = filtered_df['revenue_impact'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        
        with col2:
            avg_deal_size = filtered_df[filtered_df['revenue_impact'] > 0]['revenue_impact'].mean()
            st.metric("Avg Deal Size", f"${avg_deal_size:,.0f}")
        
        with col3:
            conversion_rate = (filtered_df['conversion_probability'] > 0.5).mean()
            st.metric("Conversion Rate", f"{conversion_rate:.1%}")
        
        with col4:
            pipeline_value = (filtered_df['customer_lifetime_value'] * filtered_df['conversion_probability']).sum()
            st.metric("Pipeline Value", f"${pipeline_value:,.0f}")
        
        # Revenue charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by outcome
            revenue_by_outcome = filtered_df.groupby('call_outcome')['revenue_impact'].sum().reset_index()
            fig_revenue = px.bar(
                revenue_by_outcome,
                x='call_outcome',
                y='revenue_impact',
                title="Revenue by Call Outcome",
                color='revenue_impact',
                color_continuous_scale='Greens'
            )
            fig_revenue.update_xaxis(tickangle=45)
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            # Lead quality distribution
            fig_lead = px.histogram(
                filtered_df,
                x='lead_quality_score',
                title="Lead Quality Score Distribution",
                nbins=10,
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig_lead, use_container_width=True)
        
        # Top opportunities
        st.subheader("Top Revenue Opportunities")
        top_opportunities = filtered_df.nlargest(10, 'customer_lifetime_value')[
            ['customer_name', 'customer_lifetime_value', 'conversion_probability', 'next_best_action', 'call_outcome']
        ]
        st.dataframe(top_opportunities, use_container_width=True)

with tab6:
    st.header("Admin Panel")
    
    # System statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Statistics")
        if not filtered_df.empty:
            st.write(f"**Total Records:** {len(st.session_state.crm_data)}")
            st.write(f"**Filtered Records:** {len(filtered_df)}")
            st.write(f"**Data Range:** {st.session_state.crm_data['call_date'].min()} to {st.session_state.crm_data['call_date'].max()}")
            st.write(f"**Categories:** {', '.join(st.session_state.crm_data['call_category'].unique())}")
    
    with col2:
        st.subheader("Data Quality")
        if not filtered_df.empty:
            missing_data = filtered_df.isnull().sum()
            if missing_data.sum() > 0:
                st.write("**Missing Data:**")
                for col, count in missing_data[missing_data > 0].items():
                    st.write(f"- {col}: {count} records")
            else:
                st.success("No missing data found!")
    
    # Bulk operations
    st.subheader("Bulk Operations")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Data"):
            st.session_state.crm_data = load_crm_data()
            st.success("Data refreshed!")
            st.rerun()
    
    with col2:
        if st.button("🧹 Clean Data"):
            # Remove duplicates, handle missing values
            original_count = len(st.session_state.crm_data)
            st.session_state.crm_data = st.session_state.crm_data.drop_duplicates()
            new_count = len(st.session_state.crm_data)
            st.success(f"Removed {original_count - new_count} duplicate records")
    
    with col3:
        if st.button("📊 Generate Report"):
            st.success("Report generation feature would be implemented here")
    
    # Configuration
    st.subheader("Configuration")
    with st.expander("System Settings"):
        auto_refresh = st.checkbox("Auto-refresh data every 5 minutes")
        email_notifications = st.checkbox("Enable email notifications")
        data_retention_days = st.number_input("Data retention (days)", min_value=30, max_value=365, value=90)
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("**AI Call Center CRM Dashboard** | Built with Streamlit & AgGrid | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
