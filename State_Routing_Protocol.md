### State Routing Protocol
#### The Basics

You need to implement the link state routing protocol by yourself. Your program will be running at all routers in the specified network. At each router, the input to your program is a set of directly attached routers (i.e. neighbours) and the costs of these links. Each router will broadcast link-state packets to all other routers in the network. Your routing program at each router should report the least-cost path and the associated cost to all other routers in the network. Your program should be able to deal with failed routers.
  

**CONFIG.TXT:**  

This file will contain the router ID and its port No in the first line. The second line has the number of neighbours for this router. Subsequent lines would have neighbour’s information including the Router ID, the cost to the neighbouring router and the port number being used by the neighbour for exchanging routing packets.

**Aims:**  

* Each router should periodically broadcast the link-state packet to its neighbours every UPDATE_INTERVAL. You should set this interval to 1 second.
* On receiving link-state packets from all other nodes, a router can build up a global view of the network topology. Given a view of the entire network topology, a router should run Dijkstra's algorithm to compute least-cost paths to all other routers within the network. Each node should wait for a ROUTE UPDATE_INTERVAL (the default value is 30 seconds) since start-up and then execute Dijkstra’s algorithm.
* Once a node fails, its neighbours must quickly be able to detect this and the corresponding links to this failed node must be removed.
* Should correctly handle of the case when a dead node joins back the topology