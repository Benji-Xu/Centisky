"""
Centisky安装程序配置
"""
from setuptools import setup, find_packages
import os

# 读取版本号
version_file = os.path.join(os.path.dirname(__file__), 'program', 'version.py')
version = "1.1.0"
with open(version_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break

# 读取README
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ""
if os.path.exists(readme_file):
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='Centisky',
    version=version,
    description='Centisky - 集成工具启动器',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Centisky',
    packages=find_packages(where='program'),
    package_dir={'': 'program'},
    python_requires='>=3.8',
    install_requires=[
        'Pillow>=9.0.0',
        'opencv-python>=4.5.0',
        'openpyxl>=3.0.0',
        'pandas>=1.3.0',
    ],
    entry_points={
        'console_scripts': [
            'centisky=launcher:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
