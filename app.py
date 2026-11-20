from datetime import date, timedelta
from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent / "laundry_uas_final.db"
STATUSES = ["Proses", "Selesai", "Diambil"]

st.set_page_config(
    page_title="LaundryDesk",
    page_icon="LD",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price_per_kg INTEGER NOT NULL,
                duration_days INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                package_id INTEGER,
                weight REAL,
                items_count INTEGER,
                discount INTEGER,
                total_price INTEGER,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                FOREIGN KEY(customer_id) REFERENCES customers(id),
                FOREIGN KEY(package_id) REFERENCES packages(id)
            )
        """)

        package_count = conn.execute(
            "SELECT COUNT(*) FROM packages"
        ).fetchone()[0]

        if package_count == 0:
            packages = [
                ("Cuci Komplit Reguler", 6000, 3),
                ("Cuci Komplit Express", 10000, 1),
                ("Setrika Komplit", 8000, 2),
                ("Cuci Kering Express", 12000, 1),
                ("Paket Hemat Bundle", 5000, 4),
            ]
            customers = [
                ("Reno Santoso", "08123456789", "Jl. Merdeka No. 1"),
                ("Hisam Widodo", "08223344556", "Jl. Proklamasi No. 17"),
                ("Siti Aminah", "08334455667", "Jl. Kebangsaan No. 8"),
                ("Ahmad Yani", "08445566778", "Jl. Pahlawan No. 4"),
                ("Dewi Sartika", "08556677889", "Jl. Cinta No. 10"),
            ]
            conn.executemany(
                "INSERT INTO packages (name, price_per_kg, duration_days) VALUES (?, ?, ?)",
                packages,
            )
            conn.executemany(
                "INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)",
                customers,
            )
            transactions = [
                (1, 1, 2.5, 10, 5000, 15000, "2023-10-01", "2023-10-04", "Selesai"),
                (2, 2, 3.0, 15, 10000, 30000, "2023-10-02", "2023-10-03", "Selesai"),
                (3, 1, 1.0, 5, 0, 6000, "2023-10-03", "2023-10-06", "Proses"),
                (4, 2, 4.0, 20, 20000, 80000, "2023-10-04", "2023-10-05", "Diambil"),
                (5, 3, 2.0, 8, 3000, 13000, "2023-10-05", "2023-10-07", "Selesai"),
            ]
            conn.executemany(
                """INSERT INTO transactions
                (customer_id, package_id, weight, items_count, discount,
                 total_price, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                transactions,
            )


def read_df(query, params=()):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def read_one(query, params=()):
    with get_connection() as conn:
        return conn.execute(query, params).fetchone()


def execute(query, params=()):
    with get_connection() as conn:
        conn.execute(query, params)
        conn.commit()


def rupiah(value):
    return f"Rp {int(value or 0):,}".replace(",", ".")


def get_customers():
    return read_df("SELECT id, name, phone, address FROM customers ORDER BY name")


def get_packages():
    return read_df(
        "SELECT id, name, price_per_kg, duration_days FROM packages ORDER BY name"
    )


def get_transactions(name_filter="", status_filter="Semua Status"):
    query = """
        SELECT
            t.id AS ID,
            c.name AS Pelanggan,
            p.name AS Paket,
            t.weight AS Berat,
            t.items_count AS Pcs,
            t.total_price AS Total,
            t.end_date AS Selesai,
            t.status AS Status
        FROM transactions t
        LEFT JOIN customers c ON c.id = t.customer_id
        LEFT JOIN packages p ON p.id = t.package_id
        WHERE c.name LIKE ?
    """
    params = [f"%{name_filter}%"]
    if status_filter != "Semua Status":
        query += " AND t.status = ?"
        params.append(status_filter)
    query += " ORDER BY t.id DESC"
    return read_df(query, params)


def calculate_total(weight, price_per_kg, discount):
    return max(0, int(round(weight * price_per_kg)) - int(discount))


