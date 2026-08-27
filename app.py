import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from PIL import Image

# Load logo image
logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
if os.path.exists(logo_path):
    logo_image = Image.open(logo_path) 

# Set page configuration
st.set_page_config(
    page_title="Equilife - Financial Balance",
    page_icon=logo_image if os.path.exists(logo_path) else None,
    layout="wide",
)

# display logo and title
col_logo, col_title = st.columns([1, 12])

with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_image, width=65)  # Adjust the width as needed
    else:
        st.write("Logo not found.")

with col_title:
    st.title("Equilife - Financial Balance")
    st.caption("Your personal financial dashboard to track income, expenses, and savings.")

DB_FILE = "database.xlsx"

# --- HELPER FUNCTIONS FOR EXCEL DATABASE ---
def init_database():
    if not os.path.exists(DB_FILE):
        wb_accounts = pd.DataFrame([
            {"Account_ID": "ACC-01", "Account_Name": "Bank BRI", "Initial_Balance": 0, "Current_Balance": 0},
            {"Account_ID": "ACC-02", "Account_Name": "Bank Mandiri", "Initial_Balance": 0, "Current_Balance": 0},
            {"Account_ID": "ACC-03", "Account_Name": "ShopeePay", "Initial_Balance": 0, "Current_Balance": 0},
            {"Account_ID": "ACC-04", "Account_Name": "GoPay", "Initial_Balance": 0, "Current_Balance": 0},
            {"Account_ID": "ACC-05", "Account_Name": "Bank Jago", "Initial_Balance": 0, "Current_Balance": 0},
        ])
        
        wb_budget = pd.DataFrame([
            {"Category_Code": "5101", "Category_Name": "Zakat & Sedekah (2.5%)", "Type": "Non-Konsumtif", "Target_Budget": 142500},
            {"Category_Code": "5102", "Category_Name": "Transfer Orang Tua", "Type": "Non-Konsumtif", "Target_Budget": 1200000},
            {"Category_Code": "5103", "Category_Name": "Sewa Kost", "Type": "Non-Konsumtif", "Target_Budget": 700000},
            {"Category_Code": "5104", "Category_Name": "Bayar Utang / Cicilan", "Type": "Non-Konsumtif", "Target_Budget": 900000},
            {"Category_Code": "5105", "Category_Name": "Beban Pasangan / Pacar", "Type": "Konsumtif", "Target_Budget": 400000},
            {"Category_Code": "5106", "Category_Name": "Beban Hiburan & Main", "Type": "Konsumtif", "Target_Budget": 400000},
            {"Category_Code": "5107", "Category_Name": "Makan & Minum Harian", "Type": "Konsumtif", "Target_Budget": 1200000},
            {"Category_Code": "5108", "Category_Name": "Utilitas (Listrik/Internet)", "Type": "Non-Konsumtif", "Target_Budget": 250000},
            {"Category_Code": "5109", "Category_Name": "Transportasi & Bensin", "Type": "Non-Konsumtif", "Target_Budget": 300000},
            {"Category_Code": "1201", "Category_Name": "Tabungan / Investasi", "Type": "Non-Konsumtif", "Target_Budget": 407500},
        ])
        
        wb_tx = pd.DataFrame(columns=["TX_ID", "Date", "Type", "Account_From", "Account_To", "Category_Code", "Amount", "Notes"])
        
        with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
            wb_accounts.to_excel(writer, sheet_name="Accounts", index=False)
            wb_budget.to_excel(writer, sheet_name="Budget", index=False)
            wb_tx.to_excel(writer, sheet_name="Transactions", index=False)

def load_data():
    init_database()
    accounts = pd.read_excel(DB_FILE, sheet_name="Accounts")
    budget = pd.read_excel(DB_FILE, sheet_name="Budget", dtype={"Category_Code": str})
    transactions = pd.read_excel(DB_FILE, sheet_name="Transactions", dtype={"Category_Code": str})
    return accounts, budget, transactions

def save_transaction(new_tx):
    accounts, budget, transactions = load_data()
    transactions = pd.concat([transactions, pd.DataFrame([new_tx])], ignore_index=True)
    
    # Update Account Balances
    amt = new_tx["Amount"]
    if new_tx["Type"] == "Pengeluaran":
        accounts.loc[accounts["Account_Name"] == new_tx["Account_From"], "Current_Balance"] -= amt
    elif new_tx["Type"] == "Pemasukan":
        accounts.loc[accounts["Account_Name"] == new_tx["Account_To"], "Current_Balance"] += amt
    elif new_tx["Type"] == "Transfer Antar Rekening":
        accounts.loc[accounts["Account_Name"] == new_tx["Account_From"], "Current_Balance"] -= amt
        accounts.loc[accounts["Account_Name"] == new_tx["Account_To"], "Current_Balance"] += amt

    with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
        accounts.to_excel(writer, sheet_name="Accounts", index=False)
        budget.to_excel(writer, sheet_name="Budget", index=False)
        transactions.to_excel(writer, sheet_name="Transactions", index=False)

# --- LOAD DATA ---
accounts_df, budget_df, tx_df = load_data()

# --- MODUL 1: WALLET CARDS ---
st.markdown("### 💳 Saldo Rekening / Dompet Riil")
cols = st.columns(len(accounts_df))
for i, row in accounts_df.iterrows():
    cols[i].metric(row["Account_Name"], f"Rp {row['Current_Balance']:,.0f}".replace(",", "."))

