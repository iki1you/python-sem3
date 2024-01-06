import asyncio


async def read_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content[:10]


async def main(filenames):
    tasks = [read_file(filename) for filename in filenames]
    names = await asyncio.gather(*tasks)
    names_str = ' '.join(name for name in names)
    return names_str
