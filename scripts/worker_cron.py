import asyncio
import os
from backend.worker import run_worker_once

def main() -> None:
    limit = int(os.getenv("DIMRI_WORKER_BATCH_SIZE", "5"))
    result = asyncio.run(run_worker_once(limit))
    print(result)

if __name__ == "__main__":
    main()
