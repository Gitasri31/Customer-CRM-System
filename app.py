import streamlit as st
import re
from crud import add_contact, get_all_contacts, update_contact, delete_contact
from db import create_table
import pandas as pd

create_table()  # make sure the table is created

st.set_page_config(page_title="Customer CRM",page_icon="📒", layout="centered")

st.title("📘 Customer CRM System")
st.caption("Manage your customers, contacts, and insights effortlessly.")


menu = ["Home","Add Contact", "View Contacts", "Update Contact", "Delete Contact","Dashboard"]
choice = st.sidebar.selectbox("Select Action", menu)

# Validation Functions
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit()

#Home
if choice == "Home":
    st.subheader("👋 Welcome to Customer CRM")
    st.markdown("""
    This is a simple yet powerful Contact Management System for small businesses or freelancers.
    
    👉 Use the sidebar to:
    - Add, view, update, or delete contacts
    - View category-wise and time-based dashboards
    
    ---
    👩‍💼 Built with ❤️ by Gitasri Das using Python, Streamlit & SQLite.
    """)

# Add Contact
if choice == "Add Contact":
    st.subheader("➕ Add New Contact")

    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    email = st.text_input("Email ID")
    phone = st.text_input("Phone Number")
    category = st.selectbox("Customer Category", ["New", "Returning", "VIP", "General"])

    
    address = st.text_area("Address")
    notes = st.text_area("Notes (optional)")
    last_interaction = st.date_input("Last Interaction Date")

    if st.button("Save Contact"):
        if fname and lname and address and email and phone:
            if not is_valid_email(email):
                st.error("❌ Invalid email format!")
            elif not is_valid_phone(phone):
                st.error("❌ Phone number must contain digits only!")
            else:
                try:
                    add_contact(fname, lname, address, email, phone, category, notes, last_interaction)
                    st.success("✅ Contact added successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠ All fields are required!")


#  View Contacts
elif choice == "View Contacts":
    st.subheader("📋 All Saved Contacts")

    data = get_all_contacts()
    if data:
        df = pd.DataFrame(data, columns=[
            "ID", "First Name", "Last Name", "Address", "Email", "Phone",
            "Category", "Notes", "Created At", "Last Interaction"
        ])

        # Filter/Search Options
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Search Name/Email/Phone")
        with col2:
            category_filter = st.selectbox("📂 Filter by Category", ["All", "New", "Returning", "VIP", "General"])

        if search:
            df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]

        if category_filter != "All":
            df = df[df["Category"] == category_filter]

        st.dataframe(df)

        # Download CSV
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), "contacts.csv", "text/csv")
    else:
        st.info("No contacts available.")


#  Update Contact
elif choice == "Update Contact":
    st.subheader("✏️ Update Existing Contact")

    data = get_all_contacts()
    df = pd.DataFrame(data, columns=[
        "ID", "First Name", "Last Name", "Address", "Email", "Phone",
        "Category", "Notes", "Created At", "Last Interaction"
    ])

    if not df.empty:
        selected_id = st.selectbox("Select Contact ID to Update", df["ID"])
        contact = df[df["ID"] == selected_id].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name", contact["First Name"])
            email = st.text_input("Email ID", contact["Email"])
            category = st.selectbox("Customer Category", ["New", "Returning", "VIP", "General"], index=["New", "Returning", "VIP", "General"].index(contact["Category"]))
        with col2:
            lname = st.text_input("Last Name", contact["Last Name"])
            phone = st.text_input("Phone Number", contact["Phone"])

        address = st.text_area("Address", contact["Address"])
        notes = st.text_area("Notes", contact["Notes"])
        last_interaction = st.date_input("Last Interaction Date", pd.to_datetime(contact["Last Interaction"]))

        if st.button("Update Now"):
            if fname and lname and address and email and phone:
                if not is_valid_email(email):
                    st.error("❌ Invalid email format!")
                elif not is_valid_phone(phone):
                    st.error("❌ Phone number must contain digits only!")
                else:
                    try:
                        update_contact(selected_id, fname, lname, address, email, phone, category, notes, last_interaction)
                        st.success("✅ Contact updated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Fill in all updated fields!")
    else:
        st.info("No contacts available to update.")



# Delete Contact
elif choice == "Delete Contact":
    st.subheader("🗑️ Delete Contact")

    data = get_all_contacts()
    df = pd.DataFrame(data, columns=["ID", "First Name", "Last Name", "Address", "Email", "Phone"])
    
    if not df.empty:
        selected_id = st.selectbox("Select Contact ID to Delete", df["ID"])
        
        if st.button("Delete"):
            try:
                delete_contact(selected_id)
                st.success("🗑️ Contact deleted successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.info("No contacts available to delete.")

#Dashboard
elif choice == "Dashboard":
    st.subheader("📊 Customer CRM Dashboard")

    data = get_all_contacts()
    if data:
        df = pd.DataFrame(data, columns=[
            "ID", "First Name", "Last Name", "Address", "Email", "Phone",
            "Category", "Notes", "Created At", "Last Interaction"
        ])

        # Category Distribution Pie Chart
        st.markdown("#### 📂 Category-wise Customer Distribution")
        category_count = df["Category"].value_counts().reset_index()
        category_count.columns = ["Category", "Count"]
        st.bar_chart(category_count.set_index("Category"))

        # Monthly Customer Additions
        st.markdown("#### 📅 New Customers Per Month")
        df["Created At"] = pd.to_datetime(df["Created At"])
        df["Month"] = df["Created At"].dt.strftime('%Y-%m')
        monthly_add = df.groupby("Month").size()
        st.line_chart(monthly_add)

    else:
        st.info("No data available to show insights.")

