import os
import subprocess
import time
from time import sleep
from typing import Callable, Tuple, Dict, Any, Optional

from automated_insta.exceptions.utils import ArgumentException
from automated_insta.tests.environment import environment


def offline_mode(timeout: Optional[int] = 7):
    def decorator(func: Callable[[Any], Any]):
        """
        Execute the provided function without internet connection.
        If it couldn't disconnect the internet in specified time, raises Exception.
        If it couldn't reconnect the internet in specified time, raises Exception.
        :param func:
        :param timeout: Number of seconds before timing out
        """

        def wrapper(*args, **kwargs):
            # These commands need admin privileges.
            # Quick solution to elevate admin privileges: Run IDE as administrator
            os.system('netsh wlan disconnect')
            if __is_network_connected(timeout=timeout):
                raise Exception

            func_e = None
            try:
                func(*args, **kwargs)
            except Exception as e:
                func_e = e

            os.system(f'netsh wlan connect name={environment.NETWORK_NAME}')
            if not __is_network_connected(timeout=timeout):
                raise Exception

            if func_e:
                raise func_e

        @timeout_checker(expected_result=True)
        def __is_network_connected(timeout: Optional[int]) -> bool:
            sp = subprocess.Popen(f'netsh interface show interface name={environment.INTERFACE_NAME}',
                                  stdout=subprocess.PIPE)
            output = str(sp.stdout.read())
            # This is a sample of what this line returns:
            #
            # Wi-Fi
            # Type:                 Dedicated
            # Administrative state: Enabled
            # Connect state:        Connected
            #
            output = output.lower()
            sp.stdout.close()
            sp.kill()
            return False if output.find('disconnected') != -1 else True

        return wrapper

    return decorator


def timeout_checker(expected_result: Any):
    """
    Repeats the given function until it returns the expected result or time out.
    :param expected_result: The result that you expect to get from the given function.
    """

    def decorator(func: Callable[[Tuple, Dict], Any]):
        def wrapper(*args, **kwargs):
            key = 'timeout'
            timeout = kwargs.get(key)
            if timeout is None:
                # 'timeout' should be passed to the 'func' by keyword: 'timeout=seconds'.
                raise ArgumentException(key)

            start_time = time.time()
            while True:
                result = func(*args, **kwargs)
                if result == expected_result:
                    break
                sleep(0.1)
                if time.time() - start_time > timeout:
                    break
            return result

        return wrapper

    return decorator
