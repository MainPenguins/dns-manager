# This is a simple DNS changer for Linux, writed with Python and LibAdwaita; asami is here baby.
from app import root_access

if __name__ == "__main__":

    root_access.take_root_access("1.1.1.1", "1.0.0.1")
