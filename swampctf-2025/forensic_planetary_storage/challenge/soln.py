# Load this directory as LDB database i.e. LevelDB (by Google). Use the python lib as below:

import plyvel

db_entries = {}

db = plyvel.DB('.')
for key, value in db:
     db_entries[key] = value

# This will give a lot of base64 encoded strings. You will have to decode almost all and you'll find the flag.
# FLAG: swampCTF{1pf5-b453d-d474b453}
sample_ouput = {

  "payload": {

    "decoded": {

      "key": "33579d5-4ac1-4823-92c7-fd3b5a6a2a07",

      "op": "PUT",

      "value": "encrypted/encoded value"

    }

  },

  "id": "/orbitdb/bafyreiejrtaennxufa3wvkdvyoj6ywq6nid3lukdqcnx2fc33tckzjzbke/ctf",

  "next": [

    {

      "/": "bafyreibbadm2ajrr6io6ufqidibrpdjfpdyfobp2aqvmcprqu5yrk7mq6q"

    }

  ],

  "refs": [

    {

      "/": "bafyreiesvykh6wt7hn4fry4mphv6ckxr5wq3c2fecvcjbqs4scbkizc6jm"

    },

    {

      "/": "bafyreihq7osywkglsjxn5lmbegtc7izqmb66atx5trkrpcmlvtcyrr6nuy"

    },

    {

      "/": "bafyreiab6do7qxgjipiypoj754vicpuscejf43eguvo2ykb2igoyrtkl64"

    }

  ],

  "version": 2,

  "key": "BJx/DXfZOVG6YkoHDGQvNQVMBaoeaEdEvcKFJP0PM1m3h9/o8lJgnTQkqGCAKovuOCovsDHQ5JOVs7qpJm3V8Ks=",

  "signature": "MEQCIF5FwOBiQKgEI7njg6He6iAlwNc+Gj8+PAll5o1PCGhKAiBlnXg9+hinX6AGB2r0uXoJ3q9Tbe6azh9euPx40G8uqw==",

  "identity": {

    "id": "02020192715ea41d7eaaceb4bd19516d0d4f1e8a2e81903480083dbdbe99dfefc9",

    "publicKey": "BJx/DXfZOVG6YkoHDGQvNQVMBaoeaEdEvcKFJP0PM1m3h9/o8lJgnTQkqGCAKovuOCovsDHQ5JOVs7qpJm3V8Ks=",

    "signatures": {

      "id": "MEQCIGx+GRqmTfPqcUL28aG2p1Q2TNEfZ9QlCgB8WU4my68UAiBZClP9WMe385COJ0WuNnXRj7BIolRC2v6vhLqUt3Yk/w==",

      "publicKey": "MEQCIFC+7AikjMLabNvdHiHh7rwrFTbystu6xc2r1h/1Zr4jAiBFxjxIMNjfI5J996HDYEQd+fnaKDi5GlNw5hgl+RwEOg=="

    },

    "type": "orbitdb",

    "Provider": "null"

  },

  "hash": {

    "/": "bafyreihq6d33ifjj6jbmjptygyksgwzcrjm5kxarbbp6djbzqx2exij27u"

  },

  "clock": {

    "id": "BJx/DXfZOVG6YkoHDGQvNQVMBaoeaEdEvcKFJP0PM1m3h9/o8lJgnTQkqGCAKovuOCovsDHQ5JOVs7qpJm3V8Ks=",

    "time": 7

  }

}
