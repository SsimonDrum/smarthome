#!/usr/bin/python3

"""
prototype of beacon server
"""

import socket
import time
import uuid
import json
import sys
import logging
import signal
import argparse

from utility import ReturnCodes
from utility import Config


# Reading:
#     https://en.wikipedia.org/wiki/OSI_model
#     https://en.wikipedia.org/wiki/Berkeley_sockets
#     https://en.wikipedia.org/wiki/IP_address
#     https://www.csd.uoc.gr/~hy556/material/tutorials/cs556-3rd-tutorial.pdf
#     https://en.wikipedia.org/wiki/Representational_state_transfer
#     https://en.wikipedia.org/wiki/Signal_(IPC)
#     https://en.wikipedia.org/wiki/Universally_unique_identifier
#     https://en.wikipedia.org/wiki/JSON
#     https://en.wikipedia.org/wiki/UTF-8
#


class BeaconServer:
    """
    base class for all Beacon Servers
    """

    def __init__(self, cfg):
        """
        class constructor

        @param cfg object holding server configuration
        """

        self.__cfg = cfg

        logging.debug("broadcast_interval : %f s",
                      self.__cfg.broadcast_interval)
        logging.debug("server_address : %s",
                      self.__cfg.server_addr)
        logging.debug("server_port : %d",
                      self.__cfg.server_port)
        logging.debug("client_ports : %d",
                      self.__cfg.client_ports)

        self.__socket = self.__init_socket()
        self.__run_beacon = True

    def __init_socket(self):
        """
        initialize brodcast socket and bind address to it
        """

        newsocket = None

        try:
            newsocket = socket.socket(   # create socket
                socket.AF_INET,          # address family
                socket.SOCK_DGRAM,       # datagram socket
                socket.IPPROTO_UDP)      # ip protocol udp

            newsocket.setsockopt(        # set socket options
                socket.SOL_SOCKET,       # set socket-level options
                socket.SO_BROADCAST,     # "name/id" of option to be set
                1)                       # option value

            newsocket.bind((             # associate socket with address
                self.__cfg.server_addr,  # 0.0.0.0 = "any" address
                self.__cfg.server_port   # on this port server will broadcast
            ))

        except Exception as ex:
            logging.error("failed to initialize socket: %s", str(ex))
            newsocket = None

        return newsocket

    def broadcast(self):
        """
        brodcast "Hello" message in regular intervals
        """

        logging.info("starting broadcasting 'Hello'")

        # do the prerequisite check
        if self.__socket is None:
            logging.error("server socket not initialized, unable to start")
            return ReturnCodes.EXIT_FAILURE

        # construct "Hello" message
        message = {                         # python dictionary for broadcast message
            "id": uuid.getnode(),           # unique identifier of master node (this node)
            "apiPort": self.__cfg.apiPort,  # port on which resides REST API on master
            "apiUrl": self.__cfg.apiUrl     # path to REST URL
        }

        # convert python dictionary to json (no additional spaces)
        message_json = json.dumps(message, separators=(',', ':'))
        # encode JSON string to UTF-8
        message_utf8 = message_json.encode("utf-8")

        while self.__run_beacon:
            numbytes = self.__socket.sendto(
                message_utf8, ('<broadcast>', self.__cfg.client_ports))

            logging.debug("beacon has sent %d bytes: %s",
                          numbytes, message_json[0:numbytes])

            # suspend exectuin so we do not flood network
            time.sleep(self.__cfg.broadcast_interval)

        logging.info("broadcast terminated")
        return ReturnCodes.EXIT_SUCCESS

    def stop_broadcast(self, signal_number, frame):
        """
        stop brodcasting "Hello" message

        @param signal_number id of received signal
        @param frame current stack frame
        """
        logging.info("received termination signal: %d, frame: %s",
                     signal_number, str(frame))
        self.__run_beacon = False


def main():
    """
    main function
    """

    try:
        # initialize logging
        logging.basicConfig(format='%(levelname)s %(funcName)s():%(lineno)s %(message)s',
                            level=logging.DEBUG)

        # parse command line arguments
        arg_parser = argparse.ArgumentParser(
            description='Run beacon that will broadcast "Hello" message on subnet')

        # add configuration file option
        arg_parser.add_argument('-c', '--config-file',
                                type=str,
                                help='path to configuration file',
                                action='store',
                                required=True)

        args = arg_parser.parse_args()

    except Exception as ex:
        logging.error("initialization error: %s", str(ex))
        return ReturnCodes.EXIT_FAILURE

    try:
        # open and parse configuration file
        cfg = Config(args.config_file)
    except Exception as ex:
        logging.error("configuration file parse error: %s", str(ex))
        return ReturnCodes.EXIT_FAILURE

    try:
        # create server
        beacon_server = BeaconServer(cfg)

        # initialize signal handling for correct server shutdown
        signal.signal(signal.SIGINT, beacon_server.stop_broadcast)
        signal.signal(signal.SIGTERM, beacon_server.stop_broadcast)

        # run server -> start broadcasting "Hello"
        return beacon_server.broadcast()

    except Exception as ex:
        logging.error("runtime error: %s", str(ex))
        return ReturnCodes.EXIT_FAILURE


sys.exit(main())
