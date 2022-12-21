import psycopg2
from psycopg2 import extensions
from config import host,user,password,working_db

class Database:
	def __init__(self,db):
		self.connect=psycopg2.connect(host=host,
						user=user,
						password=password,
						database=db)
		self.cursor=self.connect.cursor()

	def create_database_and_table(self):
		self.connect=psycopg2.connect(host=host,
						user=user,
						password=password)

		self.cursor=self.connect.cursor()	
		
		result=self.cursor.execute('SELECT datname FROM pg_database')
		
		databases=self.cursor.fetchall()
		for a in databases:
			if working_db in a[0]:
				return
			
		auto_commit=extensions.ISOLATION_LEVEL_AUTOCOMMIT
		self.connect.set_isolation_level(auto_commit)
		
		self.cursor.execute("CREATE database db_test")
		self.connect.commit()
		self.cursor.close()

		self.connect=psycopg2.connect(host=host,
						user=user,
						password=password,
						database='db_test')

		self.cursor=self.connect.cursor()
		self.cursor.execute("CREATE TABLE test_table ("
								"id		BIGSERIAL,"
								"user_id 	INTEGER,"
								"username 	TEXT,"
								"balance	INTEGER DEFAULT 0,"
								"ban		BOOLEAN DEFAULT False);")
		self.connect.commit()
		self.cursor.close()

	def user_exists(self,user_id):
		with self.connect:
			result=self.cursor.execute(f"SELECT * FROM test_table WHERE user_id=%s;",(user_id,))
			result=self.cursor.fetchall()
			return bool(len(result))

	def add_user(self,user_id,username):
		with self.connect:
			self.cursor.execute(f"INSERT INTO test_table (user_id,username,ban) VALUES (%s,%s,False)",(user_id,username,))
			self.connect.commit()
			self.cursor.close()

	def add_balance(self,user_id,balance):
		with self.connect:
			self.cursor.execute(f"UPDATE test_table SET balance=balance+%s WHERE user_id=%s",(balance,user_id,))
			self.connect.commit()
			self.cursor.close()

	def get_user_data(self):
		with self.connect:
			result=self.cursor.execute(f"SELECT user_id,username,balance,ban FROM test_table")
			result=self.cursor.fetchall()
			return result

	def add_new_balance(self,user_id,balance):
		with self.connect:
			self.cursor.execute(f"UPDATE test_table SET balance=%s WHERE user_id=%s",(balance,user_id,))
			self.connect.commit()
			self.cursor.close()

	def get_user_ban(self,user_id):
		with self.connect:
			result=self.cursor.execute(f"SELECT ban FROM test_table  WHERE user_id=%s",(user_id,))
			result=self.cursor.fetchall()
			return result
	
	def ban_unban_user_db(self,user_id,ban):
		with self.connect:
			self.cursor.execute(f"UPDATE test_table SET ban=%s WHERE user_id=%s",(ban,user_id,))
			self.connect.commit()
			self.cursor.close()

	def get_ban_user(self,user_id):
		with self.connect:
			result=self.cursor.execute(f"SELECT ban FROM test_table WHERE user_id=%s",(user_id,))
			result=self.cursor.fetchall()
			print(result)
			return result[0][0]
