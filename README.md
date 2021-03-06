### Description

This bot provides a text bridge between an IRC channel and a Mumble server.

### How to install/configure/run

You can directly run sftbot by typing `./run` or `python2 -m sftbot`.
To permanently install sftbot, type `sudo ./setup.py install`. Then, you can run it by typing `sftbot`.

You need to provide a config file that (among others) contains user credentials for the bot. An example conf file can be found in `sftbot.conf.example`.

You can either specify a conf file path as a command line argument (`sftbot myconffile.conf`), or place it at `./sftbot.conf` or `/etc/sftbot.conf`.

### Dependencies

- python2
- protobuf-python (Debian/Ubuntu package: python-protobuf, Arch package: python2-protobuf)

### TODOs

Nice-to-have features (which we don't plan to implement right now, but feel free to do it yourself):

- SSL certificate validation support
- SSL client certificate support
- More chat protocols (e.g. XMPP multi-user chat)
- Init scripts for `<your distribution here>`

### Misc

Mumble uses Google Protobuf for most of its communications; this means that one code file needs to be auto-generated (that's what the `Makefile` is there for). Unfortunately, `protoc` does not officially support `python3`, so we're forced to deal with `python2` and all its string buffer ugliness.

### Contact

You can find us at `irc.freenode.net/#sfttech`. If you found a bug, feel free to join and randomly insult channel OPs until someone fixes it (or bans you).
Alternatively, fix it yourself and send a pull request.

### Contributors/Copyright

See `COPYING`. The license is GPLv3 or higher.
