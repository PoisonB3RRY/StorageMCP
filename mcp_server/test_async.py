import asyncio

async def test():
    print('async test')
    await asyncio.sleep(0.1)
    print('async test done')

asyncio.run(test())