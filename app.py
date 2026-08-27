import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from PIL import Image

# --- CONFIG & PAGE SETUP ---
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

# --- HEADER & LANGUAGE SELECTOR (ID / EN) ---
col_logo, col_title, col_lang = st.columns([1, 8, 2])

with col_logo:
    if isinstance(logo_img, Image.Image):
        st.image(logo_img, width=60)

with col_lang:
    lang_choice = st.selectbox("Lang", ["ID", "EN"], label_visibility="collapsed")

T = {
    "ID": {
        "title": "Equilife — Personal Financial Balance",
        "caption": "Sistem Pengendalian Anggaran Fleksibel, Multi-Rekening & Kalkulasi Target Otomatis",
        "wallets": "💳 Saldo Rekening / Dompet Riil",
        "hide_bal": "Sembunyikan Saldo",
        "show_bal": "Tampilkan Saldo",
        "add_account": "➕ Tambah Rekening / Dompet Baru",
        "acc_name": "Nama Rekening / Dompet Baru",
        "initial_bal": "Saldo Awal (Rp)",
        "save_account": "Simpan Rekening Baru",
        "success_acc": "Rekening baru berhasil ditambahkan!",
        "setting_title": "⚙️ Pengaturan Target Anggaran & Persentase (%)",
        "setting_desc": "Anda bisa mengisi langsung Persentase (%) atau Nominal (Rp) pada tabel di bawah. Keduanya akan saling menyesuaikan secara interaktif.",
        "save_setting": "Simpan Pengaturan Target",
        "success_setting": "Pengaturan target anggaran berhasil diperbarui!",
        "add_tx": "➕ Tambah Transaksi Baru (Input Cepat)",
        "tx_type": "Jenis Transaksi",
        "expense": "Pengeluaran",
        "income": "Pemasukan",
        "transfer": "Transfer Antar Rekening",
        "date": "Tanggal (dd/mm/yyyy)",
        "acc_from": "Sumber Rekening",
        "acc_to": "Rekening Tujuan",
        "from_acc": "Dari Rekening",
        "to_acc": "Ke Rekening",
        "category": "Kategori Pos Pengeluaran",
        "not_needed": "- (Tidak Dibutuhkan)",
        "amount": "Nominal Transaksi (Rp)",
        "notes": "Keterangan",
        "save": "Simpan Transaksi",
        "success_save": "Transaksi berhasil disimpan!",
        "correct_title": "✏️ Koreksi Transaksi (Edit / Hapus)",
        "correct_desc": "Pilih transaksi di bawah ini untuk mengedit atau menghapusnya:",
        "select_tx": "Pilih Transaksi:",
        "btn_edit": "Edit Transaksi",
        "btn_del": "Hapus Transaksi",
        "success_del": "berhasil dihapus dan saldo dikembalikan!",
        "success_edit": "berhasil diperbarui!",
        "save_changes": "Simpan Perubahan",
        "budget_vs_act": "📋 Monitoring Target Anggaran (Budget vs Actual)",
        "target": "Target (Rp)",
        "actual": "Realisasi (Rp)",
        "remaining": "Sisa (Rp)",
        "status": "Status Anggaran",
        "status_safe": "Terpenuhi",
        "status_over": "Melampaui Batas",
        "dash_title": "📊 Dashboard Interaktif & Analisis Konsumtif",
        "filter_mode": "Tampilkan Berdasarkan Filter:",
        "monthly": "Bulanan",
        "weekly": "Mingguan",
        "week_num": "Pilih Minggu ke-",
        "lifestyle_ratio": "**Indikator Tingkat Konsumtif**",
        "life_metric": "Rasio Pengeluaran Lifestyle",
        "wise": "Proporsional",
        "warning": "Perlu Perhatian",
        "high_cons": "Tingkat Konsumtif Tinggi",
        "pie_title": "Proporsi Alokasi Pengeluaran",
        "no_data": "Belum ada data transaksi. Silakan input transaksi pertama kamu di atas!"
    },
    "EN": {
        "title": "Equilife — Personal Financial Balance",
        "caption": "Flexible Budget Control System, Multi-Accounts & Auto Target Calculation",
        "wallets": "💳 Account Balances / Real Wallets",
        "hide_bal": "Hide Balance",
        "show_bal": "Show Balance",
        "add_account": "➕ Add New Account / Wallet",
        "acc_name": "New Account / Wallet Name",
        "initial_bal": "Initial Balance (Rp)",
        "save_account": "Save New Account",
        "success_acc": "New account added successfully!",
        "setting_title": "⚙️ Budget Target & Percentage (%) Settings",
        "setting_desc": "You can directly fill Percentage (%) or Amount (Rp) in the table below. Both auto-sync seamlessly.",
        "save_setting": "Save Target Settings",
        "success_setting": "Budget settings updated successfully!",
        "add_tx": "➕ Add New Transaction (Quick Input)",
        "tx_type": "Transaction Type",
        "expense": "Expense",
        "income": "Income",
        "transfer": "Transfer Between Accounts",
        "date": "Date (dd/mm/yyyy)",
        "acc_from": "Source Account",
        "acc_to": "Destination Account",
        "from_acc": "From Account",
        "to_acc": "To Account",
        "category": "Expense Category",
        "not_needed": "- (Not Required)",
        "amount": "Transaction Amount (Rp)",
        "notes": "Notes",
        "save": "Save Transaction",
        "success_save": "Transaction saved successfully!",
        "correct_title": "✏️ Transaction Correction (Edit / Delete)",
        "correct_desc": "Select a transaction below to edit or delete it:",
        "select_tx": "Select Transaction:",
        "btn_edit": "Edit Transaction",
        "btn_del": "Delete Transaction",
        "success_del": "deleted successfully and balance restored!",
        "success_edit": "updated successfully!",
        "save_changes": "Save Changes",
        "budget_vs_act": "📋 Budget Target Monitoring (Budget vs Actual)",
        "target": "Target (Rp)",
        "actual": "Actual (Rp)",
        "remaining": "Remaining (Rp)",
        "status": "Budget Status",
        "status_safe": "Target Met",
        "status_over": "Exceeded",
        "dash_title": "📊 Interactive Dashboard & Consumption Analysis",
        "filter_mode": "Display Filtered By:",
        "monthly": "Monthly",
        "weekly": "Weekly",
        "week_num": "Select Week No.",
        "lifestyle_ratio": "**Lifestyle Consumption Indicator**",
        "life_metric": "Lifestyle Spending Ratio",
        "wise": "Proportional",
        "warning": "Attention Needed",
        "high_cons": "High Consumption Level",
        "pie_title": "Expense Allocation Ratio",
        "no_data": "No transaction data available yet. Please add your first transaction above!"
    }
}[lang_choice]

