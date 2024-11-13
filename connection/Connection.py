from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from logs.custom_logging import custom_logging
from contextlib import contextmanager

class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance


class Connection(metaclass=SingletonMeta):
    
    def __init__(self):
        
        self._url_object = None
        self._engine = None 
        self._session_factory = None
        
        self.is_initialized = False
    
    
    def initialize(self,db_config: dict):
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
            custom_logging.error(f"Error while creating engine: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
        
        
    def _check_initialized(self):
        """Check if the database connection has been initialized"""
        if not self.is_initialized:
            raise RuntimeError("Database not initialized")

    @contextmanager
    def get_session(self):
        """Returns sessions"""
        
        self._check_initialized()
        
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
            custom_logging.error(f"Error while closing connection: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
        
        