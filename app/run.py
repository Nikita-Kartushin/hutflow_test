import asyncio
import argparse
from loader.candidate_loader import CandidateLoader


async def main(path=None, n_row=None):
    loader = CandidateLoader()
    await loader.load(
        path=path,
        n_row=n_row
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("--n_row")

    args = parser.parse_args()
    path = args.path
    n_row = args.n_row

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(path=path, n_row=n_row))
