# ETH Swarm Python SDK

**!! This project is still under development !!**

## Usage

```python
from pyethswarm import debug_api, api

# debug api finish
debug_client = debug_api.Client()
print(debug_client.get_balances())
print(debug_client.get_balances('bbcbbac81f89966a90118584a3ec2f75ee33661f02cf1fa6c3e277767be20c5a'))
print('列出所有未兑现的支票')
print(debug_client.list_all_uncashed())

print('兑现所有支票，金额>1000')
print(debug_client.cashout())
# api todo
api_client = api.Client()
```

