#!/usr/bin/python3

"""
prototype of beacon client
"""


import socket
import json
import sys
import logging
import signal
import argparse

from utility import ReturnCodes
from utility import Config


# """
# Reading:
#    https://en.wikipedia.org/wiki/OSI_model
#    https://en.wikipedia.org/wiki/Berkeley_sockets
#    https://en.wikipedia.org/wiki/IP_address
#    https://www.csd.uoc.gr/~hy556/material/tutorials/cs556-3rd-tutorial.pdf
#    https://en.wikipedia.org/wiki/Representational_state_transfer
#    https://en.wikipedia.org/wiki/Signal_(IPC)
#    https://en.wikipedia.org/wiki/Universally_unique_identifier
#    https://en.wikipedia.org/wiki/JSON
#    https://en.wikipedia.org/wiki/UTF-8
# """

class BeaconClient:
    """
    base class for all Beacon Clients
    """

    def __init__(self, cfg):
        """
        class constructor

        @param cfg object holding client configuration
        """

        self.__cfg = cfg

        logging.debug("client_address : %s",
                      self.__cfg.client_addr)
        logging.debug("client_ports : %d",
                      self.__cfg.client_ports)

        self.__socket = self.__init_socket()
        self.__run_listener = True

    def __init_socket(self):
        """
        initialize brodcast listening socket
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
                self.__cfg.client_addr,  # 0.0.0.0 = "any" address
                self.__cfg.client_ports  # on this port client will lister
            ))

        except Exception as ex:
            logging.error("failed to initialize socket: %s", str(ex))
            newsocket = None

        return newsocket

    def listen(self):
        """
        method listens for incoming 'Hello message'
        """
        logging.info("started listening for 'Hello' message")

        while self.__run_listener:
            data, address = self.__socket.recvfrom(self.__cfg.helloMaxLength)

            try:
                data = json.loads(data.decode("utf-8"))
            except Exception as ex:
                logging.error("unable to parse JSON object from message %s %s",
                              str(data), str(ex))
            else:
                logging.debug("received 'Hello' message from %s:%d, message content %s",
                              address[0], address[1], data)

                rest_api_url = "http://{0}:{1}{2}".format(
                    address[0], data["apiPort"], data["apiUrl"])

                logging.info("REST API URL: %s", rest_api_url)

        logging.info("listening terminated")

    def stop_listen(self, signal_number, frame):
        """
        stop listening for "Hello" message

        @param signal_number id of received signal
        @param frame current stack frame
        """
        logging.info("received termination signal: %d, frame: %s",
                     signal_number, str(frame))
        self.__run_listener = False


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
            description="Run listener for 'Hello' message")

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
        # create listener
        beacon_client = BeaconClient(cfg)

        # initialize signal handling for correct listener shutdown
        signal.signal(signal.SIGINT, beacon_client.stop_listen)
        signal.signal(signal.SIGTERM, beacon_client.stop_listen)

        # run listener
        return beacon_client.listen()

    except Exception as ex:
        logging.error("runtime error: %s", str(ex))
        return ReturnCodes.EXIT_FAILURE


sys.exit(main())