with col_title:
    st.title(T['title'])
    st.caption(T['caption'])

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
            {"Category_Code": "5101", "Category_Name": "Zakat & Sedekah", "Type": "Non-Konsumtif", "Target_Percent": 2.5, "Target_Budget": 0.0},
            {"Category_Code": "5102", "Category_Name": "Transfer Orang Tua", "Type": "Non-Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "5103", "Category_Name": "Sewa Kost", "Type": "Non-Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "5104", "Category_Name": "Bayar Utang / Cicilan", "Type": "Non-Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "5105", "Category_Name": "Beban Pasangan / Pacar", "Type": "Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "5106", "Category_Name": "Beban Hiburan & Main", "Type": "Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "5107", "Category_Name": "Makan & Minum Harian", "Type": "Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "5108", "Category_Name": "Utilitas (Listrik/Internet)", "Type": "Non-Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "5109", "Category_Name": "Transportasi & Bensin", "Type": "Non-Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
            {"Category_Code": "1201", "Category_Name": "Tabungan / Investasi", "Type": "Non-Konsumtif", "Target_Percent": 0.0, "Target_Budget": 0.0},
        ])
        
        wb_tx = pd.DataFrame(columns=["TX_ID", "Date", "Type", "Account_From", "Account_To", "Category_Code", "Amount", "Notes"])
        
        with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
            wb_accounts.to_excel(writer, sheet_name="Accounts", index=False)
            wb_budget.to_excel(writer, sheet_name="Budget", index=False)
            wb_tx.to_excel(writer, sheet_name="Transactions", index=False)

def load_data():
    init_database()
    accounts = pd.read_excel(DB_FILE, sheet_name="Accounts")
    try:
        budget = pd.read_excel(DB_FILE, sheet_name="Budget", dtype={"Category_Code": str})
        if "Target_Percent" not in budget.columns:
            budget["Target_Percent"] = 0.0
        if "Target_Budget" not in budget.columns:
            budget["Target_Budget"] = 0.0
        budget["Target_Percent"] = pd.to_numeric(budget["Target_Percent"], errors="coerce").fillna(0.0).astype(float)
        budget["Target_Budget"] = pd.to_numeric(budget["Target_Budget"], errors="coerce").fillna(0.0).astype(float)
    except Exception:
        budget = pd.DataFrame(columns=["Category_Code", "Category_Name", "Type", "Target_Percent", "Target_Budget"])
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

def update_budget_targets(new_budget_df):
    accounts, _, transactions = load_data()
    with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
        accounts.to_excel(writer, sheet_name="Accounts", index=False)
        new_budget_df.to_excel(writer, sheet_name="Budget", index=False)
        transactions.to_excel(writer, sheet_name="Transactions", index=False)

