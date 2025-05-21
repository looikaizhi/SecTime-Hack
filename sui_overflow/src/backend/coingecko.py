import json
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel
from pycoingecko import CoinGeckoAPI

CACHE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'coingecko_data.json'
CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_cache() -> Dict[str, Any]:
    if not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}

def save_cache(cache: Dict[str, Any]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')


class CoinInfo(BaseModel):
    id: str
    name: str
    symbol: str
    current_price: float
    market_cap: float
    total_volume: float
    price_change_percentage_30d: float
    circulating_supply: float
    total_supply: float

class CoinGecko:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.cache = load_cache() # 缓存
        self.coinList = self._init_coin_list()
        self.coinInfo = self._init_coin_info()
        self.weight = self._init_coin_weight()

    def _init_coin_list(self) -> List[str]:
        if 'coinList' in self.cache and self.cache['coinList']:
            return self.cache['coinList']

        default = ['sui', 'walrus-2', 'deep', 'cetus-protocol',
                   'suins-token', 'navi', 'suilend', 'bluefin']
        self.cache['coinList'] = default
        save_cache(self.cache)
        return default

    def _init_coin_info(self) -> Dict[str, CoinInfo]:
        if 'coinInfo' in self.cache and isinstance(self.cache['coinInfo'], dict) and self.cache['coinInfo']:
            return {
                cid: CoinInfo(**info)
                for cid, info in self.cache['coinInfo'].items()
            }

        raw_map: Dict[str, Any] = {}
        obj_map: Dict[str, CoinInfo] = {}
        for cid in self.coinList:
            try:
                data = self.cg.get_coin_by_id(cid)
                info = {
                    'id': data['id'],
                    'name': data['name'],
                    'symbol': data['symbol'],
                    'current_price': data['market_data']['current_price']['usd'],
                    'market_cap': data['market_data']['market_cap']['usd'],
                    'total_volume': data['market_data']['total_volume']['usd'],
                    'price_change_percentage_30d': data['market_data']['price_change_percentage_30d'],
                    'circulating_supply': data['market_data']['circulating_supply'],
                    'total_supply': data['market_data']['total_supply'],
                }
                raw_map[cid] = info
                obj_map[cid] = CoinInfo(**info)
            except Exception as e:
                print(f"Error fetching {cid}: {e}")

        self.cache['coinInfo'] = raw_map
        save_cache(self.cache)
        return obj_map

    def _init_coin_weight(self) -> Dict[str, float]:
        if 'coinWeight' in self.cache and isinstance(self.cache['coinWeight'], dict) and self.cache['coinWeight']:
            return self.cache['coinWeight']
        total_market_cap = sum(coin.market_cap for coin in self.coinInfo.values())
        weight = {k: coin.market_cap / total_market_cap for k, coin in self.coinInfo.items()}

        self.cache['coinWeight'] = weight
        save_cache(self.cache)
        return self.cache['coinWeight']

    def get_all_coins_info(self) -> Dict[str, CoinInfo]:
        return self.coinInfo

    def get_coin_info(self, coin_id: str) -> CoinInfo | None:
        return self.coinInfo.get(coin_id)
    
    def get_current_price(self, coin_id: str| List[str]) -> float | None:
        return self.cg.get_price(ids=coin_id, vs_currencies='usd')


if __name__ == "__main__":
    cg = CoinGecko()
    print("coinList:", cg.coinList)
    print("coinInfo keys:", cg.coinInfo.keys())
