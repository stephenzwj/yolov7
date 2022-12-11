docker pull heartexlabs/label-studio:latest
echo "Starting Label Studio at path $PWD"
docker run -it -p 8080:8080 -v $(pwd)/mydata:/label-studio/data heartexlabs/label-studio:latest