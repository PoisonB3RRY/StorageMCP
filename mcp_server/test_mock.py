import unittest.mock
import asyncio

# Test basic mock functionality
mock_obj = unittest.mock.Mock()
mock_obj.return_value = "test"
print("Mock return value:", mock_obj())

# Test async mock functionality
async_mock = unittest.mock.AsyncMock()
async_mock.return_value = "async test"
print("AsyncMock return value:", asyncio.run(async_mock()))

# Test that AsyncMock returns a coroutine
print("AsyncMock type:", type(async_mock()))
print("Is coroutine:", asyncio.iscoroutine(async_mock()))