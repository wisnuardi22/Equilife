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

# --- CUSTOM CSS STYLING (SAP / ENTERPRISE DASHBOARD THEME) ---
st.markdown("""
    <style>
    /* Global Theme Customization */
    .stApp {
        background-color: #11161d;
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1c2430;
        border-right: 1px solid #2d3748;
    }
    
    /* Card Container Styling */
    .metric-card {
        background-color: #1c2430;
        border: 1px solid #2d3748;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    /* Header Typography */
    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 600;
    }
    
    /* Custom Button Styling */
    .stButton>button {
        background-color: #FFB300;
        color: #11161d;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ffa000;
        color: #ffffff;
    }
    
    /* Dataframe Table Styling */
    dataframe {
        background-color: #1c2430 !important;
    }
    </style>
""", unsafe_allow_html=True)

DB_FILE = os.path.join(BASE_DIR, "database.xlsx")

# --- DATABASE FUNCTIONS ---
def init_database():
    if not os.path.exists(DB_FILE):
        wb_accounts = pd.DataFrame([
            {"Account_ID": "ACC-01", "Account_Name": "Bank BRI", "Initial_Balance": 4300000, "Current_Balance": 4300000},
            {"Account_ID": "ACC-02", "Account_Name": "Bank Mandiri", "Initial_Balance": 7800000, "Current_Balance": 7800000},
            {"Account_ID": "ACC-03", "Account_Name": "ShopeePay", "Initial_Balance": 320000, "Current_Balance": 320000},
            {"Account_ID": "ACC-04", "Account_Name": "GoPay", "Initial_Balance": 185000, "Current_Balance": 185000},
            {"Account_ID": "ACC-05", "Account_Name": "Bank Jago", "Initial_Balance": 12400000, "Current_Balance": 12400000},
        ])
        
        wb_budget = pd.DataFrame([
            {"Category_Code": "5101", "Category_Name": "Zakat & Sedekah", "Type": "Non-Konsumtif", "Target_Percent": 2.5, "Target_Budget": 142500},
            {"Category_Code": "5102", "Category_Name": "Transfer Orang Tua", "Type": "Non-Konsumtif", "Target_Percent": 21.05, "Target_Budget": 1200000},
            {"Category_Code": "5103", "Category_Name": "Sewa Kost", "Type": "Non-Konsumtif", "Target_Percent": 12.28, "Target_Budget": 700000},
            {"Category_Code": "5104", "Category_Name": "Bayar Utang / Cicilan", "Type": "Non-Konsumtif", "Target_Percent": 15.79, "Target_Budget": 900000},
            {"Category_Code": "5105", "Category_Name": "Beban Pasangan / Pacar", "Type": "Konsumtif", "Target_Percent": 7.02, "Target_Budget": 400000},
            {"Category_Code": "5106", "Category_Name": "Beban Hiburan & Main", "Type": "Konsumtif", "Target_Percent": 7.02, "Target_Budget": 400000},
            {"Category_Code": "5107", "Category_Name": "Makan & Minum Harian", "Type": "Konsumtif", "Target_Percent": 21.05, "Target_Budget": 1200000},
            {"Category_Code": "5108", "Category_Name": "Utilitas (Listrik/Internet)", "Type": "Non-Konsumtif", "Target_Percent": 4.39, "Target_Budget": 250000},
            {"Category_Code": "5109", "Category_Name": "Transportasi & Bensin", "Type": "Non-Konsumtif", "Target_Percent": 5.26, "Target_Budget": 300000},
            {"Category_Code": "1201", "Category_Name": "Tabungan / Investasi", "Type": "Non-Konsumtif", "Target_Percent": 7.15, "Target_Budget": 407500},
        ])
        
        wb_tx = pd.DataFrame([
            {"TX_ID": "TX-0001", "Date": "27/08/2026", "Type": "Pemasukan", "Account_From": "-", "Account_To": "Bank BRI", "Category_Code": "-", "Amount": 5700000, "Notes": "Gaji Agustus"},
            {"TX_ID": "TX-0002", "Date": "26/08/2026", "Type": "Pengeluaran", "Account_From": "Bank BRI", "Account_To": "-", "Category_Code": "5103", "Amount": 700000, "Notes": "Sewa kost bulan ini"},
            {"TX_ID": "TX-0003", "Date": "25/08/2026", "Type": "Pengeluaran", "Account_From": "GoPay", "Account_To": "-", "Category_Code": "5107", "Amount": 45000, "Notes": "Makan siang"},
            {"TX_ID": "TX-0004", "Date": "25/08/2026", "Type": "Transfer Antar Rekening", "Account_From": "Bank BRI", "Account_To": "GoPay", "Category_Code": "-", "Amount": 200000, "Notes": "Top-up GoPay"},
            {"TX_ID": "TX-0005", "Date": "24/08/2026", "Type": "Pengeluaran", "Account_From": "Bank Mandiri", "Account_To": "-", "Category_Code": "5102", "Amount": 1200000, "Notes": "Transfer ke orang tua"}
        ])
        
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

