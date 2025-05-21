from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from coingecko import CoinGecko, CoinInfo

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cg = CoinGecko()

@app.get("/api/coinList")
async def get_coin_list() -> List[str]:
    return cg.coinList

@app.get("/api/coinInfo")
async def get_coin_info(coin_id: Optional[str]=None) -> Dict[str, CoinInfo] | CoinInfo| None:
    if coin_id is None:
        return cg.coinInfo
    return cg.get_coin_info(coin_id)

@app.get("/api/coinWeight")
async def get_coin_weight(coin_id: Optional[str]=None) -> Dict[str, float] | float | None:
    if coin_id is None:
        return cg.weight
    return cg.weight.get(coin_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fetchData:app", host="127.0.0.1", port=3001, reload=True)