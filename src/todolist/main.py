from fastapi import FastAPI
import uvicorn
from todolist.controller import router

app = FastAPI(title="TodoList API")
app.include_router(router)

def main():
    # Lancement du serveur via le code
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()