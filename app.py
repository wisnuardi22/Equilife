import streamlit as st
import pandas as pd
import plotly.express as px
import os
import re
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

# --- EXPERT CSS INJECTION (POPPINS & SOFT UI) ---
st.markdown("""
<style>
    /* Import Poppins Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    /* Global Font & Background */
    html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {
        font-family: 'Poppins', sans-serif !important;
        background-color: #F4F7F8 !important;
        color: #0F172A !important;
    }
    
    /* Header Card (Expert Look) */
    .expert-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 35px 40px;
        border-radius: 24px;
        color: white;
        box-shadow: 0 15px 35px -5px rgba(15, 23, 42, 0.2);
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-text h1 {
        font-weight: 700;
        color: #00A884 !important;
        margin: 0 0 5px 0;
        font-size: 32px;
        letter-spacing: -0.5px;
    }
    .header-text p {
        color: #94A3B8;
        font-size: 15px;
        margin: 0;
        font-weight: 300;
    }

    /* Hide default borders for clean look */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    
    /* Soft Metric Cards */
    div[data-testid="metric-container"] {
        background: #FFFFFF !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 24px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.03) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.06) !important;
    }
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 26px !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Elegant Pill Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00A884, #007A63) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 50px !important; /* Pill shape */
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        box-shadow: 0 8px 16px rgba(0, 168, 132, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px rgba(0, 168, 132, 0.3) !important;
    }
    
    /* Rounded Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #00A884 !important;
        box-shadow: 0 0 0 3px rgba(0, 168, 132, 0.15) !important;
    }

    /* Expander Soft UI */
    .stExpander {
        background: #FFFFFF !important;
        border-radius: 24px !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.03) !important;
        margin-bottom: 20px !important;
    }
    summary {
        font-weight: 600 !important;
        color: #0F172A !important;
        padding: 16px 20px !important;
        border-radius: 24px !important;
    }
    summary:hover {
        color: #00A884 !important;
    }
    div[data-testid="stExpanderDetails"] {
        padding: 0 24px 24px 24px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER (EXPERT LOOK) & LANGUAGE ---
T_lang = st.radio("Lang", ["ID", "EN"], horizontal=True, label_visibility="collapsed")

# Kamus Teks UI
T = {
    "ID": {
        "title": "Equilife",
        "caption": "Personal Financial Balance & Budget System",
        "wallets": "💳 Saldo Rekening Anda",
        "hide_bal": "Sembunyikan Saldo",
        "show_bal": "Tampilkan Saldo",
        "add_tx": "➕ Tambah Transaksi Baru",
        "tx_type": "Jenis Transaksi",
        "expense": "Pengeluaran",
        "income": "Pemasukan",
        "transfer": "Transfer Antar Rekening",
        "date": "Tanggal (dd/mm/yyyy)",
        "acc_from": "Sumber Rekening",
        "acc_to": "Rekening Tujuan",
        "from_acc": "Dari Rekening",
        "to_acc": "Ke Rekening",
        "category": "Kategori Pengeluaran",
        "not_needed": "- (Otomatis)",
        "amount": "Nominal Transaksi",
        "notes": "Catatan",
        "save": "Simpan Transaksi",
        "success_save": "Transaksi berhasil disimpan!",
        "correct_title": "✏️ Koreksi Riwayat",
        "correct_desc": "Pilih transaksi untuk diedit atau dihapus:",
        "select_tx": "Pilih Transaksi:",
        "btn_edit": "Edit Transaksi",
        "btn_del": "Hapus Transaksi",
        "success_del": "berhasil dihapus. Saldo telah dipulihkan.",
        "success_edit": "berhasil diperbarui.",
        "save_changes": "Simpan Perubahan",
        "budget_vs_act": "📋 Monitoring Anggaran",
        "target": "Target (Rp)",
        "actual": "Realisasi (Rp)",
        "remaining": "Sisa (Rp)",
        "status": "Status",
        "status_safe": "🟢 Terpenuhi",
        "status_over": "🔴 Melampaui Batas",
        "dash_title": "📊 Analisis Gaya Hidup",
        "filter_mode": "Filter Dashboard:",
        "monthly": "Bulan Ini",
        "weekly": "Mingguan",
        "week_num": "Pilih Minggu",
        "lifestyle_ratio": "**Rasio Konsumtif**",
        "life_metric": "Lifestyle Spending",
        "wise": "🟢 Ideal",
        "warning": "🟡 Perlu Perhatian",
        "high_cons": "🔴 Over-Konsumtif",
        "pie_title": "Alokasi Dana",
        "no_data": "Belum ada transaksi. Silakan tambah data di atas."
    },
    "EN": {
        "title": "Equilife",
        "caption": "Personal Financial Balance & Budget System",
        "wallets": "💳 Your Balances",
        "hide_bal": "Hide Balance",
        "show_bal": "Show Balance",
        "add_tx": "➕ Add New Transaction",
        "tx_type": "Transaction Type",
        "expense": "Expense",
        "income": "Income",
        "transfer": "Transfer",
        "date": "Date (dd/mm/yyyy)",
        "acc_from": "Source Account",
        "acc_to": "Destination Account",
        "from_acc": "From Account",
        "to_acc": "To Account",
        "category": "Expense Category",
        "not_needed": "- (Auto)",
        "amount": "Transaction Amount",
        "notes": "Notes",
        "save": "Save Transaction",
        "success_save": "Transaction saved successfully!",
        "correct_title": "✏️ History Correction",
        "correct_desc": "Select a transaction to edit or delete:",
        "select_tx": "Select Transaction:",
        "btn_edit": "Edit Transaction",
        "btn_del": "Delete Transaction",
        "success_del": "deleted. Balances restored.",
        "success_edit": "updated successfully.",
        "save_changes": "Save Changes",
        "budget_vs_act": "📋 Budget Monitoring",
        "target": "Target (Rp)",
        "actual": "Actual (Rp)",
        "remaining": "Remaining (Rp)",
        "status": "Status",
        "status_safe": "🟢 On Track",
        "status_over": "🔴 Exceeded",
        "dash_title": "📊 Lifestyle Analysis",
        "filter_mode": "Dashboard Filter:",
        "monthly": "This Month",
        "weekly": "Weekly",
        "week_num": "Select Week",
        "lifestyle_ratio": "**Consumption Ratio**",
        "life_metric": "Lifestyle Spending",
        "wise": "🟢 Ideal",
        "warning": "🟡 Attention Needed",
        "high_cons": "🔴 Over-Consumptive",
        "pie_title": "Fund Allocation",
        "no_data": "No transactions yet. Please add data above."
    }
}[T_lang]

st.markdown(f"""
<div class="expert-header">
    <div class="header-text">
        <h1>{T['title']}</h1>
        <p>{T['caption']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- HELPER PARSER REBUAN ---
def format_thousand(val):
    clean = re.sub(r'[^\d]', '', str(val))
    if not clean:
        return "0"
    return f"{int(clean):,.0f}".replace(",", ".")

def parse_thousand(val_str):
    clean = re.sub(r'[^\d]', '', str(val_str))
    return int(clean) if clean else 0

DB_FILE = os.path.join(BASE_DIR, "database.xlsx")

# --- DATABASE FUNCTIONS ---
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

def update_transaction(updated_tx):
    delete_transaction(updated_tx["TX_ID"])
    save_transaction(updated_tx)

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
    balance_display = f"Rp {row['Current_Balance']:,.0f}".replace(",", ".") if st.session_state.show_balance else "Rp ••••••••"
    cols[i].metric(row["Account_Name"], balance_display)

st.markdown("<br>", unsafe_allow_html=True)

# --- MODUL 2: FORM INPUT TRANSAKSI ---
with st.expander(T["add_tx"], expanded=True):
    c_type1, c_type2 = st.columns([1, 2])
    tx_type_input = c_type1.selectbox(T["tx_type"], [T["expense"], T["income"], T["transfer"]])

    with st.form("add_tx_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        tx_date = c1.date_input(T["date"], datetime.now(), format="DD/MM/YYYY")
        
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
        
        raw_amount_input = c5.text_input(T["amount"], value="50.000")
        formatted_amount_str = format_thousand(raw_amount_input)
        
        notes = c6.text_input(T["notes"], "")
        
        submit = st.form_submit_button(T["save"])
        
        if submit:
            final_amount = parse_thousand(formatted_amount_str)
            tx_id = f"TX-{len(tx_df)+1:04d}"
            new_record = {
                "TX_ID": tx_id,
                "Date": tx_date.strftime("%d/%m/%Y"),
                "Type": "Pengeluaran" if tx_type_input == T["expense"] else ("Pemasukan" if tx_type_input == T["income"] else "Transfer Antar Rekening"),
                "Account_From": acc_from,
                "Account_To": acc_to,
                "Category_Code": str(cat_code),
                "Amount": final_amount,
                "Notes": notes
            }
            save_transaction(new_record)
            st.success(T["success_save"])
            st.rerun()

# --- MODUL 3: KOREKSI TRANSAKSI ---
if "edit_active_id" not in st.session_state:
    st.session_state.edit_active_id = None

if not tx_df.empty:
    with st.expander(T["correct_title"]):
        st.write(T["correct_desc"])
        tx_options = tx_df.apply(lambda r: f"{r['TX_ID']} | {r['Date']} | {r['Type']} | Rp {r['Amount']:,.0f} | {r['Notes']}", axis=1)
        selected_tx_str = st.selectbox(T["select_tx"], tx_options)
        selected_tx_id = selected_tx_str.split(" | ")[0]
        
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button(T["btn_edit"], use_container_width=True):
            st.session_state.edit_active_id = selected_tx_id

        if col_btn2.button(T["btn_del"], use_container_width=True):
            delete_transaction(selected_tx_id)
            st.session_state.edit_active_id = None
            st.success(f"{selected_tx_id} {T['success_del']}")
            st.rerun()

        if st.session_state.edit_active_id:
            tx_row = tx_df[tx_df["TX_ID"] == st.session_state.edit_active_id].iloc[0]
            st.markdown(f"**Edit Data: {st.session_state.edit_active_id}**")
            
            with st.form("edit_tx_form"):
                ec1, ec2 = st.columns(2)
                
                try:
                    init_date = datetime.strptime(str(tx_row["Date"]), "%d/%m/%Y")
                except Exception:
                    init_date = datetime.now()
                    
                e_date = ec1.date_input(T["date"], init_date, format="DD/MM/YYYY")
                e_amount_input = ec2.text_input(T["amount"], value=format_thousand(tx_row["Amount"]))
                e_notes = st.text_input(T["notes"], value=str(tx_row["Notes"]))
                e_submit = st.form_submit_button(T["save_changes"])
                
                if e_submit:
                    e_final_amount = parse_thousand(e_amount_input)
                    updated_record = {
                        "TX_ID": st.session_state.edit_active_id,
                        "Date": e_date.strftime("%d/%m/%Y"),
                        "Type": tx_row["Type"],
                        "Account_From": tx_row["Account_From"],
                        "Account_To": tx_row["Account_To"],
                        "Category_Code": str(tx_row["Category_Code"]),
                        "Amount": e_final_amount,
                        "Notes": e_notes
                    }
                    update_transaction(updated_record)
                    st.session_state.edit_active_id = None
                    st.success(f"{st.session_state.edit_active_id} {T['success_edit']}")
                    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- MODUL 4: TABEL MONITORING ---
st.markdown(f"### {T['budget_vs_act']}")

if not tx_df.empty:
    tx_df_calc = tx_df.copy()
    filtered_tx = tx_df_calc[tx_df_calc["Type"] == "Pengeluaran"]
        
    merged_budget = budget_df.copy()
    actual_spending = filtered_tx.groupby("Category_Code")["Amount"].sum().reset_index()
    merged_budget = pd.merge(merged_budget, actual_spending, on="Category_Code", how="left").fillna(0)
    merged_budget.rename(columns={"Amount": "Actual_Spending"}, inplace=True)
    merged_budget["Remaining"] = merged_budget["Target_Budget"] - merged_budget["Actual_Spending"]
    merged_budget["Status"] = merged_budget["Remaining"].apply(lambda x: T["status_safe"] if x >= 0 else T["status_over"])

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

st.markdown("<br>", unsafe_allow_html=True)

# --- MODUL 5: DASHBOARD ---
st.markdown(f"### {T['dash_title']}")

if not tx_df.empty:
    tx_df["Parsed_Date"] = pd.to_datetime(tx_df["Date"], format="%d/%m/%Y", errors="coerce")
    tx_df["Week"] = tx_df["Parsed_Date"].dt.isocalendar().week
    
    f_col1, f_col2 = st.columns([3, 3])
    with f_col1:
        view_mode = st.radio(T["filter_mode"], [T["monthly"], T["weekly"]], horizontal=True)
    
    if view_mode == T["weekly"]:
        with f_col2:
            available_weeks = sorted(tx_df["Week"].dropna().unique())
            selected_week = st.selectbox(T["week_num"], available_weeks if available_weeks else [1])
            dash_tx = tx_df[(tx_df["Week"] == selected_week) & (tx_df["Type"] == "Pengeluaran")]
    else:
        dash_tx = tx_df[tx_df["Type"] == "Pengeluaran"]

    dash_budget = budget_df.copy()
    dash_spending = dash_tx.groupby("Category_Code")["Amount"].sum().reset_index()
    dash_budget = pd.merge(dash_budget, dash_spending, on="Category_Code", how="left").fillna(0)
    dash_budget.rename(columns={"Amount": "Actual_Spending"}, inplace=True)

    konsumtif_spent = dash_budget[dash_budget["Type"] == "Konsumtif"]["Actual_Spending"].sum()
    ratio_konsumtif = (konsumtif_spent / 5700000) * 100 if 5700000 > 0 else 0

    c_met, c_chart = st.columns([4, 6])
    
    with c_met:
        st.write(T["lifestyle_ratio"])
        status_color = T["wise"] if ratio_konsumtif < 20 else (T["warning"] if ratio_konsumtif <= 35 else T["high_cons"])
        st.metric(T["life_metric"], f"{ratio_konsumtif:.1f}%", f"Status: {status_color}")
        
    with c_chart:
        chart_data = dash_budget.groupby("Type")["Actual_Spending"].sum().reset_index()
        fig = px.pie(
            chart_data, 
            values="Actual_Spending", 
            names="Type", 
            title=T["pie_title"], 
            color="Type",
            hole=0.6,
            color_discrete_map={"Konsumtif": "#0F172A", "Non-Konsumtif": "#00A884"}
        )
        fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=3)))
        fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)