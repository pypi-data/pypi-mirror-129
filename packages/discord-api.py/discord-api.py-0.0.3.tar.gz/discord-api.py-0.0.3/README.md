# discord-api.py

## introduction

This is api wrapper for discord api.

## sample

```python
from discord_api import Client, Command

client = Client(log = False)

client.add_command(Command("ping", "pong."))

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_interaction(i)
    await i.send("Pong!", True)

client.run("token")
```

## license

Watch a `LICENSE`!