# cb0t.py

## How to install.

```bash
pip install git+https://github.com/tuna2134/cb0tcc.py
```

## Sync mode

```python
import cb0tcc

cbot = cb0tcc.cb0t("https://example.com")
print(cbot.url)
```

## async mode

```python
from cbotcc import aiocb0t

async def main():
    aiocbot = aiocb0t()
    aiocbot.create("https://example.com")
    print(aiocbot.url)
```
