from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    model_config = SettingsConfigDict(env_file=".env")

    # 数据库（可通过环境变量 DATABASE_URL 覆盖）
    database_url: str = "mysql+pymysql://root@localhost:3306/tea_and_snow_db?charset=utf8mb4"

    # JWT
    secret_key: str = "tea-and-snow-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7天

    # 上传文件
    upload_dir: str = "static"
    max_upload_size: int = 5 * 1024 * 1024  # 5MB

    # 微信小程序
    wechat_appid: str = ""
    wechat_appsecret: str = ""


@lru_cache()
def get_settings() -> Settings:
    return Settings()
