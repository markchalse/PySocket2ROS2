from setuptools import setup

package_name = 'socket2ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='markchalse',
    maintainer_email='markjun@mail.ustc.edu.cn',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_publisher = socket2ros.test_publisher_node:main',
            'test_listen = socket2ros.test_listen_node:main',
            'socket_server = socket2ros.server_node:main'
        ],
    },
)
