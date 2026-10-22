from fastapi import FastAPI

app = FastAPI(title="MNEMORA AI", version="0.1.0")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mnemora-ai",
    }
