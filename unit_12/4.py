import asyncio


async def main(filenames):
    names = await asyncio.gather(*[read_file_sync(filename) for filename in filenames])
    names_str = ' '.join(name for name in names)
    return names_str


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()