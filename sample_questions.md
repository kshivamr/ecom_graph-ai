# Sample Questions and Results

This file contains sample natural-language questions tested with the E-commerce Knowledge Graph and AI Retrieval System.

---

## 1. What is the price of iPhone 15?

### Result

```text
Product ID: P001
Product Name: iPhone 15
Price: ₹69,999
Brand: Apple
Category: Smartphones
Vendor: TechWorld
```

### Final Answer

```text
The price of the iPhone 15 is ₹69,999.
```

---

## 2. Show me products in Fruits category

### Result

```text
P007 → Banana — ₹80
P008 → Banana Smoothie — ₹150
P009 → Organic Banana — ₹120
P010 → Banana Chips — ₹100
P016 → Banana Bread — ₹180
```

### Final Answer

```text
The products in the Fruits category are:

- Banana — ₹80
- Banana Smoothie — ₹150
- Organic Banana — ₹120
- Banana Chips — ₹100
- Banana Bread — ₹180
```

---

## 3. Which products from Apple are supplied by TechWorld?

### Result

```text
P001 → iPhone 15 — ₹69,999
P003 → MacBook Air M2 — ₹89,999
```

### Final Answer

```text
Apple products supplied by TechWorld are:

- iPhone 15 — ₹69,999
- MacBook Air M2 — ₹89,999
```

---

## 4. What has Rahul Sharma ordered?

### Result

```text
Order O001 → iPhone 15 — Quantity: 1
Order O001 → Banana — Quantity: 5
Order O002 → MacBook Air M2 — Quantity: 1
```

### Final Answer

```text
Rahul Sharma has ordered:

- iPhone 15 — quantity 1
- Banana — quantity 5
- MacBook Air M2 — quantity 1
```

---

## 5. Find products containing mouse

### Result

```text
P011 → Wireless Mouse — ₹999
```

### Final Answer

```text
The product containing "mouse" is:

Wireless Mouse — ₹999
```

---

## 6. Show me all banana products

### Result

```text
P007 → Banana — ₹80
P008 → Banana Smoothie — ₹150
P009 → Organic Banana — ₹120
P010 → Banana Chips — ₹100
P016 → Banana Bread — ₹180
```

### Final Answer

```text
There are 5 banana products:

- Banana — ₹80
- Banana Smoothie — ₹150
- Organic Banana — ₹120
- Banana Chips — ₹100
- Banana Bread — ₹180
```

---

## Summary

The system successfully demonstrates natural-language retrieval for:

- Product details
- Category-based retrieval
- Brand and vendor-based retrieval
- Customer order retrieval
- Product search
- Banana product retrieval
