# DNS
DNS query equivelent to function of Windows command prompt 'nslookup' command or Unix 'dig' command, motivations were to purse understanding the DNS protocol from the a transport layer perspective

Important Concepts:

1. Schema and implemention towards the solution involved: research DNS Query Message Structure (RFC 1035) and packet manipulation (WireShark) packet analysis (testing)
2. Solution was mainly composed use of: DNS Web Sockets (sockets library)
  
  2.1. Hexadecimal to bit /bytes conversion and manipulation
  
  2.2. Working with DNS Query packet metadata
  
  2.3. Parse DNS query message for answer section A record (import binascii)
