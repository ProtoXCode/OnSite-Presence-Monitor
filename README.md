# OnSite Presence Monitor

A lightweight, dashboard-style web app that shows which employees are currently clocked in — based on ERP attendance data.

Built with [Dash](https://dash.plotly.com/) and designed to be extendable with real ERP clients (e.g. Monitor G5 API). Comes with a mock client for demo and development.

---

## 🚀 Features

- Live list of clocked-in users
- Photo-based display with styled UI
- Modular ERP client system (mock included)
- Easily swappable for real-time integrations

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/OnSite-Presence-Monitor.git
cd OnSite-Presence-Monitor
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🧪 Run the App

```bash
python app.py
```

Visit [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

---

## 📁 Project Structure

```
.
├── app.py
├── api_client/
│   ├── __init__.py
│   ├── base_client.py
│   └── mock_client.py
├── assets/
│   └── employee_images/
├── data/
│   └── sample_data.csv
├── LICENSE
└── README.md
```

---

## 🧩 Add Your Own ERP Client

Just inherit from `BaseERPClient` and implement `get_workers()`, returning a list of `UsersList` entries.

```python
class MyERPClient(BaseERPClient):
    def get_workers(self):
        # connect to your real ERP here
        return [...]
```

---

## 📝 License

[MIT License](LICENSE)  
© 2025 Tom Erik Harnes