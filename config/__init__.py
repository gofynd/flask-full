from .pre_production import PreProductionConfig
from .staging import StagingConfig
from .dev import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'pre_production': PreProductionConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
}