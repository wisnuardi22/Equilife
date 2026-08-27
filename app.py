import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from PIL import Image

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "image", "logo.png")

try:
    logo_img = Image.open(logo_path)
except Exception:
    logo_img = "📊"

st.set_page_config(
    page_title="Equilife - Financial Balance", 
    layout="wide", 
    page_icon=logo_img
)

# --- HEADER & LANGUAGE SELECTOR (TOP RIGHT) ---
col_logo, col_title, col_lang = st.columns([1, 8, 3])

with col_logo:
    if isinstance(logo_img, Image.Image):
        st.image(logo_img, width=65)

with col_lang:
    lang_choice = st.selectbox("🌐 Language / Bahasa", ["Bahasa Indonesia 🇮🇩", "English 🇬🇧"], label_visibility="collapsed")

# Kamus Penerjemah Teks UI
T = {
    "Bahasa Indonesia 🇮🇩": {
        "title": "Equilife — Personal Financial Balance",
        "caption": "Sistem Pengendalian Anggaran (Budget vs Actual), Multi-Rekening & Tingkat Konsumtif",
        "wallets": "💳 Saldo Rekening / Dompet Riil",
        "hide_bal": "🙈 Sembunyikan Saldo",
        "show_bal": "👁️ Tampilkan Saldo",
        "add_tx": "➕ **Tambah Transaksi Baru (Input Cepat)**",
        "tx_type": "Jenis Transaksi",
        "expense": "Pengeluaran",
        "income": "Pemasukan",
        "transfer": "Transfer Antar Rekening",
        "date": "Tanggal",
        "acc_from": "Sumber Rekening",
        "acc_to": "Rekening Tujuan",
        "from_acc": "Dari Rekening",
        "to_acc": "Ke Rekening",
        "category": "Kategori Pos Pengeluaran",
        "not_needed": "- (Tidak Dibutuhkan)",
        "amount": "Nominal (Rp)",
        "notes": "Keterangan",
        "save": "💾 Simpan Transaksi",
        "success_save": "Transaksi berhasil disimpan!",
        "correct_title": "🗑️ **Koreksi / Hapus Transaksi Salah**",
        "correct_desc": "Pilih transaksi di bawah ini untuk menghapusnya (saldo akan otomatis dikembalikan):",
        "select_tx_del": "Pilih Transaksi yang Akan Dihapus:",
        "btn_del": "❌ Hapus Transaksi Ini",
        "success_del": "berhasil dihapus dan saldo rekening dikembalikan!",
        "budget_vs_act": "📋 Monitoring Target Anggaran (Budget vs Actual)",
        "target": "Target (Rp)",
        "actual": "Realisasi (Rp)",
        "remaining": "Sisa (Rp)",
        "status": "Status",
        "safe": "🟢 Aman",
        "over": "🔴 Overbudget",
        "dash_title": "📊 Dashboard Interaktif & Analisis Konsumtif",
        "filter_mode": "Tampilkan Berdasarkan Filter:",
        "monthly": "Bulanan",
        "weekly": "Mingguan",
        "week_num": "Pilih Minggu ke-",
        "lifestyle_ratio": "**Indikator Tingkat Konsumtif**",
        "life_metric": "Rasio Pengeluaran Lifestyle",
        "wise": "🟢 Bijak",
        "warning": "🟡 Waspada",
        "high_cons": "🔴 Konsumtif Tinggi",
        "pie_title": "Proporsi Pengeluaran",
        "no_data": "Belum ada data transaksi. Silakan input transaksi pertama kamu di atas!"
    },
    "English 🇬🇧": {
        "title": "Equilife — Personal Financial Balance",
        "caption": "Your personal financial dashboard to track income, expenses, and savings.",
        "wallets": "💳 Account Balances / Real Wallets",
        "hide_bal": "🙈 Hide Balance",
        "show_bal": "👁️ Show Balance",
        "add_tx": "➕ **Add New Transaction (Quick Input)**",
        "tx_type": "Transaction Type",
        "expense": "Expense",
        "income": "Income",
        "transfer": "Transfer Between Accounts",
        "date": "Date",
        "acc_from": "Source Account",
        "acc_to": "Destination Account",
        "from_acc": "From Account",
        "to_acc": "To Account",
        "category": "Expense Category",
        "not_needed": "- (Not Required)",
        "amount": "Amount (Rp)",
        "notes": "Notes",
        "save": "💾 Save Transaction",
        "success_save": "Transaction saved successfully!",
        "correct_title": "🗑️ **Correction / Delete Wrong Transaction**",
        "correct_desc": "Select a transaction below to delete it (account balances will be automatically restored):",
        "select_tx_del": "Select Transaction to Delete:",
        "btn_del": "❌ Delete This Transaction",
        "success_del": "deleted successfully and balance restored!",
        "budget_vs_act": "📋 Budget Target Monitoring (Budget vs Actual)",
        "target": "Target (Rp)",
        "actual": "Actual (Rp)",
        "remaining": "Remaining (Rp)",
        "status": "Status",
        "safe": "🟢 Safe",
        "over": "🔴 Overbudget",
        "dash_title": "📊 Interactive Dashboard & Consumption Analysis",
        "filter_mode": "Display Filtered By:",
        "monthly": "Monthly",
        "weekly": "Weekly",
        "week_num": "Select Week No.",
        "lifestyle_ratio": "**Lifestyle Consumption Indicator**",
        "life_metric": "Lifestyle Spending Ratio",
        "wise": "🟢 Wise",
        "warning": "🟡 Caution",
        "high_cons": "🔴 High Consumption",
        "pie_title": "Expense Ratio",
        "no_data": "No transaction data available yet. Please add your first transaction above!"
    }
}[lang_choice]

