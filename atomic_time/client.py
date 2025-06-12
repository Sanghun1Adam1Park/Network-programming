import socket
import time

def system_seconds_since_1900() -> int:
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch: int = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

if __name__ == "__main__":
  while True:
    # Connect to the server time.nist.gov on port 37
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect(("129.6.15.28", 37))
    # Receive data. (You don’t need to send anything.) You should get 4 bytes.
    # The 4 bytes represent a 4-byte big-endian number. Decode the 4 bytes with .from_bytes() into a numeric variable.
    # Print out the value from the time server, which should be the number of seconds since January 1, 1900 00:00.
      data: bytes = s.recv(4)
      nist_time = int.from_bytes(data, byteorder="big")
      print(f"NIST Time: {nist_time}")
    # Print the system time as number of seconds since January 1, 1900 00:00.
      sys_time = system_seconds_since_1900()
      print(f"System Time: {sys_time}")

      if sys_time in range(nist_time-10, nist_time+10):
        print("Yay, we have a match!")

    time.sleep(4)
