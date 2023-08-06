#!/usr/bin/python3
#
# Copyright (C) 2021 Jacob Schultz Andersen schultz.jacob@gmail.com
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import grpc
import logging
import threading
from pathlib import Path
from configparser import ConfigParser
from concurrent import futures

import oocd_tool.openocd_pb2 as openocd_pb2
import oocd_tool.openocd_pb2_grpc as openocd_pb2_grpc
from oocd_tool.rpc_impl import *

_LOGGER = logging.getLogger(__name__)

class OpenOcd(openocd_pb2_grpc.OpenOcdServicer):

    def __init__(self, config):
        super(OpenOcd, self).__init__()
        self.config = config

    def LogStreamCreate(self, request, context):
        _LOGGER.info("LogStreamCreate called.")
        stop_event = threading.Event()
        self.log_reader = LogReader()

        def on_rpc_done():
            _LOGGER.debug("Attempting to regain servicer thread.")
            stop_event.set()
            self.log_reader.abort()

        context.add_callback(on_rpc_done)
        log_output = self.log_reader.read(request.filename)

        try:
            for data in log_output:
                yield openocd_pb2.LogStreamResponse(data=data)
        except:
            _LOGGER.info("Cancelling RPC LogStreamOpen.")
            context.cancel()

        _LOGGER.debug("Regained servicer thread.")

    def ProgramDevice(self, request_iterator, context):
        _LOGGER.info("StartDebug called.")
        stop_event = threading.Event()
        def on_rpc_done():
            _LOGGER.debug("Attempting to regain servicer thread.")
            stop_event.set()
        context.add_callback(on_rpc_done)

        write_file(request_iterator)
        log_output = openocd_program(self.config['cmd_program'])

        try:
            for data in log_output:
                yield openocd_pb2.LogStreamResponse(data=data)
        except:
            _LOGGER.info("Cancelling RPC RunOpenOcd.")
            context.cancel()

        _LOGGER.debug("Regained servicer thread.")

    def ResetDevice(self, request, context):
        openocd_reset_device(self.config['cmd_reset'])
        _LOGGER.info("ResetDevice called")
        return openocd_pb2.void()

    def StartDebug(self, request, context):
        openocd_start_debug(self.config['cmd_debug'])
        _LOGGER.info("StartDebug called.")
        return openocd_pb2.void()

    def StopDebug(self, request, context):
        openocd_terminate()
        _LOGGER.info("StopDebug called.")
        return openocd_pb2.void()


def _running_server(config):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2), maximum_concurrent_rpcs=1)
    openocd_pb2_grpc.add_OpenOcdServicer_to_server(OpenOcd(config), server)
    actual_port = server.add_insecure_port(config['bindto'])
    server.start()
    return server


def main():
    parser = argparse.ArgumentParser(description = 'oocd-rpcd')
    parser.add_argument(dest = 'config_file', nargs = '?', metavar = 'CONFIG', help = 'configuration file')
    args = parser.parse_args()
    parser = ConfigParser()

    if args.config_file == None or not Path(args.config_file).exists():
        raise ConfigException("Error: Missing configuration file.")

    parser.read(args.config_file)
    level_types = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}

    if parser.has_section('log'):
        config = parser['log']
        loglevel = logging.ERROR
        if 'level' in config:
            if not config['level'] in level_types:
                raise ConfigException("Error: Invalid log level specified.")
            loglevel = level_types[config['level']]
        if 'file' in config:
            logging.basicConfig(filename=config['file'], encoding='utf-8', level=loglevel)
        else:
            logging.basicConfig()

    config = parser['DEFAULT']
    server = _running_server(config)
    server.wait_for_termination()


if __name__ == "__main__":
    main()



