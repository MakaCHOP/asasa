import asyncio
from multiprocessing import Process
from initilizers.WebApp import run_web_app
from websocket.main import main
from websocket.user_actions.new_user import new_user_bot

#from websocket.user_actions.new_user import new_user_bot
from websocket.utils.mongo_handler import space, users

if __name__ == "__main__":
    space.drop_collection(users)
    new_user_bot(1, "ali", "asasas", ref_id=1)
    Process(target=run_web_app).start()
    asyncio.run(main())
