import asyncio
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import auth


app = FastAPI(title="Learnjot",
              description="This is the API documentation for the Learnjot application",
              version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/", include_in_schema=True)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
