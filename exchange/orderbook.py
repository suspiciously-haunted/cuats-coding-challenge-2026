from collections import deque
import bisect
from typing import Literal, Any
import time

class OrderResult:
    def __init__(self, order_id, status, fills, remaining):
        self.id = order_id
        self.status = status
        self.fills = fills
        self.remaining = remaining
    def __str__(self):
        return f"order_id = {self.id}, status = {self.status}, fills = {self.fills}, remaining = {self.remaining}"
class OrderStatus:
    def __init__(self, order_id, status, fills, remaining, asset, side, price, volume, order_type, timestamp):
        self.id = order_id
        self.status = status          # Can be "Pending", "Partial", "Filled", "Cancelled", "Failed"
        self.fills = fills
        self.remaining = remaining
        self.asset = asset
        self.side = side
        self.price = price
        self.volume = volume
        self.order_type = order_type
        self.timestamp = timestamp
    def __str__(self):
        return f"order_id = {self.id}, status = {self.status}, fills = {self.fills}, price = {self.price}, volume = {self.volume}, timestamp = {self.timestamp}, order_type = {self.type}"
class Trade:
    def __init__(self, order_id, trader, asset, price, volume):
        self.id = order_id
        self.trader = trader
        self.asset = asset
        self.price = price
        self.volume = volume
    def __str__(self):
        return f"order_id = {self.id}, asset = {self.asset}, side = {self.side}, price = {self.price}, volume = {self.volume}, timestamp = {self.timestamp}, order_type = {self.type}"
class Order:
    def __init__(self, order_id, asset, side, price, volume, timestamp, order_type, status, order_owner):
        self.id = order_id
        self.asset = asset
        self.side = side
        self.price = price
        self.volume = volume
        self.timestamp = timestamp
        self.type = order_type
        self.status = status
        self.owner = order_owner
    def __str__(self):
        return f"order_id = {self.id}, asset = {self.asset}, side = {self.side}, price = {self.price}, volume = {self.volume}, timestamp = {self.timestamp}, order_type = {self.type}"
