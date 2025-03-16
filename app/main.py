

import uvicorn
import uvicorn
from fastapi import FastAPI
from app.routes import index
from app.routes import items
import config

app = FastAPI()

app.include_router(index.router)
app.include_router(items.router)

if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run("main:app", host=config.HOST,
                port=config.PORT, log_level="info")
