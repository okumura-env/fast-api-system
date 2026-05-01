import pytest

@pytest.mark.asyncio
async def test_async_smoke():
    assert 1 + 1 == 2