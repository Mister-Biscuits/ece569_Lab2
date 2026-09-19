import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/skyler/Documents/ece569-fall2026/ece569_Lab2/ws2/install/table_description'
