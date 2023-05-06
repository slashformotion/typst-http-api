# Typst HTTP API

> WIP: Please be aware that this is not production ready, more work is needed. All contributions are welcome. 
> *But, it is possible to host a this container on https://render.com very easily right now (I have myself deployed an instance that seems to work well for now).* 

Some peoples asked for a typst render API. Here is a small example on how it can be achieved using the python bindings and flask. **ONLY WORKS FOR SINGLE FILE PROJECTS.**

## Build and run 

Build a docker image
```shell
docker build . -t typst_image
```

Create a container:
```shell
docker run -p 5000:5000  typst_image 
```

Send a `typ` file to the api and output the file to `result.pdf`: 

```shell
curl -H "Content-Type:text/plain" --data-binary @test.typ  http://localhost:5000 --output result.pdf             
```

Or more simply using httpie:
```shell
cat test.typ | http POST http://localhost:5000 > result.pdf
```
