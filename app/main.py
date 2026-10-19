from fastapi import FastAPI
from routes import router as task_router

app = FastAPI(title="TaskFlow API", version="1.0.0", description= "A FastAPI application that transforms emails to tasks")

@app.get("/")
def read_root():
    return {"message": "Running API"}

app.include_router(task_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)