def add_new_account(acc_name, initial_bal):
    accounts, budget, transactions = load_data()
    new_id = f"ACC-{len(accounts)+1:02d}"
    new_acc = pd.DataFrame([{
        "Account_ID": new_id,
        "Account_Name": acc_name,
        "Initial_Balance": initial_bal,
        "Current_Balance": initial_bal
    }])
    accounts = pd.concat([accounts, new_acc], ignore_index=True)
    with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
        accounts.to_excel(writer, sheet_name="Accounts", index=False)
        budget.to_excel(writer, sheet_name="Budget", index=False)
        transactions.to_excel(writer, sheet_name="Transactions", index=False)

accounts_df, budget_df, tx_df = load_data()

# --- TOTAL PEMASUKAN BULAN INI ---
total_income = tx_df[tx_df["Type"] == "Pemasukan"]["Amount"].sum() if not tx_df.empty else 0

# Sinkronisasi otomatis nilai jika belum tersimpan atau dihitung dari persen/rupiah yang ada
for idx, row in budget_df.iterrows():
    pct = float(row["Target_Percent"])
    bud = float(row["Target_Budget"])
    
    if row["Category_Code"] == "5101":
        pct = 2.5
        budget_df.at[idx, "Target_Percent"] = 2.5
        if total_income > 0:
            budget_df.at[idx, "Target_Budget"] = total_income * (2.5 / 100.0)
    else:
        if total_income > 0:
            if pct > 0 and bud == 0:
                budget_df.at[idx, "Target_Budget"] = total_income * (pct / 100.0)
            elif bud > 0 and pct == 0:
                budget_df.at[idx, "Target_Percent"] = (bud / total_income) * 100.0

# --- MODUL 1: WALLET CARDS & TAMBAH AKUN ---
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

with st.expander(T["add_account"]):
    with st.form("add_account_form", clear_on_submit=True):
        ac_name = st.text_input(T["acc_name"])
        ac_init = st.number_input(T["initial_bal"], min_value=0, value=0, step=10000)
        ac_submit = st.form_submit_button(T["save_account"])
        if ac_submit and ac_name:
            add_new_account(ac_name, int(ac_init))
            st.success(T["success_acc"])
            st.rerun()

st.markdown("---")

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
        
        amount = c5.number_input(T["amount"], min_value=0, value=50000, step=10000)
        c5.markdown(f"Format: **Rp {amount:,.0f}**".replace(",", "."))
        
        notes = c6.text_input(T["notes"], "")
        
        submit = st.form_submit_button(T["save"])
        
        if submit:
            tx_id = f"TX-{len(tx_df)+1:04d}"
            new_record = {
                "TX_ID": tx_id,
                "Date": tx_date.strftime("%d/%m/%Y"),
                "Type": "Pengeluaran" if tx_type_input == T["expense"] else ("Pemasukan" if tx_type_input == T["income"] else "Transfer Antar Rekening"),
                "Account_From": acc_from,
                "Account_To": acc_to,
                "Category_Code": str(cat_code),
                "Amount": int(amount),
                "Notes": notes
            }
            save_transaction(new_record)
            st.success(T["success_save"])
            st.rerun()

# --- MODUL 3: PENGATURAN TARGET & PERSENTASE (KEDUA KOLOM BISA DIEDIT BEBAS) ---
with st.expander(T["setting_title"], expanded=False):
    st.write(T["setting_desc"])
    if total_income > 0:
        st.info(f"Total Pemasukan (Gaji) Bulan Ini: **Rp {total_income:,.0f}** (Bisa isi Persentase % atau Nominal Rp secara fleksibel).".replace(",", "."))
    else:
        st.warning("Belum ada pemasukan tercatat. Silakan masukkan gaji/pemasukan terlebih dahulu pada menu input transaksi di atas.")
    
    with st.form("settings_form"):
        edited_budget_df = st.data_editor(
            budget_df, 
            column_config={
                "Category_Code": st.column_config.TextColumn("Kode", disabled=True),
                "Category_Name": st.column_config.TextColumn("Kategori Pos", disabled=True),
                "Type": st.column_config.TextColumn("Tipe", disabled=True),
                "Target_Budget": st.column_config.NumberColumn(T["target"], format="Rp %,d", min_value=0.0, step=10000.0),
                "Target_Percent": st.column_config.NumberColumn("Target (%)", format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1)
            },
            hide_index=True,
            use_container_width=True
        )
        
        submit_setting = st.form_submit_button(T["save_setting"])
        
        if submit_setting:
            edited_budget_df["Target_Percent"] = edited_budget_df["Target_Percent"].astype(float)
            edited_budget_df["Target_Budget"] = edited_budget_df["Target_Budget"].astype(float)
            
            for idx, row in edited_budget_df.iterrows():
                if row["Category_Code"] == "5101":
                    edited_budget_df.loc[idx, "Target_Percent"] = 2.5
                    if total_income > 0:
                        edited_budget_df.loc[idx, "Target_Budget"] = total_income * (2.5 / 100.0)
                else:
                    orig_pct = float(budget_df.loc[idx, "Target_Percent"])
                    new_pct = float(edited_budget_df.loc[idx, "Target_Percent"])
                    orig_bud = float(budget_df.loc[idx, "Target_Budget"])
                    new_bud = float(edited_budget_df.loc[idx, "Target_Budget"])
                    
                    # Jika user mengubah nominal rupiah, hitung persentasenya
                    if new_bud != orig_bud and total_income > 0:
                        edited_budget_df.loc[idx, "Target_Percent"] = (new_bud / total_income) * 100.0
                    # Jika user mengubah persentase, hitung nominal rupiahnya
                    elif new_pct != orig_pct and total_income > 0:
                        edited_budget_df.loc[idx, "Target_Budget"] = total_income * (new_pct / 100.0)

            update_budget_targets(edited_budget_df)
            st.success(T["success_setting"])
            st.rerun()

