
from distutils.core import setup
setup(
  name = 'web_framework_v2',         # How you named your package folder (MyLib)
  packages = ['web_framework_v2', "web_framework_v2.http", "web_framework_v2.route", "web_framework_v2.security"],   # Chose the same as "name"
  version = '1.1.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Web framework for personal use',   # Give a short description about your library
  author = 'Ori Harel',                   # Type in your name
  author_email = 'oeharel@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Heknon/web_framework_v2',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Heknon/web_framework_v2/archive/refs/tags/V1.6.5.tar.gz',    # I explain this later on
  keywords = [],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'PyJWT',
          'jsonpickle',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)