def update_budget_targets(new_budget_df):
    accounts, _, transactions = load_data()
    with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
        accounts.to_excel(writer, sheet_name="Accounts", index=False)
        new_budget_df.to_excel(writer, sheet_name="Budget", index=False)
        transactions.to_excel(writer, sheet_name="Transactions", index=False)

def add_new_account(acc_name, initial_bal):
    accounts, budget, transactions = load_data()
    new_id = f"ACC-{len(accounts)+1:02d}"
    new_acc = pd.DataFrame([{"Account_ID": new_id, "Account_Name": acc_name, "Initial_Balance": initial_bal, "Current_Balance": initial_bal}])
    accounts = pd.concat([accounts, new_acc], ignore_index=True)
    with pd.ExcelWriter(DB_FILE, engine="openpyxl") as writer:
        accounts.to_excel(writer, sheet_name="Accounts", index=False)
        budget.to_excel(writer, sheet_name="Budget", index=False)
        transactions.to_excel(writer, sheet_name="Transactions", index=False)

accounts_df, budget_df, tx_df = load_data()
total_income = tx_df[tx_df["Type"] == "Pemasukan"]["Amount"].sum() if not tx_df.empty else 0
total_expense = tx_df[tx_df["Type"] == "Pengeluaran"]["Amount"].sum() if not tx_df.empty else 0
total_balance = accounts_df["Current_Balance"].sum()

