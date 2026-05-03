from collections import deque
import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- DATA ----------------
trade_history = []
stocks = {
    "TCS": {"price": 3500, "52wh": 3800, "52wl": 3000, "day_high": 3550, "day_low": 3450, "score": 8},
    "INFY": {"price": 1500, "52wh": 1700, "52wl": 1300, "day_high": 1520, "day_low": 1480, "score": 7},
    "RELIANCE": {"price": 2800, "52wh": 3000, "52wl": 2500, "day_high": 2850, "day_low": 2750, "score": 9},
    "HDFCBANK": {"price": 1600, "52wh": 1750, "52wl": 1400, "day_high": 1620, "day_low": 1580, "score": 8},
    "ICICIBANK": {"price": 950, "52wh": 1100, "52wl": 800, "day_high": 980, "day_low": 920, "score": 7},
    "WIPRO": {"price": 450, "52wh": 520, "52wl": 380, "day_high": 460, "day_low": 440, "score": 6},
    "SBIN": {"price": 600, "52wh": 700, "52wl": 500, "day_high": 620, "day_low": 580, "score": 7},
    "AXISBANK": {"price": 1000, "52wh": 1200, "52wl": 850, "day_high": 1020, "day_low": 980, "score": 7},
    "LT": {"price": 3200, "52wh": 3500, "52wl": 2800, "day_high": 3250, "day_low": 3150, "score": 8},
    "ITC": {"price": 420, "52wh": 480, "52wl": 350, "day_high": 430, "day_low": 410, "score": 6}
}

# Order Book
order_book = {s: {"buy": deque(), "sell": deque()} for s in stocks}

# Preload sell orders
for s in stocks:
    order_book[s]["sell"].append([100, stocks[s]["price"] + 50])
    order_book[s]["sell"].append([200, stocks[s]["price"] + 80])

# ---------------- MATCHING ENGINE ----------------
def match_orders(stock):
    buy_q = order_book[stock]["buy"]
    sell_q = order_book[stock]["sell"]

    trades = []

    while buy_q and sell_q:
        b_qty, b_price = buy_q[0]
        s_qty, s_price = sell_q[0]

        if b_price >= s_price:
            trade_qty = min(b_qty, s_qty)

            # store trade
            trade = (stock, trade_qty, s_price)
            trades.append(trade)
            trade_history.append(trade)

            buy_q[0][0] -= trade_qty
            sell_q[0][0] -= trade_qty

            if buy_q[0][0] == 0:
                buy_q.popleft()
            if sell_q[0][0] == 0:
                sell_q.popleft()
        else:
            break

    return trades

# ---------------- GUI ----------------
BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#e2e8f0"
GREEN = "#22c55e"
RED = "#ef4444"

root = tk.Tk()
root.title("Stock Exchange Simulator")
root.geometry("1200x700")
root.configure(bg=BG)

selected_stock = tk.StringVar(value="TCS")

# ---------------- STOCK LIST ----------------
stock_frame = tk.Frame(root, bg=CARD)
stock_frame.place(x=10, y=10, width=250, height=300)

stock_listbox = tk.Listbox(stock_frame, bg=CARD, fg=TEXT)
stock_listbox.pack(fill="both", expand=True)

for s in stocks:
    stock_listbox.insert(tk.END, s)

def on_stock_select(event):
    sel = stock_listbox.get(stock_listbox.curselection())
    selected_stock.set(sel)
    update_orders()
    draw_graph()
    update_stock_details()   # ADD THIS

stock_listbox.bind("<<ListboxSelect>>", on_stock_select)
# -------- STOCK DETAILS --------
details_box = tk.Text(root, bg=CARD, fg=TEXT)
details_box.place(x=10, y=320, width=250, height=230)

def update_stock_details():
    s = selected_stock.get()
    data = stocks[s]

    details_box.delete(1.0, tk.END)
    details_box.insert(tk.END, f"{s}\n\n")
    details_box.insert(tk.END, f"Price: ₹{data['price']}\n")
    details_box.insert(tk.END, f"52W High: ₹{data['52wh']}\n")
    details_box.insert(tk.END, f"52W Low: ₹{data['52wl']}\n")
    details_box.insert(tk.END, f"Day High: ₹{data['day_high']}\n")
    details_box.insert(tk.END, f"Day Low: ₹{data['day_low']}\n")
    details_box.insert(tk.END, f"Score: {data['score']}\n")

# ---------------- ORDER BOOK ----------------
tk.Label(root, text="BUY ORDERS", bg=BG, fg=GREEN).place(x=270, y=320)
tk.Label(root, text="SELL ORDERS", bg=BG, fg=RED).place(x=580, y=320)
buy_box = tk.Text(root, bg=CARD, fg=GREEN, height=10, state="disabled")
buy_box.place(x=270, y=350, width=300, height=200)
# -------- TRADE HISTORY PANEL --------
history_box = tk.Text(root, bg=CARD, fg=TEXT, state="disabled")
history_box.place(x=600, y=10, width=300, height=540)