with col_title:
    st.title(T["title"])
    st.caption(T["caption"])

DB_FILE = os.path.join(BASE_DIR, "database.xlsx")

# --- DATABASE HELPER FUNCTIONS ---
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
    
    amt = new_tx["Amount"]
    if new_tx["Type"] in ["Pengeluaran", "Expense"]:
        accounts.loc[accounts["Account_Name"] == new_tx["Account_From"], "Current_Balance"] -= amt
    elif new_tx["Type"] in ["Pemasukan", "Income"]:
        accounts.loc[accounts["Account_Name"] == new_tx["Account_To"], "Current_Balance"] += amt
    else:
        accounts.loc[accounts["Account_Name"] == new_tx["Account_From"], "Current_Balance"] -= amt
        accounts.loc[accounts["Account_Name"] == new_tx["Account_To"], "Current_Balance"] += amt

    with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
        accounts.to_excel(writer, sheet_name="Accounts", index=False)
        budget.to_excel(writer, sheet_name="Budget", index=False)
        transactions.to_excel(writer, sheet_name="Transactions", index=False)

def delete_transaction(tx_id):
    accounts, budget, transactions = load_data()
    tx_to_delete = transactions[transactions["TX_ID"] == tx_id]
    
    if not tx_to_delete.empty:
        row = tx_to_delete.iloc[0]
        amt = row["Amount"]
        
        if row["Type"] in ["Pengeluaran", "Expense"]:
            accounts.loc[accounts["Account_Name"] == row["Account_From"], "Current_Balance"] += amt
        elif row["Type"] in ["Pemasukan", "Income"]:
            accounts.loc[accounts["Account_Name"] == row["Account_To"], "Current_Balance"] -= amt
        else:
            accounts.loc[accounts["Account_Name"] == row["Account_From"], "Current_Balance"] += amt
            accounts.loc[accounts["Account_Name"] == row["Account_To"], "Current_Balance"] -= amt

        transactions = transactions[transactions["TX_ID"] != tx_id]

        with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
            accounts.to_excel(writer, sheet_name="Accounts", index=False)
            budget.to_excel(writer, sheet_name="Budget", index=False)
            transactions.to_excel(writer, sheet_name="Transactions", index=False)

