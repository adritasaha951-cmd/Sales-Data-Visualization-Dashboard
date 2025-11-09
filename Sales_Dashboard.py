import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load CSV Data
try:
    df = pd.read_csv("sales_data.csv")
except FileNotFoundError:
    messagebox.showerror("File Error", "sales_data.csv not found! Please place it in the same folder.")
    exit()

# Extract data
months = df["Month"]
sales_revenue = df["Revenue"]
quantities = df["Quantity"]

# Tkinter Window Setup
root = tk.Tk()
root.title("Sales Analysis Dashboard - Desmond Company")
root.geometry("1200x800")
root.config(bg="#f7f7f7")

# Title
title = tk.Label(root, text="Sales Analysis Dashboard - Desmond Company",
                 font=("Arial", 22, "bold"), bg="#f7f7f7", fg="#1f4e79")
title.pack(pady=10)

# Sales Data Table
table_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
table_frame.pack(padx=10, pady=10, fill="x")

table_title = tk.Label(table_frame, text="📋 Monthly Sales Data",
                       font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333")
table_title.pack(pady=5)

# Treeview (table)
columns = list(df.columns)
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120, anchor='center')

for _, row in df.iterrows():
    table.insert("", "end", values=list(row))

table.pack(padx=10, pady=10, fill="x")

# Main layout frame (buttons on left, chart on right)
main_frame = tk.Frame(root, bg="#f7f7f7")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Left side: Buttons
button_frame = tk.Frame(main_frame, bg="#f7f7f7")
button_frame.pack(side="left", fill="y", padx=10, pady=10)

# Right side: Chart
chart_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="solid")
chart_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Helper Function
def clear_chart():
    for widget in chart_frame.winfo_children():
        widget.destroy()

# Visualization Functions
def show_line_chart():
    clear_chart()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(months, sales_revenue, marker='o', color='blue', linewidth=2)
    ax.set_title("Sales Trend Over Time", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_area_chart():
    clear_chart()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.fill_between(months, sales_revenue, color='skyblue', alpha=0.5)
    ax.plot(months, sales_revenue, color='blue', linewidth=2)
    ax.set_title("Area Chart - Sales Growth", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_bar_chart():
    clear_chart()
    cat_sales = df.groupby("Category")["Revenue"].sum()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(cat_sales.index, cat_sales.values, color='orange')
    ax.set_title("Sales by Product Category", fontsize=14)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Sales ($)")
    ax.grid(axis='y')
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_pie_chart():
    clear_chart()
    seg_sales = df.groupby("CustomerSegment")["Revenue"].sum()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(seg_sales.values, labels=seg_sales.index, autopct='%1.1f%%',
           startangle=90, colors=['lightcoral', 'gold', 'skyblue', 'lightgreen'])
    ax.set_title("Sales Distribution by Customer Segment", fontsize=14)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# Buttons (vertical layout)
btn_style = {"font": ("Arial", 12, "bold"), "width": 22, "height": 2, "relief": "ridge"}

line_btn = tk.Button(button_frame, text="📈 Line Chart - Sales Trend",
                     bg="#1e90ff", fg="white", command=show_line_chart, **btn_style)
area_btn = tk.Button(button_frame, text="🌄 Area Chart - Sales Growth",
                     bg="#3cb371", fg="white", command=show_area_chart, **btn_style)
bar_btn = tk.Button(button_frame, text="📊 Bar Chart - Product Category",
                    bg="#ff8c00", fg="white", command=show_bar_chart, **btn_style)
pie_btn = tk.Button(button_frame, text="🥧 Pie Chart - Customer Segment",
                    bg="#dc143c", fg="white", command=show_pie_chart, **btn_style)

# Pack buttons vertically
line_btn.pack(pady=8)
area_btn.pack(pady=8)
bar_btn.pack(pady=8)
pie_btn.pack(pady=8)

# Run App
root.mainloop()
