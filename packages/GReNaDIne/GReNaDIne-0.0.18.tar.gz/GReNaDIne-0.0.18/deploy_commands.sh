# Run the setup and build the package
python setup.py sdist bdist_wheel
# Upload the package to pypi repository
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
twine upload --repository pypi dist/*
# build the docker image
cd ./docker/
docker build . -t speignier/grenadine
# clean <none> dandling images
docker rmi $(docker images -f "dangling=true" -q) -f
# deploy docker image
docker login
docker push speignier/grenadine
