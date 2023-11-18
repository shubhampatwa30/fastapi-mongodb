import asyncio
import config
from motor.motor_asyncio import AsyncIOMotorClient

async def ping_server():
  # Replace the placeholder with your Atlas connection string
  uri = f"mongodb://{config.username}:{config.password}@ac-t24yne5-shard-00-00.m4g5i3m.mongodb.net:27017,ac-t24yne5-shard-00-01.m4g5i3m.mongodb.net:27017,ac-t24yne5-shard-00-02.m4g5i3m.mongodb.net:27017/?ssl=true&replicaSet=atlas-vxt03s-shard-0&authSource=admin&retryWrites=true&w=majority"

  # Create a new client and connect to the server
  client = AsyncIOMotorClient(uri)

  # Send a ping to confirm a successful connection
  try:
      await client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
      print(e)
      
asyncio.run(ping_server())