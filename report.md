
Your overall submission was strong and nearly covers all the testcases: 86 out of 92 pass; and all four order types are implemented and functional.

Your matching engine is actually the fastest we measured across all submissions. A 50k order workload completes in 0.15 seconds. The negated-price trick for the bid side using is well done and correctly applied throughout the codebase. Your get_market_depth is also very efficient.

The six failing tests come down to minor  issues that would be quick to fix: view_orderbook uses a property decorator instead of being a callable, the Trade class uses "volume" instead of "quantity" (and lacks buy_order_id/sell_order_id), get_market_depth crashes on unknown assets (a missing guard), and modify_order cannot detect if the new quantity is below the already-filled amount because there is no filled_quantity tracker on orders.

Your README is very helpful and concise. In some cases, having a brief comment or docstring in the functions would be helpful as well.

You did not declare the use of any AI. If no AI was used in this submission (it is graded as such), this is truly impressive!

Thanks a lot for your submission and participating!!

Please find the automated report below

# Grading Report:

## Summary

| Component                    | Tests | Raw  | AI Penalty | Score             |
| ---------------------------- | ----- | ---- | ---------- | ----------------- |
| Base — Correctness           | 43/45 | 47.8 | —          | **47.8** / 50     |
| Base — API Robustness        | 11/11 | 10.0 | —          | **10.0** / 10     |
| Base — Design Docs           | —     | —    | —          | 7 / 10 *(manual)* |
| Tier I — Multi-asset & Depth | 9/10  | 9.0  | —          | **9.0** / 10      |
| Tier II — IOC / FOK / Modify | 18/21 | 8.6  | —          | **8.6** / 10      |
| Tier III — Performance       | 5/5   | 10.0 | —          | **10.0** / 10     |
| **Grand Total**              |       |      |            | 92.4 / 100        |

---

## Base Implementation

*Core limit/market order matching, cancel, views, market data, trades, edge cases.*

### Test Results

**Base — Correctness**: 43 / 45 passed

| Test | Result |
|---|---|
| `TestBasicMarketData::test_best_ask` | ✅ passed |
| `TestBasicMarketData::test_best_ask_empty` | ✅ passed |
| `TestBasicMarketData::test_best_bid` | ✅ passed |
| `TestBasicMarketData::test_best_bid_aggregates` | ✅ passed |
| `TestBasicMarketData::test_best_bid_empty` | ✅ passed |
| `TestBasicMarketData::test_spread` | ✅ passed |
| `TestBasicMarketData::test_spread_one_side_empty` | ✅ passed |
| `TestCancelOrder::test_cancel_existing` | ✅ passed |
| `TestCancelOrder::test_cancel_filled` | ✅ passed |
| `TestCancelOrder::test_cancel_nonexistent` | ✅ passed |
| `TestCancelOrder::test_cancel_partial` | ✅ passed |
| `TestCancelOrder::test_cancel_twice` | ✅ passed |
| `TestCancelOrder::test_cancel_updates_level` | ✅ passed |
| `TestLimitOrders::test_buy_at_higher_price_matches_at_resting` | ✅ passed |
| `TestLimitOrders::test_buy_then_sell_exact` | ✅ passed |
| `TestLimitOrders::test_multiple_fills` | ✅ passed |
| `TestLimitOrders::test_no_match_different_prices` | ✅ passed |
| `TestLimitOrders::test_partial_fill` | ✅ passed |
| `TestLimitOrders::test_price_priority_over_time` | ✅ passed |
| `TestLimitOrders::test_price_time_priority` | ✅ passed |
| `TestLimitOrders::test_self_matching_allowed` | ✅ passed |
| `TestLimitOrders::test_sell_then_buy_exact` | ✅ passed |
| `TestMarketOrders::test_market_buy` | ✅ passed |
| `TestMarketOrders::test_market_not_placed_in_book` | ✅ passed |
| `TestMarketOrders::test_market_on_empty_book` | ✅ passed |
| `TestMarketOrders::test_market_sell` | ✅ passed |
| `TestMarketOrders::test_market_sweeps_at_correct_prices` | ✅ passed |
| `TestMarketOrders::test_market_sweeps_levels` | ✅ passed |
| `TestOrderBookViews::test_view_largest_excludes_cancelled` | ✅ passed |
| `TestOrderBookViews::test_view_largest_orders` | ✅ passed |
| `TestOrderBookViews::test_view_last_orders` | ✅ passed |
| `TestOrderBookViews::test_view_last_orders_limit` | ✅ passed |
| `TestOrderBookViews::test_view_orderbook` | ❌ failed |
| `TestOrderBookViews::test_view_smallest_orders` | ✅ passed |
| `TestOrderStatus::test_cancelled` | ✅ passed |
| `TestOrderStatus::test_filled` | ✅ passed |
| `TestOrderStatus::test_not_found` | ✅ passed |
| `TestOrderStatus::test_pending` | ✅ passed |
| `TestStructure::test_all_base_methods_exist` | ❌ failed |
| `TestStructure::test_import_orderbook` | ✅ passed |
| `TestStructure::test_instantiate` | ✅ passed |
| `TestTradeHistory::test_basic` | ✅ passed |
| `TestTradeHistory::test_limit` | ✅ passed |
| `TestTradeHistory::test_most_recent_first` | ✅ passed |
| `TestTradeHistory::test_none_returns_all` | ✅ passed |

