# Binance Candles

Provides python generator for crypto currency 1 min candles via Binance Socket API

## CandlesGenerator example

```
from binance_candles import CandlesGenerator

candles_generator = CandlesGenerator()
candles_generator.start()
for candle in candles_generator:
    print(candle)
```


## BufferedCandlesGenerator example

```
candles_generator = BufferedCandlesGenerator(2)
candles_generator.start()
for candles in candles_generator:
    for candle in candles:
        print(candle)
```
