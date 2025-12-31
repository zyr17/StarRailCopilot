"""
pytest 配置文件 - 设置测试环境和 fixtures
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def test_config_data():
    """提供测试配置数据"""
    return {
        'Scheduler': {
            'NextRun': {},
            'Enable': True
        },
        'Emulator': {
            'PackageName': 'com.StarRailCopilot.test',
            'ScreenshotPath': '/tmp'
        }
    }


@pytest.fixture
def mock_config():
    """创建模拟配置对象"""
    config = Mock()
    config.Emulator_PackageName = 'com.StarRailCopilot.test'
    config.Emulator_ScreenshotPath = '/tmp'
    config.Scheduler_Enable = True
    config.get_next_task = Mock(return_value=Mock(command='test_task'))
    config.get_next = Mock(return_value=Mock(command='test_task', next_run=None))
    config.task_call = Mock()
    config.task_delay = Mock()
    config.is_cloud_game = False
    return config


@pytest.fixture
def mock_device():
    """创建模拟设备对象"""
    device = Mock()
    device.package = 'com.StarRailCopilot.test'
    device.screenshot = Mock(return_value=Mock())
    device.screenshot_tracking = {}
    device.click_record_clear = Mock()
    device.stuck_record_clear = Mock()
    device.sleep = Mock()
    device.config = None
    device.app_is_running = Mock(return_value=False)
    device.emulator_stop = Mock()
    return device


@pytest.fixture
def mock_checker():
    """创建模拟服务器检查器"""
    checker = Mock()
    checker.wait_until_available = Mock()
    checker.is_recovered = Mock(return_value=False)
    checker.is_available = Mock(return_value=True)
    checker.check_now = Mock()
    return checker


@pytest.fixture
def sample_tasks():
    """提供示例任务列表"""
    return [
        'dungeon',
        'weekly', 
        'daily_quest',
        'battle_pass',
        'assignment',
        'data_update',
        'freebies',
        'rogue',
        'ornament',
        'benchmark',
        'daemon',
        'planner_scan'
    ]


@pytest.fixture(autouse=True)
def setup_test_environment():
    """自动设置测试环境"""
    # 设置测试模式环境变量
    os.environ['TESTING'] = '1'
    
    # 模拟一些可能影响测试的全局设置
    import module.logger
    module.logger.logger.setLevel('DEBUG')
    
    yield
    
    # 清理测试环境
    if 'TESTING' in os.environ:
        del os.environ['TESTING']


@pytest.fixture
def isolated_config():
    """创建隔离的配置实例，避免测试间的相互影响"""
    import tempfile
    import json
    
    # 创建临时配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            'Scheduler': {
                'Enable': True,
                'NextRun': {}
            },
            'Emulator': {
                'PackageName': 'com.StarRailCopilot.test',
                'ScreenshotPath': '/tmp'
            }
        }
        json.dump(config_data, f)
        config_file = f.name
    
    try:
        yield config_file
    finally:
        # 清理临时文件
        if os.path.exists(config_file):
            os.unlink(config_file)


# 测试标记
def pytest_configure(config):
    """配置自定义测试标记"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "device: marks tests that require device connections"
    )
    config.addinivalue_line(
        "markers", "gui: marks tests that require GUI"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试收集行为"""
    # 为没有标记的测试自动添加 unit 标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)
