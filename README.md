# ETH Swarm Python SDK

**!! This project is still under development !!**

update to 1.0.0 api

## Usage

```python
from pyethswarm import debug_api, api

# debug api finish
debug_client = debug_api.Client()
print(debug_client.get_balances())
print(debug_client.get_balances('bbcbbac81f89966a90118584a3ec2f75ee33661f02cf1fa6c3e277767be20c5a'))
print('list_all_uncashed')
print(debug_client.list_all_uncashed())

print('cashout，amount>1000')
print(debug_client.cashout())
# api todo
api_client = api.Client()
```

[Book Of Swarm](https://gateway.ethswarm.org/bzz/latest.bookofswarm.eth/)