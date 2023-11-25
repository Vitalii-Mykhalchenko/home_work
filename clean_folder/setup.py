from setuptools import setup , find_namespace_packages
setup(name='clean_folder',
      version='1.0.0',
      description='Program for sort file',
      url='https://github.com/Vitalii-Mykhalchenko/home_work',
      author='Vitalii Mykhalchenko',
      author_email='swimming580@gmail.com',
      license='MIT',
      packages= find_namespace_packages(),
      entry_points={
        'console_scripts': ['clean_folder = clean_folder.clean:main'],
    },
)