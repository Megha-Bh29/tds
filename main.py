from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    try:
        df = pd.read_csv(io.StringIO(content.decode("utf-8")), skip_blank_lines=True)
        df.columns = [col.strip().lower() for col in df.columns]
        category_col = next((c for c in df.columns if "category" in c), None)
        amount_col = next((c for c in df.columns if "amount" in c), None)

        if not category_col or not amount_col:
            return {"answer": 0.0, "email": "21f1000341@ds.study.iitm.ac.in", "exam": "tds-2025-05-roe"}

        df[category_col] = df[category_col].astype(str).str.strip().str.lower()
        df[amount_col] = df[amount_col].astype(str).str.replace(",", "").str.extract(r"([-]?\d*\.?\d+)")[0]
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)
        total = df[df[category_col] == "food"][amount_col].sum()

        return {
            "answer": round(float(total), 2),
            "email": "21f1000341@ds.study.iitm.ac.in",
            "exam": "tds-2025-05-roe"
        }
    except Exception as e:
        return {
            "answer": 0.0,
            "email": "21f1000341@ds.study.iitm.ac.in",
            "exam": "tds-2025-05-roe",
            "error": str(e)
        }