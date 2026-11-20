import sys
import sqlite3
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QTabWidget, QComboBox, QMessageBox, QFormLayout,
                             QDateEdit, QGroupBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor

DB_NAME = "laundry_uas_final.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # CREATE TABLE ADA 3
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT NOT NULL, address TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS packages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price_per_kg INTEGER NOT NULL, duration_days INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER, package_id INTEGER, weight REAL, items_count INTEGER, discount INTEGER, total_price INTEGER, start_date TEXT, end_date TEXT, status TEXT, FOREIGN KEY(customer_id) REFERENCES customers(id), FOREIGN KEY(package_id) REFERENCES packages(id))''')
    
    # CEK dan INSERT DATA AWAL
    cursor.execute("SELECT count(*) FROM packages")
    if cursor.fetchone()[0] == 0:
        # Packages 5 record
        cursor.execute("INSERT INTO packages (name, price_per_kg, duration_days) VALUES ('Cuci Komplit Reguler', 6000, 3)")
        cursor.execute("INSERT INTO packages (name, price_per_kg, duration_days) VALUES ('Cuci Komplit Express', 10000, 1)")
        cursor.execute("INSERT INTO packages (name, price_per_kg, duration_days) VALUES ('Setrika Komplit', 8000, 2)")
        cursor.execute("INSERT INTO packages (name, price_per_kg, duration_days) VALUES ('Cuci Kering Express', 12000, 1)")
        cursor.execute("INSERT INTO packages (name, price_per_kg, duration_days) VALUES ('Paket Hemat Bundle', 5000, 4)")
        
        # Customers 5 record
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Reno Santoso', '08123456789', 'Jl. Merdeka No. 1')")
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Hisam Widodo', '08223344556', 'Jl. Proklamasi No. 17')")
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Siti Aminah', '08334455667', 'Jl. Kebangsaan No. 8')")
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Ahmad Yani', '08445566778', 'Jl. Pahlawan No. 4')")
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES ('Dewi Sartika', '08556677889', 'Jl. Cinta No. 10')")
        
        # Transaksi 5 record
        cursor.execute("INSERT INTO transactions (customer_id, package_id, weight, items_count, discount, total_price, start_date, end_date, status) VALUES (1, 1, 2.5, 10, 5000, 15000, '2023-10-01', '2023-10-04', 'Selesai')")
        cursor.execute("INSERT INTO transactions (customer_id, package_id, weight, items_count, discount, total_price, start_date, end_date, status) VALUES (2, 2, 3.0, 15, 10000, 30000, '2023-10-02', '2023-10-03', 'Selesai')")
        cursor.execute("INSERT INTO transactions (customer_id, package_id, weight, items_count, discount, total_price, start_date, end_date, status) VALUES (3, 1, 1.0, 5, 0, 6000, '2023-10-03', '2023-10-06', 'Proses')")
        cursor.execute("INSERT INTO transactions (customer_id, package_id, weight, items_count, discount, total_price, start_date, end_date, status) VALUES (4, 2, 4.0, 20, 20000, 80000, '2023-10-04', '2023-10-05', 'Diambil')")
        cursor.execute("INSERT INTO transactions (customer_id, package_id, weight, items_count, discount, total_price, start_date, end_date, status) VALUES (5, 3, 2.0, 8, 3000, 13000, '2023-10-05', '2023-10-07', 'Selesai')")
        
        conn.commit()
    conn.close()

class LaundryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Laundry Project UAS")
        self.resize(1100, 750)
        
        # Set style yang lebih terang dan mudah dilihat
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f5f5f5;
                color: #000000;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #000000;
                padding: 8px 20px;
                margin-right: 2px;
                border: 1px solid #cccccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                font-weight: bold;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #000000;
            }
            QGroupBox::title {
                color: #4CAF50;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                color: #000000;
                font-size: 11pt;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #4CAF50;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                gridline-color: #ddd;
                color: #000000;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: 1px solid #1976D2;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QLabel {
                color: #000000;
                font-size: 10pt;
            }
        """)
        
        init_db()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        self.tab_trans_list = QWidget()
        self.setup_tab_trans_list()
        self.tabs.addTab(self.tab_trans_list, "Daftar Transaksi")
        self.tab_trans_form = QWidget()
        self.setup_tab_trans_form()
        self.tabs.addTab(self.tab_trans_form, "Input Transaksi")
        self.tab_cust = QWidget()
        self.setup_tab_customers()
        self.tabs.addTab(self.tab_cust, "Kelola Pelanggan")
        
        self.current_record_ids = []
        self.current_nav_index = -1
        
        self.load_combos()
        self.load_transactions()
        self.load_customers_list()
        self.tabs.currentChanged.connect(self.on_tab_changed) 

    def get_db(self): return sqlite3.connect(DB_NAME)

    def setup_tab_customers(self):
        layout = QHBoxLayout()
        form_group = QGroupBox("Input / Edit Pelanggan")
        form_layout = QFormLayout()
        self.cust_id = QLineEdit(); self.cust_id.setPlaceholderText("Auto"); self.cust_id.setReadOnly(True)
        self.cust_name = QLineEdit(); self.cust_name.setPlaceholderText("Nama Lengkap")
        self.cust_phone = QLineEdit(); self.cust_phone.setPlaceholderText("08xxx")
        self.cust_addr = QLineEdit()
        btn_save = QPushButton("SIMPAN"); btn_save.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        btn_save.clicked.connect(self.save_customer)
        btn_del = QPushButton("HAPUS"); btn_del.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        btn_del.clicked.connect(self.delete_customer)
        btn_reset = QPushButton("Reset"); btn_reset.setStyleSheet("background-color: #FF9800; color: white; padding: 10px;")
        btn_reset.clicked.connect(self.clear_cust_form)
        form_layout.addRow("ID:", self.cust_id); form_layout.addRow("Nama:", self.cust_name)
        form_layout.addRow("No HP:", self.cust_phone); form_layout.addRow("Alamat:", self.cust_addr)
        form_layout.addRow(btn_save); form_layout.addRow(btn_del); form_layout.addRow(btn_reset)
        form_group.setLayout(form_layout); layout.addWidget(form_group, 1)
        self.table_cust = QTableWidget(); self.table_cust.setColumnCount(4); self.table_cust.setHorizontalHeaderLabels(["ID", "Nama", "HP", "Alamat"])
        self.table_cust.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch); self.table_cust.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_cust.cellClicked.connect(self.on_cust_table_click); layout.addWidget(self.table_cust, 2)
        self.tab_cust.setLayout(layout)

    def load_customers_list(self):
        conn = self.get_db(); rows = conn.execute("SELECT * FROM customers ORDER BY id DESC").fetchall(); conn.close()
        self.table_cust.setRowCount(0)
        for r, row in enumerate(rows):
            self.table_cust.insertRow(r)
            for c, val in enumerate(row): self.table_cust.setItem(r, c, QTableWidgetItem(str(val)))

    def save_customer(self):
        name, phone, addr, cid = self.cust_name.text(), self.cust_phone.text(), self.cust_addr.text(), self.cust_id.text()
        if not name: return QMessageBox.warning(self, "Warning", "Nama wajib diisi!")
        conn = self.get_db()
        try:
            if not cid: conn.execute("INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)", (name, phone, addr))
            else: conn.execute("UPDATE customers SET name=?, phone=?, address=? WHERE id=?", (name, phone, addr, cid))
            conn.commit(); self.load_customers_list(); self.clear_cust_form(); self.load_combos(); QMessageBox.information(self, "Info", "Berhasil Disimpan")
        except Exception as e: QMessageBox.critical(self, "Error", str(e))
        finally: conn.close()

    def delete_customer(self):
        cid = self.cust_id.text()
        if not cid: return
        conn = self.get_db()
        if conn.execute("SELECT count(*) FROM transactions WHERE customer_id=?", (cid,)).fetchone()[0] > 0:
            conn.close(); return QMessageBox.warning(self, "Gagal", "Pelanggan punya transaksi!")
        if QMessageBox.question(self, "Hapus", "Yakin hapus?") == QMessageBox.StandardButton.Yes:
            conn.execute("DELETE FROM customers WHERE id=?", (cid,)); conn.commit(); self.load_customers_list(); self.clear_cust_form(); self.load_combos()
        conn.close()

    def on_cust_table_click(self, row, col):
        self.cust_id.setText(self.table_cust.item(row, 0).text()); self.cust_name.setText(self.table_cust.item(row, 1).text())
        self.cust_phone.setText(self.table_cust.item(row, 2).text()); self.cust_addr.setText(self.table_cust.item(row, 3).text())
    def clear_cust_form(self): self.cust_id.clear(); self.cust_name.clear(); self.cust_phone.clear(); self.cust_addr.clear()

    def setup_tab_trans_list(self):
        layout = QVBoxLayout(); f_layout = QHBoxLayout()
        self.filter_name = QLineEdit(); self.filter_name.setPlaceholderText("Cari Nama..."); self.filter_name.textChanged.connect(self.load_transactions)
        self.filter_status = QComboBox(); self.filter_status.addItems(["Semua Status", "Proses", "Selesai", "Diambil"]); self.filter_status.currentTextChanged.connect(self.load_transactions)
        f_layout.addWidget(QLabel("Nama:")); f_layout.addWidget(self.filter_name); f_layout.addWidget(QLabel("Status:")); f_layout.addWidget(self.filter_status); layout.addLayout(f_layout)
        self.table_trans = QTableWidget(); self.table_trans.setColumnCount(8); self.table_trans.setHorizontalHeaderLabels(["ID", "Pelanggan", "Paket", "Berat", "Pcs", "Total", "Selesai", "Status"])
        self.table_trans.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch); self.table_trans.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_trans.cellDoubleClicked.connect(self.on_trans_double_click); layout.addWidget(self.table_trans)
        btn = QPushButton("Buat Transaksi Baru")
        btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px; font-size: 11pt; font-weight: bold;")
        btn.clicked.connect(self.prepare_add_new); layout.addWidget(btn); self.tab_trans_list.setLayout(layout)

    def setup_tab_trans_form(self):
        layout = QVBoxLayout(); form = QFormLayout()
        self.inp_id = QLineEdit(); self.inp_id.setReadOnly(True)
        self.inp_customer = QComboBox(); self.inp_package = QComboBox(); self.inp_package.currentIndexChanged.connect(self.calculate_prediction)
        self.inp_weight = QLineEdit("0"); self.inp_weight.textChanged.connect(self.calculate_prediction)
        self.inp_items = QLineEdit("0"); self.inp_discount = QLineEdit("0"); self.inp_discount.textChanged.connect(self.calculate_prediction)
        self.lbl_total = QLabel("Rp 0")
        self.lbl_total.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 16pt; background-color: #E8F5E9; padding: 10px; border: 2px solid #4CAF50; border-radius: 5px;")
        self.inp_date_start = QDateEdit(QDate.currentDate()); self.inp_date_end = QLineEdit(); self.inp_date_end.setReadOnly(True)
        self.inp_status = QComboBox(); self.inp_status.addItems(["Proses", "Selesai", "Diambil"])
        form.addRow("ID:", self.inp_id); form.addRow("Pelanggan:", self.inp_customer); form.addRow("Paket:", self.inp_package)
        form.addRow("Berat:", self.inp_weight); form.addRow("Items:", self.inp_items); form.addRow("Diskon:", self.inp_discount)
        form.addRow("Selesai:", self.inp_date_end); form.addRow("Status:", self.inp_status); form.addRow("TOTAL:", self.lbl_total)
        layout.addLayout(form)
        
        nav = QHBoxLayout()
        self.btn_prev = QPushButton("<< Prev")
        self.btn_prev.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; font-size: 10pt;")
        self.btn_prev.clicked.connect(self.nav_prev)
        self.btn_next = QPushButton("Next >>")
        self.btn_next.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; font-size: 10pt;")
        self.btn_next.clicked.connect(self.nav_next)
        nav.addWidget(self.btn_prev); nav.addWidget(self.btn_next); layout.addLayout(nav)

        act = QHBoxLayout()
        self.btn_save = QPushButton("SIMPAN")
        self.btn_save.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px; font-size: 11pt; font-weight: bold;")
        self.btn_save.clicked.connect(self.save_transaction)
        self.btn_del = QPushButton("HAPUS")
        self.btn_del.setStyleSheet("background-color: #f44336; color: white; padding: 12px; font-size: 11pt; font-weight: bold;")
        self.btn_del.clicked.connect(self.delete_transaction)
        act.addWidget(self.btn_save); act.addWidget(self.btn_del); layout.addLayout(act)
        self.tab_trans_form.setLayout(layout)

    def on_tab_changed(self, index):
        if index in [0, 1]: self.load_combos(); self.load_transactions()

    def load_combos(self):
        conn = self.get_db(); cid = self.inp_customer.currentData(); self.inp_customer.clear()
        for r in conn.execute("SELECT id, name FROM customers").fetchall(): self.inp_customer.addItem(r[1], r[0])
        if cid: idx = self.inp_customer.findData(cid); self.inp_customer.setCurrentIndex(idx if idx >=0 else 0)
        if self.inp_package.count() == 0:
            for r in conn.execute("SELECT id, name, price_per_kg, duration_days FROM packages").fetchall():
                self.inp_package.addItem(f"{r[1]} - Rp {r[2]}/kg", {'price': r[2], 'days': r[3], 'id': r[0]})
        conn.close()

    def load_transactions(self):
        nf, sf = self.filter_name.text(), self.filter_status.currentText()
        q = "SELECT t.id, c.name, p.name, t.weight, t.items_count, t.total_price, t.end_date, t.status FROM transactions t LEFT JOIN customers c ON t.customer_id=c.id LEFT JOIN packages p ON t.package_id=p.id WHERE c.name LIKE ?"
        p = [f"%{nf}%"]; 
        if sf != "Semua Status": q += " AND t.status = ?"; p.append(sf)
        q += " ORDER BY t.id DESC"
        conn = self.get_db(); rows = conn.execute(q, p).fetchall(); conn.close()
        self.table_trans.setRowCount(0); self.current_record_ids = []
        for r, row in enumerate(rows):
            self.table_trans.insertRow(r); self.current_record_ids.append(row[0])
            for c, d in enumerate(row): 
                it = QTableWidgetItem(str(d))
                if c==7 and d=="Selesai": 
                    it.setBackground(QColor(200, 255, 200))
                    it.setForeground(QColor(0, 100, 0))
                self.table_trans.setItem(r, c, it)

    def calculate_prediction(self):
        pd = self.inp_package.currentData()
        if not pd: return
        try: w, d = float(self.inp_weight.text() or 0), int(self.inp_discount.text() or 0)
        except: w, d = 0, 0
        self.lbl_total.setText(f"Rp {int((w*pd['price'])-d):,}")
        self.inp_date_end.setText((self.inp_date_start.date().toPyDate() + timedelta(days=pd['days'])).strftime("%Y-%m-%d"))

    def save_transaction(self):
        try:
            cid, pd = self.inp_customer.currentData(), self.inp_package.currentData()
            if not cid: return QMessageBox.warning(self, "Err", "Pilih Pelanggan!")
            w, i, dis, tot = float(self.inp_weight.text()), int(self.inp_items.text()), int(self.inp_discount.text()), int(self.lbl_total.text().replace("Rp ", "").replace(",", ""))
            s_date, e_date, stat, tid = self.inp_date_start.date().toString("yyyy-MM-dd"), self.inp_date_end.text(), self.inp_status.currentText(), self.inp_id.text()
            conn = self.get_db()
            if not tid: conn.execute("INSERT INTO transactions (customer_id, package_id, weight, items_count, discount, total_price, start_date, end_date, status) VALUES (?,?,?,?,?,?,?,?,?)", (cid, pd['id'], w, i, dis, tot, s_date, e_date, stat))
            else: conn.execute("UPDATE transactions SET customer_id=?, package_id=?, weight=?, items_count=?, discount=?, total_price=?, start_date=?, end_date=?, status=? WHERE id=?", (cid, pd['id'], w, i, dis, tot, s_date, e_date, stat, tid))
            conn.commit(); conn.close(); self.load_transactions(); self.tabs.setCurrentIndex(0); QMessageBox.information(self, "Ok", "Tersimpan")
        except Exception as e: QMessageBox.critical(self, "Err", str(e))

    def delete_transaction(self):
        tid = self.inp_id.text()
        if tid and QMessageBox.question(self, "Hapus", "Hapus?") == QMessageBox.StandardButton.Yes:
            c = self.get_db(); c.execute("DELETE FROM transactions WHERE id=?", (tid,)); c.commit(); c.close()
            self.load_transactions(); self.prepare_add_new(); self.tabs.setCurrentIndex(0)

    def prepare_add_new(self):
        self.inp_id.clear(); self.inp_weight.setText("0"); self.inp_items.setText("0"); self.inp_discount.setText("0")
        self.inp_status.setCurrentIndex(0); self.tabs.setCurrentIndex(1)
        self.current_nav_index = -1 # Reset navigasi

    def on_trans_double_click(self, row, col):
        self.current_nav_index = row
        self.load_record_to_form(self.table_trans.item(row, 0).text())

    def load_record_to_form(self, tid):
        conn = self.get_db(); data = conn.execute("SELECT * FROM transactions WHERE id=?", (tid,)).fetchone(); conn.close()
        if data:
            self.inp_id.setText(str(data[0]))
            idx = self.inp_customer.findData(data[1]); self.inp_customer.setCurrentIndex(idx if idx>=0 else 0)
            for i in range(self.inp_package.count()):
                if self.inp_package.itemData(i)['id'] == data[2]: self.inp_package.setCurrentIndex(i); break
            self.inp_weight.setText(str(data[3])); self.inp_items.setText(str(data[4])); self.inp_discount.setText(str(data[5]))
            self.lbl_total.setText(f"Rp {data[6]:,}"); self.inp_date_start.setDate(QDate.fromString(data[7], "yyyy-MM-dd"))
            self.inp_date_end.setText(data[8]); self.inp_status.setCurrentText(data[9]); self.tabs.setCurrentIndex(1)

    # --- PERBAIKAN LOGIKA NAVIGASI ---
    def nav_prev(self):
        if self.current_nav_index > 0:
            self.current_nav_index -= 1
            self.load_record_to_form(self.current_record_ids[self.current_nav_index])
        else:
            QMessageBox.information(self, "Info", "Ini adalah data paling awal.")

    def nav_next(self):
        # Jika posisi belum ada (baru buka), otomatis ke data paling atas (terbaru)
        if self.current_nav_index == -1:
            if len(self.current_record_ids) > 0:
                self.current_nav_index = 0
                self.load_record_to_form(self.current_record_ids[0])
            else:
                QMessageBox.information(self, "Info", "Belum ada data transaksi.")
            return

        if self.current_nav_index < len(self.current_record_ids) - 1:
            self.current_nav_index += 1
            self.load_record_to_form(self.current_record_ids[self.current_nav_index])
        else:
            QMessageBox.information(self, "Info", "Ini adalah data paling akhir.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LaundryApp()
    window.show()
    sys.exit(app.exec())