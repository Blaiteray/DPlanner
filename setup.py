setup(
    name="DPlanner",
    version="1.0.0",
    description="An desktop application to plan deadline for windows",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Blaiteray/DPlanner",
    author="Soumitra Dx",
    author_email="soumitra.phi@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["src"],
    include_package_data=True,
    install_requires=[
        "messagebox", 
        "datetime", 
        "tkcalendar"
    ],
    entry_points={"console_scripts": ["blaiteray=src.main:main"]},
)