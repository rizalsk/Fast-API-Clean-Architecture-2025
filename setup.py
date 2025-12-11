from setuptools import setup, find_packages
from app.core.config.app import app_config

setup(
    name=app_config.APP_NAME,
    version=app_config.APP_VERSION,
    packages=find_packages(),
    include_package_data=True,
)