**Base — API Robustness**: 11 / 11 passed

| Test | Result |
|---|---|
| `TestEdgeCases::test_empty_trade_history` | ✅ passed |
| `TestEdgeCases::test_empty_views` | ✅ passed |
| `TestEdgeCases::test_many_price_levels` | ✅ passed |
| `TestEdgeCases::test_order_str_method` | ✅ passed |
| `TestEdgeCases::test_quantity_one` | ✅ passed |
| `TestEdgeCases::test_submit_order_returns_something` | ✅ passed |
| `TestEdgeCases::test_unknown_asset_ask` | ✅ passed |
| `TestEdgeCases::test_unknown_asset_bid` | ✅ passed |
| `TestEdgeCases::test_unknown_asset_spread` | ✅ passed |
| `TestEdgeCases::test_very_large_quantity` | ✅ passed |
| `TestInstanceIndependence::test_two_instances` | ✅ passed |

### Functions

| Module | Class | Function | AI Declared |
|---|---|---|---|
| `orderbook` | `OrderResult` | `__init__` | — |
| `orderbook` | `OrderResult` | `__str__` | — |
| `orderbook` | `OrderStatus` | `__init__` | — |
| `orderbook` | `OrderStatus` | `__str__` | — |
| `orderbook` | `Trade` | `__init__` | — |
| `orderbook` | `Trade` | `__str__` | — |
| `orderbook` | `Order` | `__init__` | — |
| `orderbook` | `Order` | `__str__` | — |
| `orderbook` | `OrderBook` | `__init__` | — |
| `orderbook` | `OrderBook` | `view_orderbook` | — |
| `orderbook` | `OrderBook` | `view_last_orders` | — |
| `orderbook` | `OrderBook` | `view_largest_orders` | — |
| `orderbook` | `OrderBook` | `view_smallest_orders` | — |
| `orderbook` | `OrderBook` | `get_best_bid` | — |
| `orderbook` | `OrderBook` | `get_best_ask` | — |
| `orderbook` | `OrderBook` | `get_spread` | — |
| `orderbook` | `OrderBook` | `submit_order` | — |
| `orderbook` | `OrderBook` | `cancel_order` | — |
| `orderbook` | `OrderBook` | `get_trade_history` | — |
| `orderbook` | `OrderBook` | `get_order_status` | — |

> No AI usage declared in any of the 20 functions in this tier.

---

## Tier I — Multi-Asset & Market Depth

