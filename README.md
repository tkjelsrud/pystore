# pystore
Python Distributed Volatile Storage Service

Get
get(key)
# get value at key

List
list(key)
# get child elements at key (what if extremely large?)

Set
set(key, value)
set(key, value, meta)
# key = location in tree struct, eg Test.Something.1
# value = any data (string)
# meta = ACL/security, NoStorage, TTL/Temporary, etc

Que
que(key, value, meta)
# que data at key, to be read once then scrapped
unque(key)
# get first value

Lock
lock(key)
# lock, force other process to wait (+ timeout)
# also forces lock on all child elements?

Transact
transact(key) (implisit lock)
# all set() are cached until commit
unlock(key)
# unlock structure, if transaction = scrap
commit(key) (implisit unlock)
# changes done commited (now readable)
rollback(key)
# changes scrapped

Sharing
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
