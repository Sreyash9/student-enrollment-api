from fastapi import FastAPI

app = FastAPI(title="Student Course Enrollment API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
