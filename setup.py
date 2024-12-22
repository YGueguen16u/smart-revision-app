from setuptools import setup, find_packages

setup(
    name="smart-revision-app",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==3.0.0",
        "flask-cors==4.0.0",
        "pytest==7.4.3",
        "pytest-flask==1.3.0",
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "python-multipart==0.0.6",
        "jinja2==3.1.2",
        "aiofiles==23.2.1",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "markdown==3.5.1"
    ],
    python_requires=">=3.8",
    package_data={
        "": ["static/*", "features/*"]
    }
)
