import asyncio
async def main(name:str):
    print(f"Hello {name}")

if __name__=="__main__":
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "--name",
        required=True,
        type=str,
        choices=["sami","majid","ali"],
        help="name of the person to greet"
    )
    arg = parse.parse_args()
    asyncio.run(main(arg.name))