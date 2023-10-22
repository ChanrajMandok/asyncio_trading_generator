import asyncio

from trading_generator.services.service_main import ServiceMain


def run():
    asyncio.run(ServiceMain().run())