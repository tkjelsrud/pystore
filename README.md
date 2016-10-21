# pystore
Python Distributed Volatile Storage Service

get(key)
# get value at key

list(key)
# get child elements at key (what if extremely large?)

set(key, value)
set(key, value, meta)
# key = location in tree struct, eg Test.Something.1
# value = any data (string)
# meta = ACL/security, NoStorage, TTL/Temporary, etc

que(key, value, meta)
# que data at key, to be read once then scrapped

unque(key)
# get first value

lock(key)
# lock, force other process to wait (+ timeout)
# also forces lock on all child elements?

transact(key) (implisit lock)
# all set() are cached until commit

unlock(key)
# unlock structure, if transaction = scrap

commit(key) (implisit unlock)
# changes done commited (now readable)

rollback(key)
# changes scrapped

clone()
# get the whole structure (for additional services)
# now..it starts getting messy :D

Library:
Caching w/MD5 check for changed data (quick TCP)

Service:
In memory tree and meta data
Data also in memory if below treshold (1k?)

Security?
Not use for sensitive data
