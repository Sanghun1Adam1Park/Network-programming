# Network-programming
This repo showcases project I've worked on going through [Beej's Guide to Network Concepts](https://beej.us/guide/bgnet0/html/split/index.html).

## Naive Server and Client
In this project, I built a basic HTTP client and server using Python's `socket` module.
Both the `client` and `server` utilize sockets. The `server` generates a new `socket` for each incoming connection, it involves encoding and decoding data, and data is exchanged using the HTTP protocol format.

## Better Server
This version introduces better `server`. This `server` does not just send generic HTTP response as `naive server` did. It actually reads file from local directory and determine its type for `content-type` header. On top of that, as a security measure, it uses `reletive path` so the attacker can not access sensitive informations.
This version features an improved server. Unlike the naive version which sent generic responses, this server reads files from the local directory, determines their content type for the `Content-Type` header, and serves them. As a security measure, it uses relative paths to prevent access to sensitive information outside the designated directory.

## NIST Client
In this project, I implemented client program for [NIST Time Service](https://tf.nist.gov/tf-cgi/servers.cgi). It uses `tcp` protocol socket to connect to the time service server which then will response with time in seconds since dawn of time, January 1, 1900. The data, of course, comes in bytes in Big endian. This client converts the byte back to human readable decimal number and compares with system time to ensure that system time is in valid range.
