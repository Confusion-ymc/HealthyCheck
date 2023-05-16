import httpx
from loguru import logger


async def httpx_request(url, method='GET', return_json=True, **kwargs):
    proxy = kwargs.pop('proxy', None)
    async with httpx.AsyncClient(proxies=proxy) as client:
        r = await client.request(url=url, method=method, **kwargs)
        if return_json:
            r.json()
        else:
            logger.info(r.text)
            return r.text