class OrderBook:
    def __init__(self):
        self.bids = {}  # {asset: {price: deque of Orders}}
        self.asks = {}
        self.bid_prices = {}  # dictionary of assets in ascending
        self.ask_prices = {}  # dictionary of assets in ascending
        self.order_history = [] # sorted Orders
        self.trade_history = [] # sorted filled Trades

    @property 
    def view_orderbook(self):
        return self
    
    def view_last_orders(self, n: int = 10000) -> list[Order]:
        return self.order_history[-n:][::-1]
    def view_largest_orders(self, n: int = 10000) -> list[Order]:
        return sorted([order for order in self.order_history if order.status != "Cancelled"], key = lambda x: x.volume, reverse = True)[:n]
    def view_smallest_orders(self, n: int = 10000) -> list[Order]:
        return sorted([order for order in self.order_history if order.status != "Cancelled"], key = lambda x: x.volume)[:n]


    def get_best_bid(self, asset: str) -> tuple[float, int] | None:
        if asset not in self.bid_prices or not self.bid_prices[asset]:
            return None
        best_price = -self.bid_prices[asset][0]
        total_volume = sum(order.volume for order in self.bids[asset][best_price])
        return (best_price, total_volume)
    
    def get_best_ask(self, asset: str) -> tuple[float, int] | None:
        if asset not in self.ask_prices or not self.ask_prices[asset]:
            return None
        best_price = self.ask_prices[asset][0]
        total_volume = sum(order.volume for order in self.asks[asset][best_price])
        return (best_price, total_volume)
    
    def get_spread(self, asset: str) -> float | None:
        best_bid = self.get_best_bid(asset)
        best_ask = self.get_best_ask(asset)
        if best_bid is None or best_ask is None:
            return None
        return best_ask[0] - best_bid[0]
    
    def get_market_depth(self, asset: str, levels: int = 5) -> dict:
        bid_levels = [(-neg_price, sum(order.volume for order in self.bids[asset][-neg_price])) for neg_price in self.bid_prices[asset][:levels]]
        ask_levels = [(price, sum(order.volume for order in self.asks[asset][price])) for price in self.ask_prices[asset][:levels]]
        return {"bids": bid_levels, "asks": ask_levels}
    def get_volume_at_price(self, asset: str, price: float, side: Literal["bid", "ask"]) -> int:
        book = self.bids if side == "bid" else self.asks
        if asset not in book or price not in book[asset]:
            return 0
        return sum(order.volume for order in book[asset][price])
    


    

    def submit_order(self,
        order_id: int,
        order_owner: str,
        order_type: Literal["market", "limit", "fok", "ioc"],
        side: Literal["buy", "sell"],
        asset: str,
        quantity: int,
        price: float | None = None) -> OrderResult:

        if order_type in ["limit", "fok"] and price is None:
            return OrderResult(order_id, "Failed", [], quantity)
        if asset not in self.bids:
            self.bids[asset] = {}
            self.asks[asset] = {}
            self.bid_prices[asset] = []
            self.ask_prices[asset] = []
        if side == "buy":
            book = self.bids
            price_list = self.bid_prices
            opp_book = self.asks
            opp_price_list = self.ask_prices
        else:
            book = self.asks
            price_list = self.ask_prices
            opp_book = self.bids
            opp_price_list = self.bid_prices
            
        fills = []
        status = "Pending"
        timestamp = time.time()
        remaining = quantity
        order = Order(order_id, asset, side, price, quantity, timestamp, order_type, status, order_owner)
        self.order_history.append(order)

        if order_type == "fok":
            available = 0
            for neg_p in opp_price_list[asset]:
                p = neg_p if side == "buy" else -neg_p
                if side == "buy"  and p > price: break
                if side == "sell" and p < price: break
                available += sum(o.volume for o in opp_book[asset][p])
            if available < quantity:
                return OrderResult(order_id, "Cancelled", [], quantity)
            
        while remaining > 0 and opp_price_list[asset]:
            best_price = opp_price_list[asset][0] if side == "buy" else -opp_price_list[asset][0]
            if order_type in ["limit", "fok", "ioc"]:
                if side == "buy"  and best_price > price:
                    break
                if side == "sell" and best_price < price:
                    break
            while remaining > 0 and opp_book[asset].get(best_price):
                oldest = opp_book[asset][best_price][0]
                fill_quantity = min(remaining, oldest.volume)
                fills.append({"price": best_price, "quantity": fill_quantity, "resting_order": oldest.id, "new_owner": order_owner, "prev_owner": oldest.owner})
                self.trade_history.append(Trade(order_id, order_owner, asset, best_price, fill_quantity))
                remaining -= fill_quantity
                oldest.volume -= fill_quantity
                if oldest.volume == 0:
                    oldest.status = "Filled"
                    opp_book[asset][best_price].popleft()
                else:
                    oldest.status = "Partial"
                if not opp_book[asset].get(best_price):
                    del opp_book[asset][best_price]
                    opp_price_list[asset].remove(best_price if side == "buy" else -best_price)

        filled = quantity - remaining
        if order_type == "market":
            status = "Filled" if remaining == 0 else ("Partial" if filled>0 else "Failed")
        elif order_type == "limit":
            if remaining == 0:
                status = "Filled"
            else:
                order.volume = remaining
                if price not in book[asset]:
                    book[asset][price] = deque()
                    bisect.insort(price_list[asset], (-price if side=="buy" else price))
                book[asset][price].append(order)
                status = "Partial" if filled>0 else "Pending"
        elif order_type == "fok":
                status = "Filled"
        elif order_type == "ioc":
            status = "Filled" if remaining == 0 else ("Partial" if filled > 0 else "Cancelled")
            remaining = 0
        else:
            status = "Failed"
        order.status = status
        return OrderResult(order_id, status, fills, remaining)

    def cancel_order(self, order_id: int) -> bool:
        order = next((o for o in self.order_history if o.id == order_id), None)
        if order is None or order.status in ["Filled", "Cancelled"]:
            return False
        book = self.bids if order.side == "buy" else self.asks
        price_list = self.bid_prices if order.side == "buy" else self.ask_prices
        asset = order.asset
        price = order.price
        if asset in book and price in book[asset]:
            queue = book[asset][price]
            try:
                queue.remove(order)
            except ValueError:
                return False
            if not queue:
                del book[asset][price]
                key = -price if order.side == "buy" else price
                price_list[asset].remove(key)
        order.status = "Cancelled"
        return True

    def modify_order(self,
        order_id: int,
        new_quantity: int | None = None,
        new_price: float | None = None
        ) -> bool:
        order = next((o for o in self.order_history if o.id == order_id), None)
        if order is None or order.status in ["Filled", "Cancelled"]:
            return False
        book = self.bids if order.side == "buy" else self.asks
        price_list = self.bid_prices if order.side == "buy" else self.ask_prices
        asset = order.asset
        price = order.price
        if new_quantity is not None and new_quantity <= 0:
            return False
        if asset in book and price in book[asset]:
            queue = book[asset][price]
            try:
                queue.remove(order)
            except ValueError:
                return False
            if not queue:
                del book[asset][price]
                price_list[asset].remove(price if order.side == "sell" else -price)
        
        quantity_increased = new_quantity is not None and new_quantity > order.volume
        if new_quantity is not None:
            order.volume = new_quantity
        if new_price is not None:
            order.price = new_price
            order.timestamp = time.time()
        elif quantity_increased:
            order.timestamp = time.time()

        insert_price = order.price
        if insert_price not in book[asset]:
            book[asset][insert_price] = deque()
        if new_price is None and not quantity_increased:
            book[asset][insert_price].appendleft(order)
        else:
            book[asset][insert_price].append(order)
        bisect.insort(price_list[asset], -insert_price if order.side == "buy" else insert_price)
        return True

    def get_trade_history(self, 
        asset: str | None = None,
        limit: int = 1000
        ) -> list[Trade]:
        if asset:
            return [t for t in reversed(self.trade_history) if t.asset == asset][:limit]
        return list(reversed(self.trade_history))[:limit]

    def get_order_status(self, order_id: int) -> OrderStatus | None:
        return next((o for o in self.order_history if o.id == order_id), None)