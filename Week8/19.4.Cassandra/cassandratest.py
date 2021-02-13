"""
iNeuron
"""

from cassandra.cluster import Cluster

cluster=Cluster()

session=cluster.connect('test_keyspace')
# session.execute("INSERT INTO python_test(id, first_name,last_name) VALUES (uuid(),'ratan','bajaj')")
rows=session.execute("SELECT * FROM python_test")
for row in rows:
	print row.first_name, row.last_name

print "Done"