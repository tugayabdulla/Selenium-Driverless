from selenium_driverless.scripts.options import Options
import asyncio
from selenium_driverless.webdriver import Chrome as AsyncDriver
import inspect


class Chrome(AsyncDriver):
    def __init__(self, options: Options = None, loop: asyncio.AbstractEventLoop = None):
        if not loop:
            loop = asyncio.new_event_loop()
        self._loop = loop
        super().__init__(options=options)

    def __enter__(self):
        return self.__aenter__()

    def __exit__(self, *args, **kwargs):
        self.__aexit__(*args, **kwargs)

    def __getattribute__(self, item):
        item = super().__getattribute__(item)
        if item is None:
            return item
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            if inspect.iscoroutinefunction(item):
                def syncified(*args, **kwargs):
                    return self._loop.run_until_complete(item(*args, **kwargs))
                return syncified
            if inspect.isawaitable(item):
                return self._loop.run_until_complete(item)
        return item
