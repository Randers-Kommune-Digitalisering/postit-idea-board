import asyncio
from websockets.server import serve
import logging

logger = logging.getLogger(__name__)
clients = []

async def echo(websocket):
    # Add to connection list
    clients.append(websocket)
    logger.info(f"Added new client. Total count: {len(clients)}")

    # Receive messages
    try:
        async for message in websocket:
            logger.info(f"Received message: {message}")
            # await send_message("Hello, world!")
    except Exception as e:
        logger.error(f"Websocket error: {e}")

    # Remove from connection list
    finally:
        clients.remove(websocket)

# Start the server
async def start_server():
    async with serve(echo, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

# Send message to all clients
async def send_message(message):
    logger.info("Connection count: " + str(len(clients)))
    for connection in clients:
        await connection.send(message)

# if __name__ == "__main__":
#     logger.info(f'Started websocket server on ws://localhost:8000')
#     asyncio.run(start_server())