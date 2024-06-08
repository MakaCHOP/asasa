import asyncio
from multiprocessing import Process
from initilizers.WebApp import run_web_app
from Socket.main import main

if __name__ == "__main__":
    Process(target=run_web_app).start()
    asyncio.run(main())
