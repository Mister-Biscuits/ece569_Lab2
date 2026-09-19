import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'table_description'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yml')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'urdf', 'table'), glob('urdf/table/*.xacro')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='skyler',
    maintainer_email='you@example.com',
    description='URDF description of the lab table',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [],
    },
)