st.markdown("---")

# --- MODUL 2: FORM INPUT TRANSAKSI ---
with st.expander("➕ **Tambah Transaksi Baru (Input Cepat)**", expanded=True):
    with st.form("add_tx_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        tx_date = c1.date_input("Tanggal", datetime.now())
        tx_type = c2.selectbox("Jenis Transaksi", ["Pengeluaran", "Pemasukan", "Transfer Antar Rekening"])
        
        acc_list = accounts_df["Account_Name"].tolist()
        if tx_type == "Pengeluaran":
            acc_from = c3.selectbox("Sumber Rekening", acc_list)
            acc_to = "-"
        elif tx_type == "Pemasukan":
            acc_from = "-"
            acc_to = c3.selectbox("Rekening Tujuan", acc_list)
        else:
            acc_from = c3.selectbox("Dari Rekening", acc_list, index=0)
            acc_to = c3.selectbox("Ke Rekening", acc_list, index=1)
            
        c4, c5, c6 = st.columns([3, 2, 4])
        cat_options = budget_df["Category_Code"].astype(str) + " - " + budget_df["Category_Name"]
        cat_selected = c4.selectbox("Kategori Pos Pengeluaran", cat_options if tx_type == "Pengeluaran" else ["-"])
        cat_code = cat_selected.split(" - ")[0] if tx_type == "Pengeluaran" else "-"
        
        amount = c5.number_input("Nominal (Rp)", min_value=0, value=50000, step=5000)
        notes = c6.text_input("Keterangan", "")
        
        submit = st.form_submit_button("💾 Simpan Transaksi")
        
        if submit:
            tx_id = f"TX-{len(tx_df)+1:04d}"
            new_record = {
                "TX_ID": tx_id,
                "Date": tx_date.strftime("%Y-%m-%d"),
                "Type": tx_type,
                "Account_From": acc_from,
                "Account_To": acc_to,
                "Category_Code": str(cat_code),
                "Amount": amount,
                "Notes": notes
            }
            save_transaction(new_record)
            st.success("Transaksi berhasil disimpan!")
            st.rerun()

# --- MODUL 3: FILTER & DASHBOARD KONSUMTIF ---
st.markdown("### 📊 Dashboard Equilife & Analysis")

st.sidebar.header("⚙️ Filter Dashboard")
view_mode = st.sidebar.radio("Tampilan Filter", ["Bulanan", "Mingguan"])

if not tx_df.empty:
    tx_df["Date"] = pd.to_datetime(tx_df["Date"])
    tx_df["Week"] = tx_df["Date"].dt.isocalendar().week
    
    if view_mode == "Mingguan":
        selected_week = st.sidebar.selectbox("Pilih Minggu ke-", sorted(tx_df["Week"].unique()))
        filtered_tx = tx_df[(tx_df["Week"] == selected_week) & (tx_df["Type"] == "Pengeluaran")]
    else:
        filtered_tx = tx_df[tx_df["Type"] == "Pengeluaran"]
        
    # Budget vs Actual Calculation
    merged_budget = budget_df.copy()
    actual_spending = filtered_tx.groupby("Category_Code")["Amount"].sum().reset_index()
    merged_budget = pd.merge(merged_budget, actual_spending, on="Category_Code", how="left").fillna(0)
    merged_budget.rename(columns={"Amount": "Actual_Spending"}, inplace=True)
    merged_budget["Remaining"] = merged_budget["Target_Budget"] - merged_budget["Actual_Spending"]
    merged_budget["Status"] = merged_budget["Remaining"].apply(lambda x: "🟢 Aman" if x >= 0 else "🔴 Overbudget")

    # Calculate Consumption Ratio
    total_spent = merged_budget["Actual_Spending"].sum()
    konsumtif_spent = merged_budget[merged_budget["Type"] == "Konsumtif"]["Actual_Spending"].sum()
    ratio_konsumtif = (konsumtif_spent / 5700000) * 100 if 5700000 > 0 else 0

    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        st.write("**Monitoring Target Anggaran (Budget vs Actual)**")
        st.dataframe(
            merged_budget[["Category_Code", "Category_Name", "Target_Budget", "Actual_Spending", "Remaining", "Status"]],
            column_config={
                "Target_Budget": st.column_config.NumberColumn("Target (Rp)", format="Rp %d"),
                "Actual_Spending": st.column_config.NumberColumn("Realisasi (Rp)", format="Rp %d"),
                "Remaining": st.column_config.NumberColumn("Sisa (Rp)", format="Rp %d"),
            },
            hide_index=True,
            use_container_width=True
        )

    with col_right:
        st.write("**Indikator Tingkat Konsumtif**")
        status_color = "🟢 Bijak" if ratio_konsumtif < 20 else ("🟡 Waspada" if ratio_konsumtif <= 35 else "🔴 Konsumtif Tinggi")
        st.metric("Rasio Pengeluaran Lifestyle", f"{ratio_konsumtif:.1f}%", f"Status: {status_color}")
        
        # Pie Chart Konsumtif vs Non-Konsumtif
        chart_data = merged_budget.groupby("Type")["Actual_Spending"].sum().reset_index()
        fig = px.pie(chart_data, values="Actual_Spending", names="Type", title="Proporsi Pengeluaran", color="Type",
                     color_discrete_map={"Konsumtif": "#FF4B4B", "Non-Konsumtif": "#00C853"})
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Belum ada data transaksi. Silakan input transaksi pertama kamu di atas!")
