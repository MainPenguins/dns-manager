import sys

from app.application import DNSChanger


app = DNSChanger()
app.run(sys.argv)
