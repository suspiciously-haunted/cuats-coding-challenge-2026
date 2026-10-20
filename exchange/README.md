### OrderBook design
In OrderBook, bids and asks are dictionaries for O(1) lookup. Using only a list would take O(n) lookup by price level. 
Each entry is a queue to prioritise orders by time. The queue is implemented as a doubly linked list such that poll, pop, appendleft, decreasekey is in O(1). The trade-off is remove, which will take O(n). This can be implemented by creating a Node class and manually implementing the doubly linked list, but it adds coding complexity for situations only when the queue at a single price is very long.
Other structures like list would take O(n) for appendleft and remove which is worse complexity.

bid_prices and ask_prices are maintained with bisect in sorted order. By being sorted, the best prices can be found in O(1). As bisect needs lists sorted in ascending order, the bid prices are negated. These are the costs: 
- Min/max price lookup: O(1)
- Insertion: O(log n) for bisect to find the position, then O(n) for the list shift
- Deletion: O(n) for list.remove()
 
An external library that could be used would be sorteddict for insertion, deletion at O(log n), min/max prices O(1). 
Another implementation could be a BST with O(log n) for each operation, but requires more overhead in building the data structure in python. 

order_history and trade_history are lists as they are append only which can be done in O(1). The lookup is done in O(n) but could be simplified by a separate dictionary in the future.

### Time complexity per function
| Function | Time Complexity | Complexity analysis |
|---|---|---|
| view orders | O(k) | get k orders |
| get_best_bid/ask | O(1) | get first index |
| get_spread | O(1) | two get_best calls |
| get_market_depth (d levels) | O(d x q) | sum volumes across d levels |
| submit_order (no match) | O(log n) | bisect.insort into price list |
| submit_order (k fills) | O(k) | one deque popleft per fill |
| submit_order (limit rests) | O(log n) | bisect.insort |
| cancel_order | O(m + n) | O(m) deque scan + O(n) list remove |
| modify_order | O(m + log n) | O(m) deque scan + O(log n) insort |
| get_order_status | O(h) | linear scan of order_history |
| get_trade_history | O(t) | linear scan of trade_history |
where n = price levels, m = orders at a price level, q = orders per level, h = total orders ever, t = total tradee

### Edge cases
When a price level is empty, the price level is deleted to keep the entry at [0] correct. get is used to prevent key value error.
FOK is checked before any execution to make sure the order does not fail halfway through.
