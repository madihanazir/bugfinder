## ✅ Local Testing Guide

### 🔧 Environment Setup

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_key_here
MOCK_MODE=true
PORT=8080
```

> **Note:** If you're just testing the API behavior, keep `MOCK_MODE=true` (no API key needed). Due to 429 error (rate limiting), Gemini API billing could not be used during testing. Hence, the deployed version does not work with the real LLM unless quota is increased.

---

### 🚀 Start the Server

Run using Python:

```bash
python main.py
```

Or with Uvicorn (preferred):

```bash
python -m uvicorn main:app --reload
```

---

### 🔍 Health Check

Open in your browser or Postman:

```http
GET http://localhost:8080/ping
```

Expected:

```json
{"message": "pong"}
```

```http
GET http://localhost:8080/healthz
```

Expected:

```json
{"status": "ok"}
```

---

### 🧪 Test Bug Detection (Main API)

Use Postman or cURL:

```http
POST http://localhost:8080/find-bug
```

#### 🔧 Optional Query Param:

```http
?mode=developer-friendly
```

OR

```http
?mode=casual
```

---

### 🪪 Mock Mode Behavior

When `MOCK_MODE=true`, the response is simulated:

```json
{
  "language": "python",
  "bug_type": "Mocked Bug",
  "description": "This is a mocked bug description.",
  "suggestion": "This is a mocked suggestion."
}
```

Helps in testing without API key. If limits are hit with real key:

```json
{
  "error": "429 Too Many Requests"
}
```

---

### 🧠 Real API Mode

Set `MOCK_MODE=false` in `.env` to activate Gemini usage.

* Replace `your_gemini_key_here` with your actual Gemini API key from Google AI Studio
* Ensure your quota is active

---

### 🔍 LLM Behavior

The API:

1. Takes your input code
2. Applies a system prompt based on the mode
3. Sends to Gemini
4. Parses and returns:

   * Bug type
   * Description
   * Suggestion

You can test this flow locally using either mock or real data.

---

### 🛠️ Debug Tip

Add this to verify mode in your terminal:

```python
print(f"[MODE] MOCK_MODE = {MOCK_MODE}")
```

---

### 📦 Final Instructions

This project is ready to run locally!

* Download the source from [Releases](https://github.com/your-repo/releases)
* Unzip the folder
* Run with `MOCK_MODE=true` for safe testing
* To test real Gemini behavior, add your `.env`

API will be live at:

```
http://localhost:8080
```


## 📦 Download & Run Locally

A ready-to-run zip file is available under the [🔗 Releases](https://github.com/your-username/your-repo-name/releases) section.

### ✅ How to Use It:

1. **Go to:** [👉 Latest Release](https://github.com/your-username/your-repo-name/releases)

2. **Download the `.zip`** file under the **Assets** section.

3. **Unzip it** on your local machine.

4. In the unzipped folder, **create a `.env` file**:

   ```env
   GEMINI_API_KEY=your_gemini_key_here
   MOCK_MODE=true
   PORT=8080
   ```

   > ⚠️ Set `MOCK_MODE=true` if you're testing without an API key.

5. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Start the API server**:

   ```bash
   python -m uvicorn main:app --reload or python main.py
   ```

7. **Access locally at**:

   * [http://localhost:8080/ping](http://localhost:8080/ping) → Pong
   * [http://localhost:8080/healthz](http://localhost:8080/healthz) → OK
   * [POST http://localhost:8080/find-bug](http://localhost:8080/find-bug) → Bug detection
Note: Due to 429 error (rate limiting), Gemini API billing could not be used during testing. Hence, the deployed version does not work with the real LLM unless quota is increased.
