from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Advanced Age Calculator"
    debug: bool = False
    secret_key: str = "your-secret-key-here"

    class Config:
        env_file = ".env"

settings = Settings()

# Performance Optimization Configurations
PERFORMANCE_CONFIG = {
    "cache_ttl": 300,  # 5 minutes
    "connection_pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "enable_compression": True,
    "compression_threshold": 1024
}

# Database optimization
DB_OPTIMIZATION = {
    "pool_size": 10,
    "max_overflow": 20,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "echo": False  # Disable SQL logging in production
}

# Caching configuration
CACHE_CONFIG = {
    "backend": "redis",
    "default_timeout": 300,
    "key_prefix": "age_calc:",
    "version": 1
}
