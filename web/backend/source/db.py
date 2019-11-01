import mysql.connector

class DBInterface:
	def __init__(self, host, user, pwd, db):
		self.db = mysql.connector.connect(host=host, user=user, passwd=pwd, database=db)
		self.cursor = self.db.cursor(buffered=True)

	def query(self, q, t=None):
		if t == None:
			return self.cursor.execute(q)
		return self.cursor.execute(q,t)

	def select(self, q, t=None):
		if t == None:
			self.cursor.execute(q)
			return self.cursor.fetchall()
		self.cursor.execute(q,t)
		return self.cursor.fetchall()

	def commit(self):
		return self.db.commit()
