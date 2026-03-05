import asyncio
from datetime import datetime
async def screw_function(times: int):
    print("function up")
    await asyncio.sleep(times)
    print(f"function cost up {times}")
    print("function down")

async def main():
    print(datetime.now())
    result = await asyncio.gather(
        screw_function(1),
        screw_function(2),
        screw_function(3)
    )
    print(datetime.now())
    print("main down")

function1 = main()
asyncio.run(function1)