# --- MODUL 4: KOREKSI TRANSAKSI ---
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
            st.markdown("---")
            st.markdown(f"**Edit Form: {st.session_state.edit_active_id}**")
            
            with st.form("edit_tx_form"):
                ec1, ec2 = st.columns(2)
                try:
                    init_date = datetime.strptime(str(tx_row["Date"]), "%d/%m/%Y")
                except Exception:
                    init_date = datetime.now()
                    
                e_date = ec1.date_input(T["date"], init_date, format="DD/MM/YYYY")
                e_amount = ec2.number_input(T["amount"], min_value=0, value=int(tx_row["Amount"]), step=10000)
                ec2.markdown(f"Format: **Rp {e_amount:,.0f}**".replace(",", "."))
                
                e_notes = st.text_input(T["notes"], value=str(tx_row["Notes"]))
                e_submit = st.form_submit_button(T["save_changes"])
                
                if e_submit:
                    updated_record = {
                        "TX_ID": st.session_state.edit_active_id,
                        "Date": e_date.strftime("%d/%m/%Y"),
                        "Type": tx_row["Type"],
                        "Account_From": tx_row["Account_From"],
                        "Account_To": tx_row["Account_To"],
                        "Category_Code": str(tx_row["Category_Code"]),
                        "Amount": int(e_amount),
                        "Notes": e_notes
                    }
                    update_transaction(updated_record)
                    st.session_state.edit_active_id = None
                    st.success(f"{st.session_state.edit_active_id} {T['success_edit']}")
                    st.rerun()

st.markdown("---")

# --- MODUL 5: TABEL MONITORING ANGGARAN ---
st.markdown(f"### {T['budget_vs_act']}")

if not tx_df.empty:
    tx_df_calc = tx_df.copy()
    filtered_tx = tx_df_calc[tx_df_calc["Type"] == "Pengeluaran"]
        
    merged_budget = budget_df.copy()
    actual_spending = filtered_tx.groupby("Category_Code")["Amount"].sum().reset_index()
    merged_budget = pd.merge(merged_budget, actual_spending, on="Category_Code", how="left").fillna(0)
    merged_budget.rename(columns={"Amount": "Actual_Spending"}, inplace=True)
    merged_budget["Remaining"] = merged_budget["Target_Budget"] - merged_budget["Actual_Spending"]
    
    merged_budget["Status"] = merged_budget.apply(
        lambda r: T["status_safe"] if r["Actual_Spending"] <= r["Target_Budget"] else T["status_over"], 
        axis=1
    )

    st.dataframe(
        merged_budget[["Category_Code", "Category_Name", "Target_Percent", "Target_Budget", "Actual_Spending", "Remaining", "Status"]],
        column_config={
            "Target_Percent": st.column_config.NumberColumn("Target (%)", format="%.2f %%"),
            "Target_Budget": st.column_config.NumberColumn(T["target"], format="Rp %,d"),
            "Actual_Spending": st.column_config.NumberColumn(T["actual"], format="Rp %,d"),
            "Remaining": st.column_config.NumberColumn(T["remaining"], format="Rp %,d"),
            "Status": st.column_config.TextColumn(T["status"]),
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info(T["no_data"])

st.markdown("---")

# --- MODUL 6: DASHBOARD INTERAKTIF ---
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
    ratio_konsumtif = (konsumtif_spent / total_income) * 100 if total_income > 0 else 0

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
            hole=0.6
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)