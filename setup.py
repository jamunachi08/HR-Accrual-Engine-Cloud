from setuptools import setup, find_packages

setup(
    name="hr_accrual_engine",
    version="0.1.0",
    description="Configurable HR accrual engine (Ticket, Leave, EOS) with GL postings",
    author="Your Company",
    author_email="support@yourcompany.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
