"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import pathlib
import os

from raccy.utils.utils import check_path_exists


class _Logger:
    """
    Base Logger class
    """
    __loggers = {}

    def __init__(self, name: str = None, fmt: str = None, filename: str = None):
        self.name = name if name else __name__
        self.fmt = fmt if fmt else '%(asctime)s:%(levelname)s:%(message)s'
        self._root_path = pathlib.Path('.').absolute()
        self.filename = filename if filename else self._get_log_file()

    def _get_log_file(self):
        log_path = os.path.join(self._root_path, 'logs/raccy.log')
        if not check_path_exists(log_path, isfile=True):
            os.mkdir(os.path.join(self._root_path, 'logs'))
        return log_path

    def _create_logger(self):
        _logger = logging.getLogger(self.name)
        _logger.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter(self.fmt)
        file_handler = logging.FileHandler(self.filename)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        _logger.addHandler(file_handler)
        _logger.addHandler(stream_handler)

        return _logger

    def _log_file_manager(self):
        """
        check if the log file size is more than 10mb then deletes it
        """
        raise NotImplementedError(f'{self.__class__.__name__}._log_file_manager() method is not implemented!')

    def __call__(self):
        if self.name in self.__loggers:
            return self.__loggers.get(self.name)
        else:
            _logger = self._create_logger()
            self.__loggers[self.name] = _logger
            return _logger


def logger(name: str = None, fmt: str = None, filename: str = None):
    _logger = _Logger(name, fmt, filename)
    return _logger()
