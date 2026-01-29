#!/usr/bin/env python3
"""Test Redis database connection with detailed diagnostics"""

import socket
from redis_db import redis

print("Redis Connection Diagnostics")
print("=" * 50)

# Show connection parameters
print("\nConnection Parameters:")
print(f"  Host: {redis.connection_pool.connection_kwargs.get('host', 'N/A')}")
print(f"  Port: {redis.connection_pool.connection_kwargs.get('port', 'N/A')}")
print(f"  SSL: {redis.connection_pool.connection_kwargs.get('ssl', False)}")

# Test basic connectivity
print("\nTesting Network Connectivity...")
try:
    host = redis.connection_pool.connection_kwargs.get('host', '')
    port = redis.connection_pool.connection_kwargs.get('port', 0)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((host, port))
    
    if result == 0:
        print(f"  ✓ Host {host}:{port} is reachable")
    else:
        print(f"  ✗ Host {host}:{port} is NOT reachable (error code: {result})")
    sock.close()
except Exception as e:
    print(f"  ✗ Network test failed: {e}")

# Try Redis Ping
print("\nTesting Redis Ping...")
try:
    response = redis.ping()
    print(f"  ✓ Redis Ping Successful: {response}")
except Exception as e:
    print(f"  ✗ Redis Ping Failed: {str(e)}")
    print(f"     This could mean:")
    print(f"     - The Redis server is down")
    print(f"     - The credentials are incorrect")
    print(f"     - The network is unreachable")

print("\n" + "=" * 50)
