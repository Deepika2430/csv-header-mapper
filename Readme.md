# CSV Header Mapping API

A Python-based Flask server that maps column headers from user-uploaded CSV files to a predefined header template. It supports exact matching, fuzzy matching, and semantic similarity. Currently integrated with the Google API via `.env` configuration.

## 🚀 Features

* Accepts CSV uploads via a simple API
* Maps headers to a predefined standard
* Returns processed CSV with updated headers
* Powered by Google API for semantic understanding

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone <REPO_URL>
cd <project-directory>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### On Windows

```bash
.\venv\Scripts\activate
```

#### On macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Add Google API Key

Create a `.env` file in the root directory:

```bash
echo "GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>" > .env
```

Replace `<YOUR_GOOGLE_API_KEY>` with your actual API key.

### 6. Run the Flask Server

```bash
python server.py
```

## 🌐 Access the UI

Visit the following endpoint in your browser:

```
http://localhost:3333/
```

You can also use your machine's IP address instead of `localhost`.

---

## 🔄 API Usage

### Endpoint

```
POST /map-headers
```

### Description

Accepts a CSV file, processes it by mapping headers to a predefined template, and returns the updated CSV file.

### Request Format

* **Method:** `POST`
* **Content-Type:** `multipart/form-data`

#### Form Data

| Key  | Type | Description             |
| ---- | ---- | ----------------------- |
| file | file | CSV file to be uploaded |

### Response

* **On Success:** Returns the processed CSV file with mapped headers.
* **On Failure:** Returns a JSON response with an error message.

```json
{
  "error": "Invalid file format"
}
```

---

## 🛠 Technologies Used

* Python
* Flask
* Google API (via `.env`)
* dotenv