*Multi-asset isolation, `get_market_depth`, `get_volume_at_price`.*

**Points: 9.0 / 10** 

### Test Results

**Tier I — Multi-asset & Depth**: 9 / 10 passed

| Test | Result |
|---|---|
| `TestMarketDepth::test_depth_aggregates` | ✅ passed |
| `TestMarketDepth::test_depth_structure` | ✅ passed |
| `TestMarketDepth::test_depth_unknown_asset` | ❌ failed |
| `TestMarketDepth::test_method_exists` | ✅ passed |
| `TestMultiAsset::test_assets_isolated` | ✅ passed |
| `TestMultiAsset::test_best_bid_ask_per_asset` | ✅ passed |
| `TestMultiAsset::test_filter_by_asset` | ✅ passed |
| `TestVolumeAtPrice::test_basic` | ✅ passed |
| `TestVolumeAtPrice::test_empty` | ✅ passed |
| `TestVolumeAtPrice::test_method_exists` | ✅ passed |

### Functions

| Module | Class | Function | AI Declared |
|---|---|---|---|
| `orderbook` | `OrderBook` | `get_market_depth` | — |
| `orderbook` | `OrderBook` | `get_volume_at_price` | — |

> No AI usage declared in any of the 2 functions in this tier.

---

## Tier II — IOC / FOK / Order Modification

*Fill-or-Kill, Immediate-or-Cancel, `modify_order` with priority rules.*

**Points: 8.6 / 10** 

### Test Results

**Tier II — IOC / FOK / Modify**: 18 / 21 passed

| Test | Result |
|---|---|
| `TestFOK::test_fok_across_levels` | ✅ passed |
| `TestFOK::test_fok_empty_book` | ✅ passed |
| `TestFOK::test_fok_exact_qty` | ❌ failed |
| `TestFOK::test_fok_fully_fillable` | ✅ passed |
| `TestFOK::test_fok_not_in_book` | ✅ passed |
| `TestFOK::test_fok_price_too_low` | ✅ passed |
| `TestFOK::test_fok_rejected` | ✅ passed |
| `TestFOK::test_fok_sell` | ✅ passed |
| `TestIOC::test_ioc_correct_qty` | ❌ failed |
| `TestIOC::test_ioc_empty_book` | ✅ passed |
| `TestIOC::test_ioc_full_fill` | ✅ passed |
| `TestIOC::test_ioc_not_in_book` | ✅ passed |
| `TestIOC::test_ioc_partial` | ✅ passed |
| `TestModifyOrder::test_method_exists` | ✅ passed |
| `TestModifyOrder::test_modify_cancelled` | ✅ passed |
| `TestModifyOrder::test_modify_filled` | ✅ passed |
| `TestModifyOrder::test_modify_nonexistent` | ✅ passed |
| `TestModifyOrder::test_price_change` | ✅ passed |
| `TestModifyOrder::test_qty_below_filled` | ❌ failed |
| `TestModifyOrder::test_qty_down` | ✅ passed |
| `TestModifyOrder::test_qty_up_loses_priority` | ✅ passed |

### Functions

| Module | Class | Function | AI Declared |
|---|---|---|---|
| `orderbook` | `OrderBook` | `modify_order` | — |

> No AI usage declared in any of the 1 functions in this tier.

---

## Tier III — Performance

*Throughput on 10k–50k order streams, cancel-heavy workloads, multi-asset stress.*

**Points: 10.0 / 10** 

### Test Results

**Tier III — Performance**: 5 / 5 passed

| Test | Result |
|---|---|
| `TestPerformance::test_10k_orders` | ✅ passed |
| `TestPerformance::test_50k_orders` | ✅ passed |
| `TestPerformance::test_cancel_heavy` | ✅ passed |
| `TestPerformance::test_market_data_queries` | ✅ passed |
| `TestPerformance::test_multi_asset_stress` | ✅ passed |