def transaction_form(default=None, form_key="transaction_form"):
    customers = get_customers()
    packages = get_packages()

    if customers.empty:
        st.warning("Tambahkan pelanggan terlebih dahulu sebelum membuat transaksi.")
        return None
    if packages.empty:
        st.warning("Belum ada paket laundry di database.")
        return None

    default = default or {}
    customer_ids = customers["id"].astype(int).tolist()
    package_ids = packages["id"].astype(int).tolist()

    customer_default = default.get("customer_id")
    package_default = default.get("package_id")
    customer_index = customer_ids.index(customer_default) if customer_default in customer_ids else 0
    package_index = package_ids.index(package_default) if package_default in package_ids else 0

    with st.form(form_key):
        customer_labels = {
            int(row.id): f"{row.name} · {row.phone}"
            for row in customers.itertuples()
        }
        package_labels = {
            int(row.id): f"{row.name} · {rupiah(row.price_per_kg)}/kg · {row.duration_days} hari"
            for row in packages.itertuples()
        }

        c1, c2 = st.columns(2)
        with c1:
            customer_id = st.selectbox(
                "Pelanggan",
                customer_ids,
                index=customer_index,
                format_func=lambda x: customer_labels[x],
            )
            package_id = st.selectbox(
                "Paket laundry",
                package_ids,
                index=package_index,
                format_func=lambda x: package_labels[x],
            )
            weight = st.number_input(
                "Berat (kg)",
                min_value=0.1,
                max_value=500.0,
                value=max(0.1, float(default.get("weight") or 1.0)),
                step=0.1,
            )
            items_count = st.number_input(
                "Jumlah item (pcs)",
                min_value=0,
                max_value=10000,
                value=max(0, int(default.get("items_count") or 0)),
                step=1,
            )
        with c2:
            discount = st.number_input(
                "Diskon (Rp)",
                min_value=0,
                max_value=100000000,
                value=max(0, int(default.get("discount") or 0)),
                step=1000,
            )
            start_date = st.date_input(
                "Tanggal masuk",
                value=date.fromisoformat(default["start_date"])
                if default.get("start_date")
                else date.today(),
            )
            status = st.selectbox(
                "Status",
                STATUSES,
                index=STATUSES.index(default.get("status"))
                if default.get("status") in STATUSES
                else 0,
            )

        selected_package = packages.loc[packages["id"] == package_id].iloc[0]
        total = calculate_total(weight, selected_package["price_per_kg"], discount)
        end_date = start_date + timedelta(days=int(selected_package["duration_days"]))

        st.info(
            f"Estimasi selesai: **{end_date:%d %B %Y}**  \n"
            f"Total transaksi: **{rupiah(total)}**"
        )
        submitted = st.form_submit_button("Simpan transaksi", type="primary", use_container_width=True)

    if submitted:
        return {
            "customer_id": customer_id,
            "package_id": package_id,
            "weight": weight,
            "items_count": items_count,
            "discount": discount,
            "total_price": total,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "status": status,
        }
    return None


def page_dashboard():
    st.title("LaundryDesk")
    st.caption("Laundry management, made straightforward.")

    totals = read_one("""
        SELECT
            COUNT(*) AS transactions,
            COALESCE(SUM(total_price), 0) AS revenue,
            SUM(CASE WHEN status = 'Proses' THEN 1 ELSE 0 END) AS in_progress,
            SUM(CASE WHEN status = 'Selesai' THEN 1 ELSE 0 END) AS completed
        FROM transactions
    """)
    customer_total = read_one("SELECT COUNT(*) AS total FROM customers")["total"]

    cols = st.columns(4)
    cols[0].metric("Total transaksi", totals["transactions"])
    cols[1].metric("Total nilai transaksi", rupiah(totals["revenue"]))
    cols[2].metric("Sedang diproses", totals["in_progress"] or 0)
    cols[3].metric("Pelanggan", customer_total)

    st.subheader("Transaksi terbaru")
    recent = get_transactions()
    if recent.empty:
        st.info("Belum ada transaksi.")
    else:
        st.dataframe(recent.head(10), use_container_width=True, hide_index=True)


