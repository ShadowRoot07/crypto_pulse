# ⚡ SHADOW_PULSE v1.0.4

![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-cyan?style=for-the-badge&logo=target)
![Build](https://img.shields.io/badge/CI%2FCD-GITHUB_ACTIONS-fuchsia?style=for-the-badge&logo=githubactions)
![Hardware](https://img.shields.io/badge/HARDWARE-MOBILE_TERMUX-orange?style=for-the-badge&logo=termux)

A high-performance **Crypto Intelligence Terminal** built for the decentralized future. This system monitors real-time market fluctuations, provides AI-driven technical analysis, and serves as an encrypted knowledge repository for blockchain operations.

---

## 🛠️ SYSTEM ARCHITECTURE

`SHADOW_PULSE` is engineered to be lightweight yet powerful, capable of running entirely from a mobile environment (**Termux**) while handling complex tasks in the cloud.

* **Core Engine:** Django 5.x (Python 3.13+)
* **Neural Link:** Groq Cloud API (Llama 3.3 70B Model)
* **Visual Interface:** Tailwind CSS + Chart.js (Cyberpunk UI/UX)
* **Data Hub:** PostgreSQL (via Neon.tech)
* **Intelligence:** BeautifulSoup4 for Real-Time Web Scraping
* **Deployment:** Vercel Edge Network

---

## 🛸 KEY FEATURES

### 1. Real-Time Command Center (Dashboard)
Live tracking of the Top 10 Cryptocurrencies with dynamic SVG/Canvas charting. Every pulse of the market is captured and displayed in a high-contrast scanner interface.

### 2. AI_PREDICTOR_V1 (AJAX Powered)
Asynchronous market analysis module. Enter a trade amount and receive an instant technical verdict from the AI without interrupting the live feed.

### 3. Encrypted Chat & Advisor Bot
An interactive communication bridge. Ask the **Advisor Bot** about technical trends or wait for the **News Bot** to inject real-world decrypted headlines directly into the terminal.

### 4. Crypto_Archives (The Wiki)
A curated knowledge base for operators to master blockchain fundamentals, mining protocols, and trading strategies.

---

## ⌨️ TERMINAL COMMANDS (Management)

Manage the system directly from your shell:

| Command | Action |
| :--- | :--- |
| `python manage.py update_prices` | Sync market data with global exchanges. |
| `python manage.py run_news_bot` | Scrape real news and summarize via AI. |
| `python manage.py purge_data` | Clear chat logs and system noise. |
| `python manage.py purge_data --all` | Factory reset for all database records. |

---

## 🛠️ INSTALLATION & DEPLOYMENT

### Local Environment (Termux/PC)
```bash
# Clone the repository
git clone [https://github.com/ShadowRoot07/crypto_pulse.git](https://github.com/ShadowRoot07/crypto_pulse.git)

# Install dependencies
pip install -r requirements.txt

# Sync Database
python manage.py migrate

# Initialize System
python manage.py runserver
```

## CI/CD Deployment

This project is configured for GitHub Actions. Upon every push to main, the system undergoes a rigorous test suite to ensure connection integrity and logic stability before deploying to Vercel.

## 🛡️ ENCRYPTION & SECURITY

The connection to the PostgreSQL backbone is secured via SSL. All API keys and sensitive credentials are encrypted using environment variables, ensuring zero exposure of the system's core.

LOG_MESSAGE: "In the shadow of the code, we find the pulse of the future."

### Developed by __ShadowRoot07__
