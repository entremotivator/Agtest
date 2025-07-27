import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

st.set_page_config(page_title="CRM Dashboard", layout="wide")

# --- Sample CRM Data ---
def load_data():
    return pd.DataFrame([
        {"Name": "Alice", "Email": "alice@example.com", "Phone": "123-456-7890", "Stage": "Lead", "Last Contact": "2025-07-20", "Next Follow-up": "2025-07-30", "Status": "Open"},
        {"Name": "Bob", "Email": "bob@example.com", "Phone": "321-654-0987", "Stage": "Qualified", "Last Contact": "2025-07-10", "Next Follow-up": "2025-07-28", "Status": "In Progress"},
        {"Name": "Charlie", "Email": "charlie@example.com", "Phone": "555-555-5555", "Stage": "Proposal", "Last Contact": "2025-07-01", "Next Follow-up": "2025-07-27", "Status": "Won"},
    ])

df = load_data()
st.title("📊 CRM Dashboard using AgGrid")

# --- Sidebar Add Contact ---
with st.sidebar:
    st.subheader("➕ Add New Contact")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    stage = st.selectbox("Stage", ["Lead", "Qualified", "Proposal", "Negotiation", "Closed"])
    status = st.selectbox("Status", ["Open", "In Progress", "Won", "Lost"])
    last_contact = st.date_input("Last Contact")
    next_follow_up = st.date_input("Next Follow-up")

    if st.button("Add Contact"):
        new_row = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Stage": stage,
            "Last Contact": last_contact.strftime("%Y-%m-%d"),
            "Next Follow-up": next_follow_up.strftime("%Y-%m-%d"),
            "Status": status,
        }
        df.loc[len(df)] = new_row
        st.success("Contact added. Please refresh to see changes.")

# --- Grid Builder ---
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True, filter=True, sortable=True, resizable=True)
gb.configure_selection("single", use_checkbox=True)
gb.configure_grid_options(domLayout='normal')

# Custom cell color format based on status
cellsytle_jscode = JsCode("""
function(params) {
    if (params.value === 'Won') {
        return {
            'color': 'white',
            'backgroundColor': 'green'
        }
    } else if (params.value === 'Lost') {
        return {
            'color': 'white',
            'backgroundColor': 'red'
        }
    } else if (params.value === 'In Progress') {
        return {
            'color': 'black',
            'backgroundColor': 'yellow'
        }
    }
}
""")
gb.configure_column("Status", cellStyle=cellsytle_jscode)

# Add grid features
gb.configure_side_bar()  # Sidebar filters, columns, etc.
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)
gb.configure_grid_options(rowGroupPanelShow="always", enableRangeSelection=True)

grid_options = gb.build()

# --- Display Grid ---
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    height=500
)

updated_df = grid_response["data"]
selected = grid_response["selected_rows"]

# --- Export CSV ---
st.download_button("📥 Export CSV", updated_df.to_csv(index=False), "crm_export.csv")

# --- Row Deletion ---
if selected:
    st.warning("Selected Contact: " + selected[0]['Name'])
    if st.button("❌ Delete Selected Contact"):
        updated_df = updated_df[updated_df["Email"] != selected[0]["Email"]]
        st.success("Contact deleted. Please refresh to see changes.")

# --- Save Changes Button (Placeholder for DB/Sheet saving) ---
if st.button("💾 Save Changes"):
    st.success("Changes saved (this can be hooked to DB or Google Sheet).")

