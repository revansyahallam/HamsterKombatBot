from time import time
from typing import Any
import json
import asyncio
from bot.utils.logger import logger
from bot.utils.scripts import escape_html
import aiohttp

from bot.api.http import make_request


async def get_config(
        http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/config',
        {},
        'getting Config',
    )

    return response_json


async def get_config_version(http_client: aiohttp.ClientSession, config_version: str) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'GET',
        f"https://api.hamsterkombatgame.io/clicker/config/{config_version}",
        {},
        'getting config version',
    )
    return response_json


async def get_profile_data(http_client: aiohttp.ClientSession) -> dict[str]:
    while True:
        response_json = await make_request(
            http_client,
            'POST',
            'https://api.hamsterkombatgame.io/clicker/sync',
            {},
            'getting Profile Data',
            ignore_status=422,
        )

        profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

        return profile_data


async def get_ip_info(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/ip',
        {},
        'getting Ip Info',
    )
    return response_json


async def get_account_info(http_client: aiohttp.ClientSession):
    try:
        response = await http_client.post(url='https://api.hamsterkombatgame.io/auth/account-info', json={})
        response_text = await response.text()
        
        response.raise_for_status()
        response_json = json.loads(response_text)
        config_version = response.headers.get('Config-Version')
        return config_version, response_json
    except Exception as error:
        logger.error(
            f'Unknown error while get account info: {error} | '
            f'Response text: {escape_html(response_text)[:256]}...'
        )
        return "", {}


async def get_skins(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/get-skin',
        {},
        'getting Skins',
    )
    return response_json

async def buy_skin(http_client: aiohttp.ClientSession, skin_id: str) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/skin/buy',
        {"skinId": skin_id},
        'buy skin',
    )
    return response_json

async def select_skin(http_client: aiohttp.ClientSession, skin_id: str) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/skin/select',
        {"skinId": skin_id},
        'select skin',
    )
    return response_json


async def send_taps(
        http_client: aiohttp.ClientSession, available_energy: int, taps: int
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/tap',
        {
            'availableTaps': available_energy,
            'count': taps,
            'timestamp': int(time()),
        },
        'Tapping',
        ignore_status=422,
    )

    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

    return profile_data
