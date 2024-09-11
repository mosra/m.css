
from setuptools import setup, find_packages


setup(
    name="mcss-theme",
    version=0.0.1,
    description="A Pelican theme using m.css",
    long_descri
    author="W. Minchin",
    author_email="w_minchin@hotmail.com",
    url="https://github.com/MinchinWeb/seafoam",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pelican',
        'minchin.pelican.plugins.image_process>=1.0.1, !=1.1.2',
        'minchin.pelican.jinja_filters',
        # requires asset plugin, bundle? -- https://github.com/getpelican/pelican-plugins/tree/master/assets
        ],
    extras_require={
        ':python_version < "3.4"': ['pathlib2'],
        'dev': ['minchin.releaser',
                'markdown',
               ],
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Pelican :: Themes',
        ],
    zip_safe=False, 
)