tk.Label(root, text="TRADE HISTORY",
         bg=BG, fg=TEXT,
         font=("Helvetica", 10, "bold")).place(x=900, y=0)

sell_box = tk.Text(root, bg=CARD, fg=RED, height=10, state="disabled")
sell_box.place(x=580, y=350, width=300, height=200)

def update_orders():
    stock = selected_stock.get()
    buy_box.config(state="normal")
    sell_box.config(state="normal")
    
    buy_box.delete(1.0, tk.END)
    sell_box.delete(1.0, tk.END)

    for q, p in order_book[stock]["buy"]:
        buy_box.insert(tk.END, f"{q} @ {p}\n")

    for q, p in order_book[stock]["sell"]:
        sell_box.insert(tk.END, f"{q} @ {p}\n")
    
    buy_box.config(state="disabled")
    sell_box.config(state="disabled")
def update_history():
    history_box.config(state="normal")
    history_box.delete(1.0, tk.END)

    for stock, qty, price in trade_history[-20:]:
        history_box.insert(tk.END, f"{stock}: {qty} @ ₹{price}\n")
    
    history_box.config(state="disabled")

# -------- TRADE HISTORY PANEL --------
history_box = tk.Text(root, bg=CARD, fg=TEXT)
history_box.place(x=900, y=10, width=250, height=540)

tk.Label(root, text="TRADE HISTORY",
         bg=BG, fg=TEXT,
         font=("Helvetica", 10, "bold")).place(x=900, y=0)

# ---------------- BUY ORDER ----------------
def place_buy():
    try:
        stock = selected_stock.get()
        qty = int(qty_entry.get())
        price = int(price_entry.get())

        order_book[stock]["buy"].append([qty, price])
        trades = match_orders(stock)
        update_orders()
        update_history()

        if trades:
            msg = "Trades Executed:\n"
            for stock, q, p in trades:
                msg += f"{q} @ ₹{p}\n"
            messagebox.showinfo("Trade Success", msg)
        else:
            messagebox.showinfo("Order Placed", "Buy order added to order book")

    except:
        messagebox.showerror("Error", "Invalid input")


# ---------------- SELL ORDER ----------------
def place_sell():
    try:
        stock = selected_stock.get()
        qty = int(qty_entry.get())
        price = int(price_entry.get())

        order_book[stock]["sell"].append([qty, price])
        trades = match_orders(stock)
        update_orders()
        update_history()

        if trades:
            msg = "Trades Executed:\n"
            for stock, q, p in trades:
                msg += f"{q} @ ₹{p}\n"
            messagebox.showinfo("Trade Success", msg)
        else:
            messagebox.showinfo("Order Placed", "Sell order added to order book")

    except:
        messagebox.showerror("Error", "Invalid input")
# ---------------- INPUT PANEL ----------------
input_frame = tk.Frame(root, bg=CARD)
input_frame.place(x=270, y=570, width=610, height=100)

tk.Label(input_frame, text="Qty", bg=CARD, fg=TEXT).grid(row=0, column=0)
qty_entry = tk.Entry(input_frame)
qty_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Price", bg=CARD, fg=TEXT).grid(row=1, column=0)
price_entry = tk.Entry(input_frame)
price_entry.grid(row=1, column=1)

tk.Button(input_frame, text="Buy", bg=GREEN, width=10, command=place_buy).grid(row=2, column=0, pady=5)
tk.Button(input_frame, text="Sell", bg=RED, width=10, command=place_sell).grid(row=2, column=1, pady=5)

# ---------------- GRAPH ----------------
fig, ax = plt.subplots(figsize=(3.5,2.5))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=270, y=10, width=320, height=270)

def draw_graph():
    ax.clear()
    ax.set_facecolor('black')
    prices = [stocks[selected_stock.get()]["price"]]
    for _ in range(20):
        prices.append(prices[-1] + random.randint(-10, 10))
    ax.plot(prices, color='green', linewidth=2)
    ax.set_title(selected_stock.get(), color='white', fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    canvas.draw()

# ---------------- GAINERS / LOSERS ----------------
gl_box = tk.Text(root, bg=CARD, fg=TEXT)
gl_box.place(x=580, y=10, width=300, height=300)

def update_gainers():
    data = []
    for s in stocks:
        change = random.uniform(-3, 3)
        data.append((s, change))

    data.sort(key=lambda x: x[1], reverse=True)

    gl_box.delete(1.0, tk.END)
    gl_box.insert(tk.END, "Top Gainers:\n")
    for s, c in data[:3]:
        gl_box.insert(tk.END, f"{s} +{c:.2f}%\n")

    gl_box.insert(tk.END, "\nTop Losers:\n")
    for s, c in data[-3:]:
        gl_box.insert(tk.END, f"{s} {c:.2f}%\n")

# ---------------- INIT ----------------
update_orders()
draw_graph()
update_gainers()
update_stock_details()

root.mainloop()
