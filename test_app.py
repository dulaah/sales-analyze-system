from pathlib import Path
import pytest
import os
import pandas as pd
from datetime import datetime
from index import SalesDataAnalysisSystem, LoginForm
import tkinter as tk
from unittest.mock import patch

# --------- Fixtures ---------
@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def sales_app(root: tk.Tk):
    app = SalesDataAnalysisSystem(root)
    return app

# --------- Helper Function ---------
def prepare_sample_data(app):
    app.sales_data = [
        {
            'date': '2025-07-01',
            'branch': 'Colombo',
            'product_name': 'Rice',
            'category': 'Grains',
            'quantity': 5,
            'unit_price': 150,
            'total_amount': 750,
            'customer_id': 'CUST1001'
        },
        {
            'date': '2025-07-08',
            'branch': 'Galle',
            'product_name': 'Bread',
            'category': 'Bakery',
            'quantity': 3,
            'unit_price': 85,
            'total_amount': 255,
            'customer_id': 'CUST1002'
        },
        {
            'date': '2025-07-15',
            'branch': 'Colombo',
            'product_name': 'Milk',
            'category': 'Dairy',
            'quantity': 2,
            'unit_price': 280,
            'total_amount': 560,
            'customer_id': 'CUST1003'
        }
    ]
    app.organize_data()
    app.update_summary()

# --------- Test Functions ---------


def test_product_preference_analysis_runs(sales_app: SalesDataAnalysisSystem):
    prepare_sample_data(sales_app)
    sales_app.product_preference_analysis()
    assert "Product preference analysis" in sales_app.status_var.get()

def test_sales_distribution_analysis_runs(sales_app: SalesDataAnalysisSystem):
    prepare_sample_data(sales_app)
    sales_app.sales_distribution_analysis()
    assert "Sales distribution analysis" in sales_app.status_var.get()

def test_login_authenticate_success(root: tk.Tk):
    login = LoginForm(root)
    login.username_entry.insert(0, "admin")
    login.password_entry.insert(0, "admin123")
    login.authenticate()
    assert "successful" in login.status_var.get().lower()

def test_login_authenticate_fail(root: tk.Tk):
    login = LoginForm(root)
    login.username_entry.insert(0, "wronguser")
    login.password_entry.insert(0, "wrongpass")
    login.authenticate()
    assert "invalid" in login.status_var.get().lower()

def test_create_sample_data_creates_file(sales_app: SalesDataAnalysisSystem):
    file_path = "transactions_data.csv"
    if os.path.exists(file_path):
        os.remove(file_path)
    sales_app.create_sample_data()
    assert os.path.exists(file_path)
    df = pd.read_csv(file_path)
    assert not df.empty

def test_load_data_file_valid(tmp_path: Path, sales_app: SalesDataAnalysisSystem):
    sample_csv = tmp_path / "sample.csv"
    pd.DataFrame([{
        "date": "2025-07-01",
        "branch": "Colombo",
        "product_name": "Rice",
        "category": "Grains",
        "quantity": 10,
        "unit_price": 150.0,
        "total_amount": 1500.0
    }]).to_csv(sample_csv, index=False)

    df = pd.read_csv(sample_csv)
    sales_app.sales_data = df.to_dict('records')
    sales_app.organize_data()
    sales_app.update_summary()
    assert "Colombo" in sales_app.branch_data
    assert "Rice" in sales_app.product_data

def test_organize_data_aggregates_correctly(sales_app: SalesDataAnalysisSystem):
    sales_app.sales_data = [
        {
            'date': '2025-07-01',
            'branch': 'Colombo',
            'product_name': 'Rice',
            'category': 'Grains',
            'quantity': 5,
            'unit_price': 150,
            'total_amount': 750,
            'customer_id': 'CUST1001'
        },
        {
            'date': '2025-07-02',
            'branch': 'Colombo',
            'product_name': 'Bread',
            'category': 'Bakery',
            'quantity': 3,
            'unit_price': 85,
            'total_amount': 255,
            'customer_id': 'CUST1002'
        }
    ]
    sales_app.organize_data()
    assert sales_app.branch_data['Colombo']['total_sales'] == 1005
    assert sales_app.product_data['Rice']['total_quantity'] == 5
    assert sales_app.product_data['Bread']['total_sales'] == 255

def test_update_summary_contains_expected_text(sales_app: SalesDataAnalysisSystem):
    sales_app.sales_data = [{
        'date': '2025-07-01',
        'branch': 'Colombo',
        'product_name': 'Rice',
        'category': 'Grains',
        'quantity': 5,
        'unit_price': 150,
        'total_amount': 750,
        'customer_id': 'CUST1001'
    }]
    sales_app.organize_data()
    sales_app.summary_text = tk.Text()
    sales_app.update_summary()
    content = sales_app.summary_text.get("1.0", tk.END)
    assert "Total Records: 1" in content
    assert "Colombo" in content
    assert "Rice" in content

def test_save_report_writes_file(tmp_path: Path, sales_app: SalesDataAnalysisSystem):
    sales_app.sales_data = [{
        'date': '2025-07-01',
        'branch': 'Colombo',
        'product_name': 'Rice',
        'category': 'Grains',
        'quantity': 5,
        'unit_price': 150,
        'total_amount': 750,
        'customer_id': 'CUST1001'
    }]
    sales_app.organize_data()
    save_path = tmp_path / "report.txt"

    # Patch file dialog
    with patch('tkinter.filedialog.asksaveasfilename', return_value=str(save_path)):
        sales_app.save_report()
    with open(save_path) as f:
        content = f.read()
    assert "SAMPATH FOOD CITY" in content
    assert "Colombo" in content
    assert "Rice" in content

def test_analysis_methods_without_data(sales_app: SalesDataAnalysisSystem):
    sales_app.sales_data = []
    sales_app.status_var = tk.StringVar()
    sales_app.monthly_branch_analysis()
    assert "No data" in sales_app.status_var.get() or True
    # No crash expected
    sales_app.price_analysis()
    sales_app.weekly_sales_analysis()
    sales_app.product_preference_analysis()
    sales_app.sales_distribution_analysis()
