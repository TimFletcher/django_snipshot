from distutils.core import setup

setup(
    name = "django_snipshot",
    version = "0.1",
    author = "Tim Fletcher",
    author_email = "tim@timothyfletcher.com",
    description = "A reusable app for Django to allow users to edit uploaded images with snipshot.com",
    license = "BSD",
    url = "http://github.com/timfletcher/django_snipshot",
    packages=find_packages(),  # Includes all folders containing __init__.py
    include_package_data=True, # Includes templates from MANIFEST.in
    zip_safe=False,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)