# pystore
Python Distributed Volatile Storage Service
Establish full duplex socket connections, byte streams

#logon(public key, secret encr)
establish session, get session variables
server may redirect (load balancing?)

#get(key)
if authed, get value at key (value, meta)

#getInt(key)
get as integer (fail if not stored as such)

#list(key)
get child elements at key (what if extremely large?)
maintain timestamp of last received (to detect if no new data coming)

#listen(key)
asynchronously, receive all data entering (que/broadcast only) 

#set(key, value, meta)
key = location in tree struct, eg MYAPP.TEST.1
[KEY-FixLen Meta-FixLen DATA-len PAYLOAD]
value = any data (string)
meta = ACL/security, NoStorage, TTL/Temporary, asInt, asString, etc

#store(key)
#store(key, value, meta)
like set, but forces storage to external repository (non volatile), sycnronous, does not limit length?

#que(key, value)
#que(key, value, meta)
que data at key, append to existing data, to be read once then scrapped
que data is short (number or small string), fixed length (32 bytes?), ACL only at node not each que element
[KEY-FixLen Meta-FixLen UPD-DATA-len PAYLOAD PAYLOAD PAYLOAD...]
This may overflow...
#unque(key)
get first value

#lock(key)
lock, force other process to wait (+ timeout)
also forces lock on all child elements?

#transact(key) (implisit lock)
all set() are cached until commit
#unlock(key)
unlock structure, if transaction = scrap
#commit(key) (implisit unlock)
changes done commited (now readable)
#rollback(key)
changes scrapped

#clone() / sync()
check if needed to exchange data / get the whole structure (for additional services)
now..it starts getting messy :D

#segment(key)
force key segment to be stored in separate file/repository

#stat()
get stats, total elements, memory usage, requests pr time

Library:
Caching w/MD5 check for changed data (quick TCP)

Service:
In memory tree and meta data
Data also in memory if below treshold (1k?)
Keep in memory if requested often (time to live), then store

Security?
Not use for sensitive data
