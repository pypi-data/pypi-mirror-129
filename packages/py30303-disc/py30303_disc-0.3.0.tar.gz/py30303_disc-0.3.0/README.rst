==================================
Python UDP 30303 Discovery Library
==================================

.. image:: https://github.com/garbled1/py30303_disc/workflows/Tests/badge.svg?branch=master
    :target: https://github.com/garbled1/py30303_disc/actions?workflow=Tests
    :alt: Test Status

.. image:: https://github.com/garbled1/py30303_disc/workflows/Package%20Build/badge.svg?branch=master
    :target: https://github.com/garbled1/py30303_disc/actions?workflow=Package%20Build
    :alt: Package Build

.. image:: https://codecov.io/gh/garbled1/py30303_disc/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/garbled1/py30303_disc
    :alt: Codecov

.. image:: https://img.shields.io/readthedocs/py30303_disc/latest?label=Read%20the%20Docs
    :target: https://py30303_disc.readthedocs.io/en/latest/index.html
    :alt: Read the Docs

Summary
=======

An async python library to perform UDP network discovery.

Protocols Supported
===================

There are 3 protocols supported by this library:

* 30303 - Simple and basic
* wiznet - Wiznet devices, does not fully decode the packet (yet)
* ecowitt - Ecowitt weather stations


Notes on the 30303 Protocol
===========================

When you perform a 303030 discovery, any device that responds will report 3 things.

IP Address

Hostname
  The hostname will be from the perspective of the device, not DNS.  Often devices will have hardcoded hostnames, like a Balboa Spa WiFi will report as BWGSPA.

MAC Address
  In the form XX-XX-XX-XX-XX-XX

How to Use
==========

``pip install py30303_disc``

See the example in src/py30303_disc/d30303_discover.py

The parse function has a few modes:

parse(data, addr)
  Simply decode the message, and return the tuple

parse(data, addr, hostname="blah")
  Only return the tuple if the hostname matches

parse(data, addr, mac_prefix="XX-XX-XX")
  Only return the tuple if the mac address matches the prefix given.  Prefix
  can be of arbitrary size.

parse(data, addr, hostname="blah", mac_prefix="blah")
  Match both the hostname and the mac_prefix.


For the send_discovery() function, there are 4 modes.  Default mode is "basic_30303".

send_discovery("basic_30303")
  Sends "Discovery: Who is out there?"

send_discovery("simple_30303")
  Sends "D"

send_discovery("wiznet")
  Sends "FIND" (requires reply port bound to 5001)

send_discovery("ecowitt")
  Sends an ecowitt CMD_BROADCAST, requires reply port bound to 59387
  
Issues and Discussions
======================

As usual in any GitHub based project, raise an issue if you find any bug or room for improvement (certainly there are many), or open a discussion (new feature!!) if you want to discuss or talk :-)


Version
=======

v0.3.0
