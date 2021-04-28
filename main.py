import asyncio
import logging
import signal
from asyncio import AbstractEventLoop

from aiohttp.web import Application, run_app
from aiohttp_apiset import SwaggerRouter
from aiohttp_apiset.middlewares import jsonify
from aiohttp_apiset.swagger.operations import OperationIdMapping

from handlers import handler


def sig_handler(loop):
    logging.info("Receive interrupt signal")
    loop.stop()


def get_application(loop: AbstractEventLoop) -> Application:
    router = SwaggerRouter(
        swagger_ui='/swagger/',
        search_dirs=['./'],
    )

    app = Application(router=router, middlewares=[jsonify])

    opmap = OperationIdMapping()
    opmap.add(handler)

    router.include(spec='swagger.yaml', operationId_mapping=opmap)

    return app


def main():
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, sig_handler, loop)
    loop.add_signal_handler(signal.SIGTERM, sig_handler, loop)

    app = get_application(loop)

    # loop.run_until_complete(api.start())
    run_app(app)
    print("Backend started")

    loop.run_forever()

    loop.close()

    print("Backend stopped")


if __name__ == "__main__":
    main()
