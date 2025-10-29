import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Sampath Food City - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.setup_login_gui()

    def setup_login_gui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Sampath Food City Login", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(main_frame, text="Login", command=self.authenticate).grid(row=3, column=0, columnspan=2, pady=20)
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, foreground="red").grid(row=4, column=0, columnspan=2)
        self.root.bind("<Return>", lambda event: self.authenticate())

    def authenticate(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        valid_credentials = {"admin": "admin123", "user": "user123"}

        if username in valid_credentials and valid_credentials[username] == password:
            self.status_var.set("Login successful!")
            self.root.after(500, self.launch_main_app)
        else:
            self.status_var.set("Invalid username or password")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def launch_main_app(self):
        self.root.destroy()
        main_root = tk.Tk()
        app = SalesDataAnalysisSystem(main_root)
        main_root.mainloop()


class SalesDataAnalysisSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sampath Food City - Sales Data Analysis System")
        self.root.geometry("1200x800")
        self.sales_data = []
        self.branch_data = {}
        self.product_data = {}
        self.weekly_sales = defaultdict(float)
        self.monthly_sales = defaultdict(float)
        self.selected_branch_var = tk.StringVar(value="All Branches")
        self.valid_branches = ["Colombo", "Galle", "Matara"]
        self.setup_gui()
        self.load_data()

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        ttk.Label(main_frame, text="Sampath Food City - Sales Data Analysis System", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        control_frame = ttk.LabelFrame(main_frame, text="Analysis Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        file_frame = ttk.LabelFrame(control_frame, text="File Operations", padding="5")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(file_frame, text="Load Data File", command=self.load_data_file).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="Save Analysis Report", command=self.save_report).pack(fill=tk.X, pady=2)

        analysis_frame = ttk.LabelFrame(control_frame, text="Analysis Options", padding="5")
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(analysis_frame, text="Monthly Sales by Branch", command=self.monthly_branch_analysis).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Product Price Analysis", command=self.price_analysis).pack(fill=tk.X, pady=2)

        weekly_frame = ttk.Frame(analysis_frame)
        weekly_frame.pack(fill=tk.X, pady=2)
        ttk.Label(weekly_frame, text="Select Branch for Weekly Analysis:").pack(side=tk.LEFT)
        self.branch_combo = ttk.Combobox(weekly_frame, textvariable=self.selected_branch_var, values=["All Branches"] + sorted(self.valid_branches), state="readonly")
        self.branch_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(weekly_frame, text="Weekly Sales Analysis", command=self.weekly_sales_analysis).pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(analysis_frame, text="Product Preference Analysis", command=self.product_preference_analysis).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Sales Distribution Analysis", command=self.sales_distribution_analysis).pack(fill=tk.X, pady=2)

        summary_frame = ttk.LabelFrame(control_frame, text="Data Summary", padding="5")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        self.summary_text = tk.Text(summary_frame, height=8, width=30)
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        self.result_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        self.result_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.notebook = ttk.Notebook(self.result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.chart_frame, text="Charts")

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def load_data(self):
        try:
            df = pd.read_csv("transactions_data.csv")
            df = df[df['branch'].isin(self.valid_branches)]
            self.sales_data = df.to_dict('records')
            self.organize_data()
            self.update_summary()
            self.branch_combo['values'] = ["All Branches"] + sorted(self.branch_data.keys())
            self.status_var.set(f"Data loaded successfully. {len(self.sales_data)} records loaded.")
        except FileNotFoundError:
            messagebox.showerror("Error", "transactions_data.csv file not found!")
            self.create_sample_data()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")

    def create_sample_data(self):
        sample_data = []
        products = [
            {"name": "Rice", "category": "Grains", "base_price": 150},
            {"name": "Bread", "category": "Bakery", "base_price": 85},
            {"name": "Milk", "category": "Dairy", "base_price": 280},
            {"name": "Chicken", "category": "Meat", "base_price": 650},
            {"name": "Fish", "category": "Seafood", "base_price": 800},
            {"name": "Vegetables", "category": "Produce", "base_price": 120},
            {"name": "Fruits", "category": "Produce", "base_price": 200},
            {"name": "Soap", "category": "Personal Care", "base_price": 95},
            {"name": "Toothpaste", "category": "Personal Care", "base_price": 180},
            {"name": "Shampoo", "category": "Personal Care", "base_price": 320}
        ]
        
        start_date = datetime(2025, 7, 1)
        end_date = datetime(2025, 7, 31)
        
        for day in range((end_date - start_date).days + 1):
            current_date = start_date + timedelta(days=day)
            for branch in self.valid_branches:
                daily_transactions = np.random.randint(5, 20)
                for _ in range(daily_transactions):
                    product = np.random.choice(products)
                    quantity = np.random.randint(1, 10)
                    price_variation = np.random.uniform(0.9, 1.1)
                    unit_price = product["base_price"] * price_variation
                    total_amount = quantity * unit_price
                    sample_data.append({
                        "transaction_id": f"TXN{len(sample_data)+1:06d}",
                        "date": current_date.strftime("%Y-%m-%d"),
                        "branch": branch,
                        "product_name": product["name"],
                        "category": product["category"],
                        "quantity": quantity,
                        "unit_price": round(unit_price, 2),
                        "total_amount": round(total_amount, 2),
                        "customer_id": f"CUST{np.random.randint(1000, 9999)}"
                    })
        
        df = pd.DataFrame(sample_data)
        df.to_csv("transactions_data.csv", index=False)

    def organize_data(self):
        self.branch_data.clear()
        self.product_data.clear()
        self.weekly_sales.clear()
        self.monthly_sales.clear()
        
        for record in self.sales_data:
            date_obj = datetime.strptime(record['date'], '%Y-%m-%d')
            branch = record['branch']
            product = record['product_name']
            amount = float(record['total_amount'])
            
            if branch not in self.branch_data:
                self.branch_data[branch] = {'total_sales': 0, 'monthly_sales': defaultdict(float), 'weekly_sales': defaultdict(float), 'products': defaultdict(int)}
            
            self.branch_data[branch]['total_sales'] += amount
            month_key = date_obj.strftime('%Y-%m')
            week_key = date_obj.strftime('%Y-W%U')
            self.branch_data[branch]['monthly_sales'][month_key] += amount
            self.branch_data[branch]['weekly_sales'][week_key] += amount
            self.branch_data[branch]['products'][product] += int(record['quantity'])
            
            if product not in self.product_data:
                self.product_data[product] = {'total_sales': 0, 'total_quantity': 0, 'prices': []}
            
            self.product_data[product]['total_sales'] += amount
            self.product_data[product]['total_quantity'] += int(record['quantity'])
            self.product_data[product]['prices'].append(float(record['unit_price']))
            
            self.weekly_sales[week_key] += amount
            self.monthly_sales[month_key] += amount

    def update_summary(self):
        self.summary_text.delete(1.0, tk.END)
        summary = f"""DATA SUMMARY
=============
Total Records: {len(self.sales_data)}
Total Branches: {len(self.branch_data)}
Total Products: {len(self.product_data)}

Top 3 Branches by Sales:
"""
        sorted_branches = sorted(self.branch_data.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        for i, (branch, data) in enumerate(sorted_branches[:3]):
            summary += f"{i+1}. {branch}: Rs. {data['total_sales']:,.2f}\n"
        
        summary += f"\nTop 3 Products by Sales:\n"
        sorted_products = sorted(self.product_data.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        for i, (product, data) in enumerate(sorted_products[:3]):
            summary += f"{i+1}. {product}: Rs. {data['total_sales']:,.2f}\n"
        
        dates = [datetime.strptime(record['date'], '%Y-%m-%d') for record in self.sales_data]
        min_date = min(dates).strftime('%Y-%m-%d') if dates else "N/A"
        max_date = max(dates).strftime('%Y-%m-%d') if dates else "N/A"
        
        summary += f"\nDate Range:\n{min_date} to {max_date}"
        self.summary_text.insert(1.0, summary)

    def monthly_branch_analysis(self):
        if not self.sales_data:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        self.create_monthly_branch_chart()
        self.status_var.set("Monthly branch analysis completed.")

    def create_monthly_branch_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        months = sorted(list(self.monthly_sales.keys()))
        branches = list(self.branch_data.keys())
        data_matrix = [[self.branch_data[branch]['monthly_sales'][month] for month in months] for branch in branches]
        
        x = np.arange(len(months))
        width = 0.15
        
        for i, (branch, data) in enumerate(zip(branches, data_matrix)):
            ax.bar(x + i * width, data, width, label=branch)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Sales Amount (Rs.)')
        ax.set_title('Monthly Sales by Branch')
        ax.set_xticks(x + width * (len(branches) - 1) / 2)
        ax.set_xticklabels(months, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rs. {x/1000:.0f}K'))
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def price_analysis(self):
        if not self.sales_data:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        self.create_price_analysis_chart()
        self.status_var.set("Product price analysis completed.")

    def create_price_analysis_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        products = list(self.product_data.keys())
        avg_prices = [np.mean(self.product_data[p]['prices']) for p in products]
        price_ranges = [np.max(self.product_data[p]['prices']) - np.min(self.product_data[p]['prices']) for p in products]
        
        ax1.bar(products, avg_prices, color='skyblue', alpha=0.7)
        ax1.set_title('Average Product Prices')
        ax1.set_ylabel('Average Price (Rs.)')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        ax2.bar(products, price_ranges, color='lightcoral', alpha=0.7)
        ax2.set_title('Product Price Ranges')
        ax2.set_ylabel('Price Range (Rs.)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def weekly_sales_analysis(self):
        if not self.sales_data:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        selected_branch = self.selected_branch_var.get()
        self.create_weekly_chart(self.weekly_sales if selected_branch == "All Branches" else self.branch_data[selected_branch]['weekly_sales'],
                                  "Weekly Sales Trend (All Branches)" if selected_branch == "All Branches" else f"Weekly Sales Trend ({selected_branch})")
        self.status_var.set(f"Weekly sales analysis for {selected_branch} completed.")

    def create_weekly_chart(self, weekly_data, title):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        weeks = sorted(list(weekly_data.keys()))
        sales = [weekly_data[week] for week in weeks]
        
        ax.plot(weeks, sales, marker='o', linewidth=2, markersize=6)
        ax.set_title(title)
        ax.set_xlabel('Week')
        ax.set_ylabel('Sales Amount (Rs.)')
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rs. {x/1000:.0f}K'))
        plt.xticks(rotation=45)
        
        if weeks and sales:
            x_numeric = range(len(weeks))
            z = np.polyfit(x_numeric, sales, 1)
            p = np.poly1d(z)
            ax.plot(weeks, p(x_numeric), "--", alpha=0.7, color='red', label='Trend')
            ax.legend()
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def product_preference_analysis(self):
        if not self.sales_data:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        self.create_preference_chart(Counter({record['product_name']: int(record['quantity']) for record in self.sales_data}).most_common(),
                                      defaultdict(float, {record['category']: float(record['total_amount']) for record in self.sales_data}))
        self.status_var.set("Product preference analysis completed.")

    def create_preference_chart(self, top_products, category_sales):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        products = [item[0] for item in top_products]
        quantities = [item[1] for item in top_products]
        
        ax1.barh(products, quantities)
        ax1.barh(products, quantities, color='lightgreen', alpha=0.7)
        ax1.set_title('Top Products by Quantity Sold')
        ax1.set_xlabel('Quantity Sold')
        ax1.grid(True, alpha=0.3)

        categories = list(category_sales.keys())
        sales_values = list(category_sales.values())

        ax2.pie(sales_values, labels=categories, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Sales Distribution by Category')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def sales_distribution_analysis(self):
        if not self.sales_data:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        transaction_amounts = [float(record['total_amount']) for record in self.sales_data]
        self.create_distribution_chart(transaction_amounts)
        self.status_var.set("Sales distribution analysis completed.")

    def create_distribution_chart(self, transaction_amounts):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        ax1.hist(transaction_amounts, bins=10, alpha=0.7, edgecolor='black')
        ax1.set_title('Distribution of Transaction Amounts')
        ax1.set_xlabel('Transaction Amount (Rs.)')
        ax1.set_ylabel('Frequency')
        ax1.grid(True, alpha=0.3)

        ranges = [
            (0, 100, "Rs. 0-100"),
            (100, 500, "Rs. 100-500"),
            (500, 1000, "Rs. 500-1,000"),
            (1000, 2000, "Rs. 1,000-2,000"),
            (2000, 5000, "Rs. 2,000-5,000"),
            (5000, 10000, "Rs. 5,000-10,000"),
            (10000, float('inf'), "Rs. 10,000+")
        ]
        
        range_labels = [r[2] for r in ranges]
        range_counts = [sum(1 for amount in transaction_amounts if min_val <= amount < max_val) for min_val, max_val, _ in ranges]

        ax2.bar(range_labels, range_counts, alpha=0.7)
        ax2.set_title('Transaction Count by Amount Range')
        ax2.set_xlabel('Amount Range')
        ax2.set_ylabel('Number of Transactions')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_data_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Sales Data File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                df = pd.read_csv(file_path)
                required_columns = ['date', 'branch', 'product_name', 'category', 'quantity', 'unit_price', 'total_amount']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    messagebox.showerror("Error", f"Missing required columns: {missing_columns}")
                    return
                
                df = df[df['branch'].isin(self.valid_branches)]
                self.sales_data = df.to_dict('records')
                self.organize_data()
                self.update_summary()
                self.branch_combo['values'] = ["All Branches"] + sorted(self.branch_data.keys())
                self.status_var.set(f"Data loaded from {file_path}. {len(self.sales_data)} records loaded.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {str(e)}")

    def save_report(self):
        if not self.sales_data:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Analysis Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("SAMPATH FOOD CITY - SALES DATA ANALYSIS REPORT\n")
                    f.write("=" * 60 + "\n")
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    f.write("SUMMARY\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"Total Records: {len(self.sales_data)}\n")
                    f.write(f"Total Branches: {len(self.branch_data)}\n")
                    f.write(f"Total Products: {len(self.product_data)}\n")
                    f.write(f"Total Sales: Rs. {sum(record['total_amount'] for record in self.sales_data):,.2f}\n\n")
                    
                    sorted_branches = sorted(self.branch_data.items(), key=lambda x: x[1]['total_sales'], reverse=True)
                    f.write("BRANCH PERFORMANCE\n")
                    f.write("-" * 20 + "\n")
                    for branch, data in sorted_branches:
                        f.write(f"{branch}: Rs. {data['total_sales']:,.2f}\n")
                    
                    f.write("\nTOP PRODUCTS BY SALES\n")
                    f.write("-" * 20 + "\n")
                    sorted_products = sorted(self.product_data.items(), key=lambda x: x[1]['total_sales'], reverse=True)
                    for product, data in sorted_products:
                        f.write(f"{product}: Rs. {data['total_sales']:,.2f}\n")
                    
                    f.write("\nMONTHLY SALES TRENDS\n")
                    f.write("-" * 20 + "\n")
                    sorted_months = sorted(self.monthly_sales.items())
                    for month, sales in sorted_months:
                        f.write(f"{month}: Rs. {sales:,.2f}\n")
                
                messagebox.showinfo("Successful", f"Report saved to {file_path}")
                self.status_var.set(f"Report saved to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error saving report: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()