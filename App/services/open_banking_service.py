import requests
from typing import List
from datetime import datetime
from .schemas import Transaction


class OpenBankingService:
    def __init__(self, api_key: str, base_url: str = "https://api.openbanking.example.com"):
        self.api_key = api_key
        self.base_url = base_url

    async def get_transactions(self, account_id: str, from_date: datetime, to_date: datetime) -> List[Transaction]:
        url = f"{self.base_url}/accounts/{account_id}/transactions"
        params = {
            "fromBookingDateTime": from_date.isoformat(),
            "toBookingDateTime": to_date.isoformat()
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            response = await self._make_async_request(url, headers=headers, params=params)
            transactions = [
                Transaction(
                    amount=txn["amount"],
                    description=txn["description"],
                    date=datetime.fromisoformat(txn["bookingDateTime"]),
                    category=txn.get("category", "Uncategorized")
                )
                for txn in response["data"]
            ]
            return transactions
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def _make_async_request(self, url: str, **kwargs):
        # Using aiohttp for async HTTP requests
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **kwargs) as response:
                if response.status != 200:
                    raise Exception(f"API request failed with status {response.status}")
                return await response.json()