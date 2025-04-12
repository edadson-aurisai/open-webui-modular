import asyncio
import sys
import os
import logging
from datetime import datetime

# Add parent directories to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # chat-service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # backend

from app.services.folders import create_folder, get_folder
from app.services.tags import create_tag, get_tag
from app.services.chats import create_chat, get_chat
from app.services.messages import create_message, list_messages

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_database():
    try:
        # Test user ID
        user_id = "test_user_123"

        logger.info("Starting database test...")

        # 1. Create a folder
        logger.info("Creating folder...")
        folder_id = await create_folder(
            user_id=user_id,
            name="Test Folder",
            description="A test folder for database integration testing"
        )
        logger.info(f"Created folder with ID: {folder_id}")

        # Verify folder was created
        folder = await get_folder(folder_id, user_id)
        logger.info(f"Retrieved folder: {folder}")

        # 2. Create a tag
        logger.info("Creating tag...")
        tag_id = await create_tag(
            user_id=user_id,
            name="Test Tag",
            color="#FF5733"
        )
        logger.info(f"Created tag with ID: {tag_id}")

        # Verify tag was created
        tag = await get_tag(tag_id, user_id)
        logger.info(f"Retrieved tag: {tag}")

        # 3. Create a chat
        logger.info("Creating chat...")
        chat_id = await create_chat(
            user_id=user_id,
            title="Test Chat",
            messages=[],
            models=[{"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}],
            system="You are a helpful assistant.",
            tags=[tag_id]
        )
        logger.info(f"Created chat with ID: {chat_id}")

        # Verify chat was created
        chat = await get_chat(chat_id, user_id)
        logger.info(f"Retrieved chat: {chat}")

        # 4. Add a message to the chat
        logger.info("Creating message...")
        message_id = await create_message(
            user_id=user_id,
            chat_id=chat_id,
            content="Hello, this is a test message!",
            role="user"
        )
        logger.info(f"Created message with ID: {message_id}")

        # 5. Retrieve messages for the chat
        messages = await list_messages(chat_id, user_id)
        logger.info(f"Retrieved {len(messages)} messages for chat {chat_id}")
        for msg in messages:
            logger.info(f"Message: {msg}")

        logger.info("Database test completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Error during database test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_database())
    if result:
        logger.info("All tests passed!")
        sys.exit(0)
    else:
        logger.error("Tests failed!")
        sys.exit(1)
