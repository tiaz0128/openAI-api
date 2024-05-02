from src.create import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="", port=8000)
