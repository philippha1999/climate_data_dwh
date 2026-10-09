import duckdb

con = duckdb.connect("klima.duckdb")
con.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER, name VARCHAR)")
con.execute("INSERT INTO test VALUES (1, 'Frankfurt')")
print(con.execute("SELECT * FROM test").fetchall())
con.close()
