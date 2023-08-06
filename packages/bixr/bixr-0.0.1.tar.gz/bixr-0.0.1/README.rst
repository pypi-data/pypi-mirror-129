Banca d'Italia Exchange Rates
=============================

This is a Python library to access the REST API at ...


All dates are in CET/CEST
Data is only available for (Italian) workdays
Rates can be Base/quote (C) or quote/base (I) see `exchangeConventionCode`
Ranges include both extremes

There are two APIs:

- LLAPI: low level API that maps directly to REST calls, and returns the JSON response as-is.
- API: higher level API that handles pandas datetime types and returns pandas DataFrames.