# --- SIDEBAR NAVIGATION (MENU UTAMA) ---
with st.sidebar:
    st.markdown("### 🏛️ **EQUILIFE**")
    st.caption("Enterprise Financial Control")
    st.markdown("---")
    
    menu = st.radio(
        "Navigasi Menu",
        ["Overview", "Transaksi", "Anggaran", "Analisis"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("⚙️ **Pengaturan Akun**")
    with st.expander("➕ Tambah Rekening Baru"):
        with st.form("sidebar_acc_form", clear_on_submit=True):
            acc_name_input = st.text_input("Nama Rekening")
            acc_init_input = st.number_input("Saldo Awal (Rp)", min_value=0, step=50000)
            if st.form_submit_button("Simpan Rekening"):
                if acc_name_input:
                    add_new_account(acc_name_input, int(acc_init_input))
                    st.success("Rekening berhasil ditambah!")
                    st.rerun()

# --- HEADER UTAMA ---
st.markdown(f"## 📊 Equilife — Enterprise Financial System")
st.markdown("---")

# ==========================================
# 1. MENU: OVERVIEW
# ==========================================
if menu == "Overview":
    st.markdown("### 📈 Ringkasan Saldo & Finansial")
    
    # Kartu Metrik Utama Ala SAP
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 0;">TOTAL SALDO REKENING</p>
                <h2 style="color: #FFB300; margin-top: 5px;">Rp {total_balance:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 0;">PEMASUKAN BULAN INI</p>
                <h2 style="color: #10B981; margin-top: 5px;">Rp {total_income:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 0;">PENGELUARAN BULAN INI</p>
                <h2 style="color: #ef4444; margin-top: 5px;">Rp {total_expense:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)

    # Rincian Saldo Dompet / Rekening
    st.markdown("#### 💳 Saldo per Akun")
    wallet_cols = st.columns(len(accounts_df))
    for idx, row in accounts_df.iterrows():
        wallet_cols[idx].markdown(f"""
            <div class="metric-card" style="padding: 12px; text-align: center;">
                <p style="font-size: 12px; color: #94a3b8; margin-bottom: 2px;">{row['Account_Name']}</p>
                <p style="font-size: 16px; font-weight: bold; color: #f8fafc; margin: 0;">Rp {row['Current_Balance']:,.0f}</p>
            </div>
        """, unsafe_allow_html=True)

    # Tabel Transaksi Terbaru (Clean Enterprise Table)
    st.markdown("#### 🕒 Transaksi Terakhir")
    if not tx_df.empty:
        st.dataframe(
            tx_df.tail(5)[["TX_ID", "Date", "Type", "Account_From", "Account_To", "Amount", "Notes"]],
            column_config={
                "TX_ID": "ID",
                "Date": "Tanggal",
                "Type": "Jenis",
                "Account_From": "Dari",
                "Account_To": "Ke",
                "Amount": st.column_config.NumberColumn("Nominal", format="Rp %,d"),
                "Notes": "Keterangan"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Belum ada data transaksi tercatat.")

# ==========================================
# 2. MENU: TRANSAKSI
# ==========================================
elif menu == "Transaksi":
    st.markdown("### 📝 Manajemen & Input Transaksi")
    
    with st.form("form_tambah_tx", clear_on_submit=True):
        col_t1, col_t2 = st.columns(2)
        tx_type = col_t1.selectbox("Jenis Transaksi", ["Pengeluaran", "Pemasukan", "Transfer Antar Rekening"])
        tx_date = col_t2.date_input("Tanggal Transaksi", datetime.now())
        
        acc_list = accounts_df["Account_Name"].tolist()
        c_acc1, c_acc2 = st.columns(2)
        
        if tx_type == "Pengeluaran":
            acc_from = c_acc1.selectbox("Sumber Rekening", acc_list)
            acc_to = "-"
            cat_options = budget_df["Category_Code"].astype(str) + " - " + budget_df["Category_Name"]
            cat_selected = c_acc2.selectbox("Kategori Pos Pengeluaran", cat_options)
            cat_code = cat_selected.split(" - ")[0]
        elif tx_type == "Pemasukan":
            acc_from = "-"
            acc_to = c_acc2.selectbox("Rekening Tujuan", acc_list)
            cat_code = "-"
        else:
            acc_from = c_acc1.selectbox("Dari Rekening", acc_list, index=0)
            acc_to = c_acc2.selectbox("Ke Rekening", acc_list, index=1 if len(acc_list)>1 else 0)
            cat_code = "-"
            
        c_amt1, c_amt2 = st.columns(2)
        amount = c_amt1.number_input("Nominal (Rp)", min_value=0, step=10000, value=50000)
        notes = c_amt2.text_input("Keterangan / Catatan")
        
        if st.form_submit_button("Simpan Transaksi"):
            tx_id = f"TX-{len(tx_df)+1:04d}"
            new_record = {
                "TX_ID": tx_id,
                "Date": tx_date.strftime("%d/%m/%Y"),
                "Type": tx_type,
                "Account_From": acc_from,
                "Account_To": acc_to,
                "Category_Code": cat_code,
                "Amount": int(amount),
                "Notes": notes
            }
            save_transaction(new_record)
            st.success("Transaksi berhasil dicatat dan saldo rekening diperbarui!")
            st.rerun()

    st.markdown("---")
    st.markdown("#### 📋 Riwayat Seluruh Transaksi")
    if not tx_df.empty:
        # Pilihan Hapus Transaksi
        del_id = st.selectbox("Pilih ID Transaksi untuk Dihapus", ["-- Pilih --"] + tx_df["TX_ID"].tolist())
        if del_id != "-- Pilih --":
            if st.button("Hapus Transaksi Terpilih"):
                delete_transaction(del_id)
                st.success(f"Transaksi {del_id} berhasil dihapus!")
                st.rerun()
                
        st.dataframe(
            tx_df,
            column_config={
                "TX_ID": "ID", "Date": "Tanggal", "Type": "Jenis", 
                "Account_From": "Dari", "Account_To": "Ke", 
                "Category_Code": "Kode Pos",
                "Amount": st.column_config.NumberColumn("Nominal", format="Rp %,d"),
                "Notes": "Keterangan"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Belum ada riwayat transaksi.")

# ==========================================
# 3. MENU: ANGGARAN
# ==========================================
elif menu == "Anggaran":
    st.markdown("### 📋 Monitoring Target Anggaran (Budget vs Actual)")
    st.info("Atur persentase (%) target anggaran Anda di bawah ini secara fleksibel. Nominal Rupiah akan menyesuaikan secara otomatis dengan total pemasukan.")

    # Sinkronisasi Budget berdasarkan total pemasukan
    for idx, row in budget_df.iterrows():
        pct = float(row["Target_Percent"])
        if row["Category_Code"] == "5101":
            pct = 2.5
            budget_df.loc[idx, "Target_Percent"] = 2.5
        budget_df.loc[idx, "Target_Budget"] = total_income * (pct / 100.0)

    edited_budget = st.data_editor(
        budget_df,
        column_config={
            "Category_Code": st.column_config.TextColumn("Kode", disabled=True),
            "Category_Name": st.column_config.TextColumn("Kategori Pos", disabled=True),
            "Type": st.column_config.TextColumn("Tipe", disabled=True),
            "Target_Percent": st.column_config.NumberColumn("Target (%)", format="%.2f %%", min_value=0.0, max_value=100.0, step=0.1),
            "Target_Budget": st.column_config.NumberColumn("Target (Rp)", format="Rp %,d", disabled=True)
        },
        hide_index=True,
        use_container_width=True
    )

    if st.button("Simpan Perubahan Anggaran"):
        update_budget_targets(edited_budget)
        st.success("Target anggaran berhasil diperbarui!")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 📊 Perbandingan Realisasi Anggaran")
    if not tx_df.empty:
        exp_tx = tx_df[tx_df["Type"] == "Pengeluaran"]
        actual_spend = exp_tx.groupby("Category_Code")["Amount"].sum().reset_index()
        monitoring_df = pd.merge(budget_df, actual_spend, on="Category_Code", how="left").fillna(0)
        monitoring_df.rename(columns={"Amount": "Realisasi"}, inplace=True)
        monitoring_df["Sisa"] = monitoring_df["Target_Budget"] - monitoring_df["Realisasi"]
        monitoring_df["Status"] = monitoring_df.apply(lambda r: "Terpenuhi" if r["Realisasi"] <= r["Target_Budget"] else "Melampaui Batas", axis=1)

        st.dataframe(
            monitoring_df[["Category_Code", "Category_Name", "Target_Budget", "Realisasi", "Sisa", "Status"]],
            column_config={
                "Category_Code": "Kode",
                "Category_Name": "Kategori",
                "Target_Budget": st.column_config.NumberColumn("Target", format="Rp %,d"),
                "Realisasi": st.column_config.NumberColumn("Realisasi", format="Rp %,d"),
                "Sisa": st.column_config.NumberColumn("Sisa Budget", format="Rp %,d"),
                "Status": "Status"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Visualisasi Enterprise (Bar Chart bersih bernuansa Korporat SAP)
        fig_bar = px.bar(
            monitoring_df, 
            x="Category_Name", 
            y=["Target_Budget", "Realisasi"], 
            barmode="group",
            title="Grafik Komparasi Target vs Realisasi Anggaran",
            color_discrete_sequence=["#FFB300", "#00B09B"] # Palet Mango & Teal Korporat
        )
        fig_bar.update_layout(
            plot_bgcolor="#1c2430", 
            paper_bgcolor="#11161d", 
            font_color="#f8fafc",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#2d3748")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# 4. MENU: ANALISIS
# ==========================================
elif menu == "Analisis":
    st.markdown("### 📊 Analisis Konsumtif & Alokasi Keuangan")
    
    if not tx_df.empty:
        exp_tx = tx_df[tx_df["Type"] == "Pengeluaran"]
        analysis_df = pd.merge(exp_tx, budget_df, on="Category_Code", how="left").fillna("Konsumtif")
        
        konsumtif_total = analysis_df[analysis_df["Type_y"] == "Konsumtif"]["Amount"].sum()
        ratio_lifestyle = (konsumtif_total / total_income) * 100 if total_income > 0 else 0

        c_ana1, c_ana2 = st.columns(2)
        with c_ana1:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #94a3b8; font-size: 14px;">RASIO PENGELUARAN KONSUMTIF</p>
                    <h1 style="color: #FFB300;">{ratio_lifestyle:.1f}%</h1>
                    <p style="font-size: 13px; color: #10B981;">Status: Proporsional & Sehat (< 35%)</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c_ana2:
            pie_data = analysis_df.groupby("Type_y")["Amount"].sum().reset_index()
            fig_pie = px.pie(
                pie_data, 
                values="Amount", 
                names="Type_y", 
                title="Proporsi Konsumtif vs Non-Konsumtif",
                hole=0.5,
                color_discrete_sequence=["#FFB300", "#00B09B", "#3b82f6"]
            )
            fig_pie.update_layout(
                plot_bgcolor="#1c2430", 
                paper_bgcolor="#1c2430", 
                font_color="#f8fafc",
                margin=dict(t=30, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Belum cukup data transaksi untuk melakukan analisis mendalam.")