accounts_df, budget_df, tx_df = load_data()

# --- MODUL 1: WALLET CARDS ---
if "show_balance" not in st.session_state:
    st.session_state.show_balance = True

c_title, c_toggle = st.columns([8, 2])
with c_title:
    st.markdown(f"### {T['wallets']}")

with c_toggle:
    btn_label = T["hide_bal"] if st.session_state.show_balance else T["show_bal"]
    if st.button(btn_label, use_container_width=True):
        st.session_state.show_balance = not st.session_state.show_balance
        st.rerun()

cols = st.columns(len(accounts_df))
for i, row in accounts_df.iterrows():
    if st.session_state.show_balance:
        balance_display = f"Rp {row['Current_Balance']:,.0f}".replace(",", ".")
    else:
        balance_display = "Rp ••••••••"
        
    cols[i].metric(row["Account_Name"], balance_display)

st.markdown("---")

# --- MODUL 2: FORM INPUT TRANSAKSI ---
with st.expander(T["add_tx"], expanded=True):
    c_type1, c_type2 = st.columns([1, 2])
    tx_type_input = c_type1.selectbox(T["tx_type"], [T["expense"], T["income"], T["transfer"]])

    with st.form("add_tx_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tx_date = c1.date_input(T["date"], datetime.now())
        
        acc_list = accounts_df["Account_Name"].tolist()
        if tx_type_input == T["expense"]:
            acc_from = c2.selectbox(T["acc_from"], acc_list)
            acc_to = "-"
        elif tx_type_input == T["income"]:
            acc_from = "-"
            acc_to = c2.selectbox(T["acc_to"], acc_list)
        else:
            acc_from = c2.selectbox(T["from_acc"], acc_list, index=0)
            acc_to = c2.selectbox(T["to_acc"], acc_list, index=1)
            
        c4, c5, c6 = st.columns([3, 2, 4])
        
        if tx_type_input == T["expense"]:
            cat_options = budget_df["Category_Code"].astype(str) + " - " + budget_df["Category_Name"]
            cat_selected = c4.selectbox(T["category"], cat_options)
            cat_code = cat_selected.split(" - ")[0]
        else:
            c4.text_input(T["category"], value=T["not_needed"], disabled=True)
            cat_code = "-"
        
        amount = c5.number_input(T["amount"], min_value=0, value=50000, step=5000)
        notes = c6.text_input(T["notes"], "")
        
        submit = st.form_submit_button(T["save"])
        
        if submit:
            tx_id = f"TX-{len(tx_df)+1:04d}"
            new_record = {
                "TX_ID": tx_id,
                "Date": tx_date.strftime("%Y-%m-%d"),
                "Type": "Pengeluaran" if tx_type_input == T["expense"] else ("Pemasukan" if tx_type_input == T["income"] else "Transfer Antar Rekening"),
                "Account_From": acc_from,
                "Account_To": acc_to,
                "Category_Code": str(cat_code),
                "Amount": amount,
                "Notes": notes
            }
            save_transaction(new_record)
            st.success(T["success_save"])
            st.rerun()

# --- MODUL 3: KOREKSI / HAPUS TRANSAKSI ---
if not tx_df.empty:
    with st.expander(T["correct_title"]):
        st.write(T["correct_desc"])
        tx_options = tx_df.apply(lambda r: f"{r['TX_ID']} | {r['Date']} | {r['Type']} | Rp {r['Amount']:,.0f} | {r['Notes']}", axis=1)
        selected_tx = st.selectbox(T["select_tx_del"], tx_options)
        
        if st.button(T["btn_del"]):
            selected_tx_id = selected_tx.split(" | ")[0]
            delete_transaction(selected_tx_id)
            st.success(f"{selected_tx_id} {T['success_del']}")
            st.rerun()

st.markdown("---")

# --- MODUL 4: TABEL MONITORING ANGGARAN (BUDGET VS ACTUAL) ---
st.markdown(f"### {T['budget_vs_act']}")

if not tx_df.empty:
    tx_df["Date"] = pd.to_datetime(tx_df["Date"])
    tx_df["Week"] = tx_df["Date"].dt.isocalendar().week
    filtered_tx = tx_df[tx_df["Type"] == "Pengeluaran"]
        
    merged_budget = budget_df.copy()
    actual_spending = filtered_tx.groupby("Category_Code")["Amount"].sum().reset_index()
    merged_budget = pd.merge(merged_budget, actual_spending, on="Category_Code", how="left").fillna(0)
    merged_budget.rename(columns={"Amount": "Actual_Spending"}, inplace=True)
    merged_budget["Remaining"] = merged_budget["Target_Budget"] - merged_budget["Actual_Spending"]
    merged_budget["Status"] = merged_budget["Remaining"].apply(lambda x: T["safe"] if x >= 0 else T["over"])

    st.dataframe(
        merged_budget[["Category_Code", "Category_Name", "Target_Budget", "Actual_Spending", "Remaining", "Status"]],
        column_config={
            "Target_Budget": st.column_config.NumberColumn(T["target"], format="Rp %d"),
            "Actual_Spending": st.column_config.NumberColumn(T["actual"], format="Rp %d"),
            "Remaining": st.column_config.NumberColumn(T["remaining"], format="Rp %d"),
            "Status": st.column_config.TextColumn(T["status"]),
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info(T["no_data"])

st.markdown("---")

# --- MODUL 5: DASHBOARD INTERAKTIF & ANALISIS KONSUMTIF ---
st.markdown(f"### {T['dash_title']}")

if not tx_df.empty:
    # Filter Controls inside Main Dashboard Area
    f_col1, f_col2 = st.columns([3, 3])
    with f_col1:
        view_mode = st.radio(T["filter_mode"], [T["monthly"], T["weekly"]], horizontal=True)
    
    if view_mode == T["weekly"]:
        with f_col2:
            selected_week = st.selectbox(T["week_num"], sorted(tx_df["Week"].unique()))
            dash_tx = tx_df[(tx_df["Week"] == selected_week) & (tx_df["Type"] == "Pengeluaran")]
    else:
        dash_tx = tx_df[tx_df["Type"] == "Pengeluaran"]

    dash_budget = budget_df.copy()
    dash_spending = dash_tx.groupby("Category_Code")["Amount"].sum().reset_index()
    dash_budget = pd.merge(dash_budget, dash_spending, on="Category_Code", how="left").fillna(0)
    dash_budget.rename(columns={"Amount": "Actual_Spending"}, inplace=True)

    total_spent = dash_budget["Actual_Spending"].sum()
    konsumtif_spent = dash_budget[dash_budget["Type"] == "Konsumtif"]["Actual_Spending"].sum()
    ratio_konsumtif = (konsumtif_spent / 5700000) * 100 if 5700000 > 0 else 0

    c_met, c_chart = st.columns([4, 6])
    
    with c_met:
        st.write(T["lifestyle_ratio"])
        status_color = T["wise"] if ratio_konsumtif < 20 else (T["warning"] if ratio_konsumtif <= 35 else T["high_cons"])
        st.metric(T["life_metric"], f"{ratio_konsumtif:.1f}%", f"Status: {status_color}")
        
    with c_chart:
        chart_data = dash_budget.groupby("Type")["Actual_Spending"].sum().reset_index()
        fig = px.pie(chart_data, values="Actual_Spending", names="Type", title=T["pie_title"], color="Type",
                     color_discrete_map={"Konsumtif": "#FF4B4B", "Non-Konsumtif": "#00C853"})
        st.plotly_chart(fig, use_container_width=True)