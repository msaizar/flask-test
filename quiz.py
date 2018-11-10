from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = (b'gAAAAABb4N1rLWRgGK2vrQjEmRDBTPB8JkCmXOCBKHp5sM27EFIMCNrFE6muRDdgW'
'6WfjB01CSCgWtGHkz6s-zISMPzlRbl8T9t3AcfSZnQk67506vTxKSFgYX38wo7ETQRtNnM-MRM8xM'
'qZ6_WZFpsWyxmmhPuEoE1nUwnKpFqTkmsm42Yd-Jo=')

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()