# DNS
DNS query equivelent to function of Windows command prompt 'nslookup' command or Unix 'dig' command
Important Concepts:
1. Blueprint and implemention: research DNS Query Message Structure (RFC 1035) and packet manipulation (WireShark) packet analysis (testing)
2. Driver: DNS Web Sockets (sockets library)
  2.1. Hexadecimal to bit /bytes conversion and manipulation
  2.2. Working with DNS Query packet metadata
  2.3. Parse DNS query message for answer section A record (import binascii)
