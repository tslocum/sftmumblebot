import AbstractConnection
import sys
import socket
import string
import util


class IRCConnection(AbstractConnection.AbstractConnection):
    def __init__(self, hostname, port, nickname, channel, encoding, name,
                 loglevel):
        super(IRCConnection, self).__init__(name, loglevel)
        self._hostname = hostname
        self._port = port
        self._nickname = nickname
        self._channel = channel
        self._encoding = encoding
        self._socket = None

        # contains all read, but uninterpreted data
        self._readBuffer = ""

    def _openConnection(self):
        self._socket = socket.socket()
        self._socket.connect((self._hostname, self._port))
        return True

    def _initConnection(self):
        """
        send initial packages:
            NICKname, USER identification, channel JOIN
        """
        if not self._sendMessage("NICK %s" % self._nickname):
            raise Exception("could not send NICK message.")
        if not self._sendMessage("USER %s %s bla :%s" %
                                 (self._nickname,
                                  self._hostname,
                                  self._nickname)):
            raise Exception("could not send USER message.")
        if not self._sendMessage("JOIN #%s" % self._channel):
            raise Exception("could not send JOIN message.")

        return True

    def _postConnect(self):
        """
        _connectionEstablished() will be called later, in _listen().
        """
        return True

    def _closeConnection(self):
        self._sendMessage("QUIT")
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        return True

    def _listen(self):
        """
        reads a bunch of data from the socket, splits it up in lines,
        and interprets them.
        the last line, if unfinished, is not interpreted and saved for the
        next _listen() call.
        """

        # read up to 1 kB of data into the buffer.
        self._readBuffer += self._socket.recv(1024)
        # get all distinct lines from the buffer into lines.
        lines = self._readBuffer.split('\n')
        # move the last (unfinished) line back into the buffer.
        self._readBuffer = lines.pop()

        # process all lines.
        for line in lines:
            line = util.try_decode(line, self._encoding)
            self._log("rx: " + line, 3)
            # split the line up at spaces
            line = line.rstrip().split(' ', 3)

            if len(line) < 2:
                continue

            # check if the line contains a ping message (PING)
            if line[0] == "PING":
                self._sendMessage("PONG " + line[1])

            if len(line) < 4:
                continue

            # check if the line contains a private message (PRIVMSG)
            if line[1] == "PRIVMSG":
                self._invokeTextCallback(line[0].split('!')[0].lstrip(': '),
                                         line[3].lstrip(': '))

            if line[3] == "#" + self._channel + " :End of /NAMES list.":
                self._connectionEstablished()

        return True

    def _sendMessageUnsafe(self, message):
        """
        send the given line via the socket.
        """
        self._log("tx: " + message, 3)
        try:
            self._socket.send(util.try_encode(message, self._encoding) + "\n")
        except Exception as e:
            self._log("failed sending %s: " % (message) + str(e), 1)
            return False
        return True

    def _sendTextMessageUnsafe(self, message):
        """
        send a PRIVMSG to #self._channel
        """
        return self._sendMessage("PRIVMSG #" + self._channel + " :" + message)

    def setAway(self, message=None):
        """
        send /AWAY command to IRC server

        if message=None, remove 'away' status
        else, set away message.
        """
        if not self._established:
            self._log("can't set away status: connection not established", 1)
            return False

        if message:
            return self._sendMessage("AWAY" + " :" + message)
        else:
            return self._sendMessage("AWAY")
