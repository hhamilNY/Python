class DatabaseConnection:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connected = False

    def __enter__(self):    
        self.connect()
        self.connected = True
        print(f"Connected to database {self.database}"  )
        return self

    def connect(self):
        # Simulate a database connection establishment
        self.connection = f"Connected to {self.database} at {self.host}:{self.port} as {self.user}"
        return self.connection

    def disconnect(self):
        # Simulate closing the database connection
        if self.connection:
            self.connection = None
            return "Disconnected from the database"
        return "No active connection to disconnect"

    def execute_query(self, query):
        # Simulate executing a query on the database
        if not self.connection:
            return "No active connection. Please connect to the database first."
        return f"Executing query: {query} on {self.database}"   
    def __repr__(self):
        return (f"DatabaseConnection(host={self.host}, port={self.port}, "
                f"user={self.user}, database={self.database})") 
    
    def __str__(self):
        status = "connected" if self.connection else "disconnected"
        return (f"DatabaseConnection to {self.database} at {self.host}:{self.port} "
                f"as {self.user} is currently {status}")
    
    def __eq__(self, other):
        if isinstance(other, DatabaseConnection):
            return (self.host == other.host and
                    self.port == other.port and
                    self.user == other.user and
                    self.database == other.database)
        return False    
       
    def __with__(self):
        self.connect()
        return self 
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        self.connected = False
        print(f"Disconnected from database {self.database}" )
        # Handle exceptions if any
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return True  # Suppress exceptions for this example


def main(): 
    db1 = DatabaseConnection("localhost", 5432, "admin", "password", "test_db")
    print(db1.connect())        
    print(db1.execute_query("SELECT * FROM users;"))
    print(db1)
    print(repr(db1))    
    db2 = DatabaseConnection("localhost", 5432, "admin", "password", "test_db")
    print(db1 == db2)  # True
    print(db1.disconnect()) 
    print(db1)

if __name__ == "__main__":
    main()