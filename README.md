TOYLANG
====

# Language should look like

```
吾有一术，曰降龙十八掌
	必先得 青龙

	若青龙 为1
		白虎 设 青龙加1

	乃得 白虎

白虎 设 施降龙十八掌于2
录得 白虎
```

This is equivalent of:

```python3

def xianglong(qinglong):
    if qinglong > 0:
        baihu = qinglong + 1

    return baihu

baihu = xianglong(2)
```