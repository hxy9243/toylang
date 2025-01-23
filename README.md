TOYLANG
====

# Summary

This is a toy POV project that shows how the easiest interpreter/transpiler could work. Hopefully it makes you excited about programming.

# Overview

```
吾有一术曰,降龙十八掌,欲练此术,必先得,青龙
    白虎,设,1
	若,青龙,为1
		白虎,设,青龙,加1
	乃得白虎
白虎,设,施降龙十八掌,2
录得白虎
```

This is equivalent of:

```python3
def 降龙十八掌(青龙, ):

        白虎=1
        if 青龙==1:
                白虎=青龙+1
        return 白虎
白虎=降龙十八掌(2)
print(白虎)
```

# Quickstart

At this point everything is in one file. Simply pull the repo and run:

```
python3 toylang/toylang.py
```