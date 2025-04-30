from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from routes import auth_router, product_route, store_route, user_route
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.include_router(product_route.router)
app.include_router(store_route.router)
app.include_router(user_route.router)
app.include_router(auth_router.router)

# Optional: Allow all CORS (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# Custom exception handler for 404 - Not Found
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": "The requested resource was not found."},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"An error occurred: {exc.detail}"},
    )

# Custom exception handler for general validation errors


@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Catch all unexpected exceptions


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )
