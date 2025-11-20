# bank_app.py
import streamlit as st
import json
from pathlib import Path
import random
import string

# ===================== CONFIG =====================
st.set_page_config(page_title="Simple Bank", page_icon="🏦", layout="centered")

DATABASE = "database.json"

# ===================== DATA HANDLING =====================
def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

# ===================== account_number GENERATOR =====================
def generate_account_number():
    alpha = random.choices(string.ascii_uppercase, k=5)
    digits = random.choices(string.digits, k=4)
    code = alpha + digits
    random.shuffle(code)
    return "".join(code)

# ===================== MAIN APP =====================
def main():
    st.title("🏦 Simple Banking System")
    st.markdown("---")

    menu = [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "View Balance & Details",
        "Update Details",
        "Delete Account"
    ]

    choice = st.sidebar.selectbox("Menu", menu)

    data = load_data()

    # ===================== CREATE ACCOUNT =====================
    if choice == "Create Account":
        st.subheader("Create New Account")
        with st.form("create_account_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number (10 digits)")
            pin = st.text_input("Set 4-digit PIN", type="password", max_chars=4)

            submitted = st.form_submit_button("Create Account")
            if submitted:
                if not all([name, email, phone, pin]):
                    st.error("All fields are required!")
                elif len(phone) != 10 or not phone.isdigit():
                    st.error("Phone number must be exactly 10 digits!")
                elif len(pin) != 4 or not pin.isdigit():
                    st.error("PIN must be exactly 4 digits!")
                else:
                    account_no = generate_account_number()
                    new_user = {
                        "name": name.strip(),
                        "email": email.strip(),
                        "phone number": int(phone),
                        "pin": int(pin),
                        "account_number": account_no,
                        "balance": 0
                    }
                    data.append(new_user)
                    save_data(data)
                    st.success(f"Account Created Successfully!")
                    st.balloons()
                    st.info(f"Your account_number: **{account_no}**")
                    st.write("Save this number – you'll need it to log in!")

    # ===================== DEPOSIT MONEY =====================
    elif choice == "Deposit Money":
        st.subheader("Deposit Money")
        with st.form("deposit_form"):
            acc_no = st.text_input("account_number")
            pin = st.text_input("PIN", type="password", max_chars=4)
            amount = st.number_input("Amount to Deposit (₹)", min_value=1, max_value=10000)

            submitted = st.form_submit_button("Deposit")
            if submitted:
                user = next((u for u in data if u.get("account_number") == acc_no and u.get("pin") == int(pin or 0)),None)
                # user = next((u for u in data if u["account_number"] == acc_no and u["pin"] == int(pin or 0)), None)
                if not user:
                    st.error("Invalid account_number or PIN!")
                elif amount > 10000:
                    st.error("Maximum deposit limit is ₹10,000 per transaction!")
                else:
                    user["balance"] += int(amount)
                    save_data(data)
                    st.success(f"₹{amount} deposited successfully!")
                    st.write(f"**New Balance: ₹{user['balance']}**")

    # ===================== WITHDRAW MONEY ===================== streamlit run streamlitcode.py
    elif choice == "Withdraw Money":
        st.subheader("Withdraw Money")
        with st.form("withdraw_form"):
            acc_no = st.text_input("account_number")
            pin = st.text_input("PIN", type="password", max_chars=4)
            amount = st.number_input("Amount to Withdraw (₹)", min_value=1)

            submitted = st.form_submit_button("Withdraw")
            if submitted:
                user = next((u for u in data if u.get("account_number") == acc_no and u.get("pin") == int(pin or 0)),None)
                # user = next((u for u in data if u["account_number"] == acc_no and u["pin"] == int(pin or 0)), None)
                if not user:
                    st.error("Invalid account_number or PIN!")
                elif amount > user["balance"]:
                    st.error(f"Insufficient balance! Available: ₹{user['balance']}")
                else:
                    user["balance"] -= int(amount)
                    save_data(data)
                    st.success(f"₹{amount} withdrawn successfully!")
                    st.write(f"**Remaining Balance: ₹{user['balance']}**")

    # ===================== VIEW DETAILS =====================
    elif choice == "View Balance & Details":
        st.subheader("Account Details & Balance")
        acc_no = st.text_input("Enter account_number")
        pin = st.text_input("Enter PIN", type="password", max_chars=4)

        if st.button("Show Details"):
            user = next((u for u in data if u.get("account_number") == acc_no and u.get("pin") == int(pin or 0)),None)
            # user = next((u for u in data if u["account_number"] == acc_no and u["pin"] == int(pin or 0)), None)
            if not user:
                st.error("Invalid credentials!")
            else:
                st.success("Login Successful!")
                st.markdown(f"""
                **Name:** {user['name']}  
                **Email:** {user['email']}  
                **Phone:** {user['phone number']}  
                **account_number:** `{user['account_number']}`  
                **Current Balance:** ₹{user['balance']:,}
                """)

    # ===================== UPDATE DETAILS =====================
    elif choice == "Update Details":
        st.subheader("Update Account Details")
        acc_no = st.text_input("account_number")
        pin = st.text_input("Current PIN", type="password", max_chars=4)
        user = next((u for u in data if u.get("account_number") == acc_no and u.get("pin") == int(pin or 0)),None)
        # user = next((u for u in data if u["account_number"] == acc_no and u["pin"] == int(pin or 0)), None)

        if user:
            st.success("Account verified!")
            with st.form("update_form"):
                new_name = st.text_input("New Name (leave blank to keep current)", placeholder=user['name'])
                new_email = st.text_input("New Email (leave blank to keep current)", placeholder=user['email'])
                new_phone = st.text_input("New Phone (10 digits, leave blank to keep)", placeholder=str(user['phone number']))
                new_pin = st.text_input("New PIN (4 digits, leave blank to keep)", type="password", max_chars=4)

                if st.form_submit_button("Update Details"):
                    if new_name.strip():
                        user['name'] = new_name.strip()
                    if new_email.strip():
                        user['email'] = new_email.strip()
                    if new_phone.strip():
                        if len(new_phone) == 10 and new_phone.isdigit():
                            user['phone number'] = int(new_phone)
                        else:
                            st.error("Phone must be 10 digits!")
                            st.stop()
                    if new_pin:
                        if len(new_pin) == 4 and new_pin.isdigit():
                            user['pin'] = int(new_pin)
                        else:
                            st.error("New PIN must be 4 digits!")
                            st.stop()

                    save_data(data)
                    st.success("Details updated successfully!")
                    st.rerun()
        else:
            if st.button("Verify Account"):
                st.error("Invalid account_number or PIN!")

    # ===================== DELETE ACCOUNT =====================
    elif choice == "Delete Account":
        st.subheader("Delete Account ⚠️")
        st.warning("This action is permanent and cannot be undone!")

        acc_no = st.text_input("account_number to Delete")
        pin = st.text_input("PIN", type="password", max_chars=4)

        if st.button("Delete Permanently", type="primary"):
            user = next((u for u in data if u.get("account_number") == acc_no and u.get("pin") == int(pin or 0)),None)
            # user = next((u for u in data if u["account_number"] == acc_no and u["pin"] == int(pin or 0)), None)
            if not user:
                st.error("Invalid credentials!")
            else:
                data.remove(user)
                save_data(data)
                st.error("Account deleted permanently!")
                st.balloons()  # ironic celebration :)

    # ===================== FOOTER =====================
    st.markdown("---")
    st.caption("Simple Banking System • Made with ❤️ using Streamlit")

if __name__ == "__main__":
    main()
