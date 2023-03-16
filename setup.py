from setuptools import setup
from setuptools import find_packages

setup(name='simple_chat',
      version='0.0.1',
      description='A wrapper of openai gpt api',
      author='The fastest man alive.',
      packages=find_packages(),
      install_requires=["openai>=0.27.0","rich"])