# 📈 Stock Exchange Simulator

A Python-based **Stock Exchange Simulator** built using **Tkinter (GUI)**, **Matplotlib (data visualization)**, and **deque (queue data structure)**. This project mimics the basic working of a stock exchange including order placement, order matching, and trade history tracking.

---

## 🚀 Features

* 📊 Real-time stock selection and details display
* 🟢 Buy and 🔴 Sell order placement
* 🔄 Order matching engine (FIFO-based)
* 📜 Trade history tracking
* 📈 Live price graph simulation
* 📉 Top gainers and losers display

---

## 🧠 Concepts Used

### 1. Data Structures

* **Queue (deque):** Used for maintaining buy and sell orders in FIFO order
* **List:** Used for storing trade history
* **Dictionary:** Used for storing stock data and order book

### 2. Algorithms

* **Order Matching Algorithm:** Matches buy and sell orders based on price priority

### 3. GUI Development

* Built using **Tkinter**
* Layout managed using **Frames (Panels)**
* Widgets used:

  * Listbox (stock selection)
  * Text (order book, history, details)
  * Entry (input fields)
  * Button (actions)

### 4. Data Visualization

* Integrated **Matplotlib** with Tkinter using `FigureCanvasTkAgg`

---

## 🏗️ Project Structure

```
tradesimulator.py   # Main application file
README.md           # Project documentation
```

---

## ⚙️ How It Works

### 1. Order Placement

* User enters quantity and price
* Clicks Buy or Sell
* Order is added to the respective queue

### 2. Order Matching

* System checks top buy and sell orders
* If Buy Price ≥ Sell Price → Trade executes
* Partial matching supported

### 3. Trade Execution

* Trade is recorded in history
* Order quantities are updated
* Fully executed orders are removed (FIFO)

---

## 🖥️ GUI Layout

The interface is divided into multiple panels:

* 📌 **Stock List Panel** – Select stocks
* 📌 **Stock Details Panel** – View stock metrics
* 📌 **Order Book Panel** – View buy/sell orders
* 📌 **Trade History Panel** – View recent trades
* 📌 **Graph Panel** – Simulated price chart
* 📌 **Input Panel** – Place buy/sell orders

---

## 📊 Example Workflow

1. Select a stock (e.g., TCS)
2. Enter quantity and price
3. Click Buy or Sell
4. System matches orders
5. Trade is executed and displayed


