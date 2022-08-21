import pytest
import bot_commands


class MockCTX:
    def __init__(self):
        self.sent_response = None

    async def send(self, value):
        self.sent_response = value


def return_known_list(index):
    return ["known_value"]


@pytest.mark.asyncio
async def test_dude(monkeypatch):
    moct_ctx = MockCTX()
    monkeypatch.setattr(bot_commands, 'build_list', return_known_list)
    await bot_commands.dude(moct_ctx)
    assert moct_ctx.sent_response == "known_value"


@pytest.mark.asyncio
async def test_wednesday_command(monkeypatch):
    moct_ctx = MockCTX()
    monkeypatch.setattr(bot_commands, 'build_list', return_known_list)
    await bot_commands.wednesday(moct_ctx)
    assert moct_ctx.sent_response == "known_value"
