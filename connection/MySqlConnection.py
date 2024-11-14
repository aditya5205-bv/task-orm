from sqlalchemy import URL, Select, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from logs.custom_logging import custom_logging
from contextlib import contextmanager
from settings import DB_CONFIG

class MySqlConnection:
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance
    
    
    def __init__(self, db_config: dict):
        # self._url_object = None
        # self._engine = None 
        # self._session_factory = None
        self.is_initialized = False
    
    
    # def initialize(self,db_config: dict):
        """Initialize db connection i.e. engine and sessionmaker"""
        
        if self.is_initialized:
            custom_logging.warning("Engine is already initialized")
            return
        
        self.__url_object = URL.create(
            "mysql",
            username = db_config.get('user'),
            password = db_config.get('password'),
            port = db_config.get('port'),
            database = db_config.get('database'),
        )
        
        try:
            self._engine = create_engine(self.__url_object)
            custom_logging.info("Engine created")
            
            self._session_factory = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)
                    
            self.is_initialized = True
        
        except Exception as e:
            custom_logging.error(f"Error while creating engine {e}", exc_info=True)
        
        
    def check_initialized(self):
        """Check if the database connection has been initialized"""
        if not self.is_initialized:
            raise RuntimeError("Database not initialized")

    @contextmanager
    def _get_session(self):
        """Returns session object"""
        
        self.check_initialized()
        
        try:
            session = scoped_session(self._session_factory)
        
            yield session
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e
            
        finally:
            custom_logging.info("Session closed")
            session.close()
        
        
    def execute_query(self, query):
        
        self.check_initialized()
        
        try:
            with self._get_session() as session:
            
                res = session.execute(query)
                
                if isinstance(query, Select):
                    return res.all()
                else:
                    session.commit()
                    return True

        except Exception as e:
            custom_logging.error(f"Query execution error {e}", exc_info=True)
        
        
    def disconnect(self):
        """Close connection"""
        try:
            if self._engine:
                
                self._engine.dispose()
                self._engine = None 
                self._session_factory = None
                self.is_session = False
                
                custom_logging.info("Connection closed")
                
        except Exception as e:
            custom_logging.error(f"Error while closing connection {e}", exc_info=True)
        
        
    def __enter__(self):
        self.initialize(DB_CONFIG)
        return self
    
    def __exit__(self):
        self.disconnect()
        
