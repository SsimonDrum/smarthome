#!/usr/bin/python3

import json


class ReturnCodes(object):
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1


class Config(object):
    def __init__(self, config_file):
        """
        constructor
        """
        self.__config_file = config_file
        self.__parse()

    def __parse(self):
        """
        open configuration file, parse it and set class members
        """
        cfg = open(self.__config_file, "r")
        data = json.loads(cfg.read())
        cfg.close()

        self.broadcast_interval = float(data["broadcast_interval"])
        if self.broadcast_interval <= 0.0:
            raise ValueError("invalid broadcast interval")

        self.server_addr = str(data["server_addr"])

        self.client_addr = str(data["client_addr"])

        self.server_port = int(data["server_port"])
        if self.server_port < 1024 or self.server_port >= 65536:
            raise ValueError("invalid server port")

        self.client_ports = int(data["client_port"])
        if self.client_ports < 1024 or self.client_ports >= 65536:
            raise ValueError("invalid client port")

        self.apiPort = int(data["apiPort"])
        if self.apiPort < 1024 or self.apiPort >= 65536:
            raise ValueError("invalid api port")

        self.apiUrl = str(data["apiUrl"])

        self.helloMaxLength = int(data["helloMaxLength"])
        if self.helloMaxLength < 1 or self.helloMaxLength > 65536:
            raise ValueError("invalid 'Hello' message length")
