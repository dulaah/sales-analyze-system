# 🛒 Sampath Food City - Sales Data Analysis System  

A desktop-based **Sales Data Analysis System** built with **Python (Tkinter GUI)**.  
This application allows users to **login securely**, **analyze sales data**, and **generate reports** with visual charts.  

---

 Features  

### 🔐 Login System  
- Secure login for **Admin** and **User** accounts.  
- Credentials:  
  - **Admin** → `admin / admin123`  
  - **User** → `user / user123`  

### 📊 Sales Data Analysis  
- **Monthly Sales by Branch** – Compare sales trends across branches.  
- **Weekly Sales Analysis** – View weekly sales trends (per branch or all branches).  
- **Product Price Analysis** – Analyze average and range of product prices.  
- **Product Preference Analysis** – Top products by quantity sold + sales by category.  
- **Sales Distribution Analysis** – Explore total sales distribution across categories.  

---

## 🛠️ Technologies Used  
- **Python 3**  
- **Tkinter** – GUI  
- **Pandas** – Data processing  
- **Matplotlib** – Graphs & charts  
- **NumPy** – Numerical analysis  

---

## 📂 Project Structure  

python_system/
│── index.py # Main application (GUI + Login + Dashboard)
│── app.py # Core sales analysis logic
│── test_app.py # Unit tests
│── transactions_data.csv # Sample sales dataset
│── pycache/ # Compiled files

---

## ▶️ How to Run  

1. Clone the repository:  
   ```bash
   git clone https://github.com/dulaah/sales-analyze-system.git
   cd sales-analyze-system/python_system
Install required libraries:
bash
Copy code
pip install pandas matplotlib numpy

Run the program:
python index.py