def page_transactions():
    st.title("Transactions")
    st.caption("View, filter, create, and update laundry transactions.")

    with st.expander("Filter transaksi", expanded=True):
        c1, c2 = st.columns(2)
        name_filter = c1.text_input("Cari nama pelanggan")
        status_filter = c2.selectbox(
            "Status transaksi", ["Semua Status"] + STATUSES
        )

    transactions = get_transactions(name_filter, status_filter)
    st.dataframe(transactions, use_container_width=True, hide_index=True)

    st.divider()
    create_tab, edit_tab, delete_tab = st.tabs(
        ["Tambah transaksi", "Edit transaksi", "Hapus transaksi"]
    )

    with create_tab:
        st.subheader("Transaksi baru")
        new_data = transaction_form(form_key="create_transaction")
        if new_data:
            execute(
                """INSERT INTO transactions
                (customer_id, package_id, weight, items_count, discount,
                 total_price, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                tuple(new_data.values()),
            )
            st.success("Transaksi berhasil ditambahkan.")
            st.rerun()

    with edit_tab:
        st.subheader("Perbarui transaksi")
        ids = read_df("SELECT id FROM transactions ORDER BY id DESC")["id"].tolist()
        if not ids:
            st.info("Belum ada transaksi untuk diedit.")
        else:
            selected_id = st.selectbox("Pilih ID transaksi", ids, key="edit_transaction_id")
            record = read_one(
                "SELECT * FROM transactions WHERE id = ?", (selected_id,)
            )
            edit_data = transaction_form(dict(record), form_key="edit_transaction")
            if edit_data:
                execute(
                    """UPDATE transactions SET
                    customer_id=?, package_id=?, weight=?, items_count=?,
                    discount=?, total_price=?, start_date=?, end_date=?, status=?
                    WHERE id=?""",
                    (*edit_data.values(), selected_id),
                )
                st.success("Transaksi berhasil diperbarui.")
                st.rerun()

    with delete_tab:
        st.subheader("Hapus transaksi")
        ids = read_df("SELECT id FROM transactions ORDER BY id DESC")["id"].tolist()
        if not ids:
            st.info("Belum ada transaksi.")
        else:
            selected_id = st.selectbox("Pilih ID yang akan dihapus", ids, key="delete_transaction_id")
            confirm = st.checkbox("Saya yakin ingin menghapus transaksi ini.")
            if st.button("Hapus transaksi", type="primary", disabled=not confirm):
                execute("DELETE FROM transactions WHERE id = ?", (selected_id,))
                st.success("Transaksi berhasil dihapus.")
                st.rerun()


def page_customers():
    st.title("Customers")
    st.caption("Manage customer records.")

    customers = get_customers()
    st.dataframe(customers, use_container_width=True, hide_index=True)

    add_tab, edit_tab, delete_tab = st.tabs(
        ["Tambah pelanggan", "Edit pelanggan", "Hapus pelanggan"]
    )

    with add_tab:
        with st.form("add_customer"):
            name = st.text_input("Nama lengkap")
            phone = st.text_input("Nomor telepon")
            address = st.text_area("Alamat")
            submitted = st.form_submit_button("Simpan pelanggan", type="primary")
        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Nama dan nomor telepon wajib diisi.")
            else:
                execute(
                    "INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)",
                    (name.strip(), phone.strip(), address.strip()),
                )
                st.success("Pelanggan berhasil ditambahkan.")
                st.rerun()

    with edit_tab:
        if customers.empty:
            st.info("Belum ada data pelanggan.")
        else:
            customer_ids = customers["id"].astype(int).tolist()
            selected_id = st.selectbox("Pilih pelanggan", customer_ids, key="edit_customer_id")
            record = read_one("SELECT * FROM customers WHERE id = ?", (selected_id,))
            with st.form("edit_customer"):
                name = st.text_input("Nama lengkap", value=record["name"])
                phone = st.text_input("Nomor telepon", value=record["phone"])
                address = st.text_area("Alamat", value=record["address"] or "")
                submitted = st.form_submit_button("Perbarui pelanggan", type="primary")
            if submitted:
                if not name.strip() or not phone.strip():
                    st.error("Nama dan nomor telepon wajib diisi.")
                else:
                    execute(
                        "UPDATE customers SET name=?, phone=?, address=? WHERE id=?",
                        (name.strip(), phone.strip(), address.strip(), selected_id),
                    )
                    st.success("Data pelanggan berhasil diperbarui.")
                    st.rerun()

    with delete_tab:
        if customers.empty:
            st.info("Belum ada data pelanggan.")
        else:
            customer_ids = customers["id"].astype(int).tolist()
            selected_id = st.selectbox("Pilih pelanggan yang akan dihapus", customer_ids, key="delete_customer_id")
            linked = read_one(
                "SELECT COUNT(*) AS total FROM transactions WHERE customer_id = ?",
                (selected_id,),
            )["total"]
            if linked:
                st.warning("Pelanggan ini masih memiliki transaksi dan tidak dapat dihapus.")
            else:
                confirm = st.checkbox("Saya yakin ingin menghapus pelanggan ini.")
                if st.button("Hapus pelanggan", type="primary", disabled=not confirm):
                    execute("DELETE FROM customers WHERE id = ?", (selected_id,))
                    st.success("Pelanggan berhasil dihapus.")
                    st.rerun()


def page_packages():
    st.title("Laundry Packages")
    st.caption("Available packages and service duration.")
    packages = get_packages()
    if packages.empty:
        st.info("Belum ada paket laundry.")
    else:
        display = packages.rename(
            columns={
                "id": "ID",
                "name": "Nama paket",
                "price_per_kg": "Harga per kg",
                "duration_days": "Durasi (hari)",
            }
        )
        st.dataframe(display, use_container_width=True, hide_index=True)


def main():
    init_db()

    with st.sidebar:
        st.title("LaundryDesk")
        st.caption("Laundry management system")
        page = st.radio(
            "Navigation",
            ["Dashboard", "Transactions", "Customers", "Packages"],
            label_visibility="collapsed",
        )
        st.divider()
        st.caption("Python · Streamlit · SQLite")

    if page == "Dashboard":
        page_dashboard()
    elif page == "Transactions":
        page_transactions()
    elif page == "Customers":
        page_customers()
    else:
        page_packages()


if __name__ == "__main__":
    main()
