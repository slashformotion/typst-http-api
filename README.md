# Typst HTTP API

>> NOTE: We are not maintaining this project anymore, please do not use it in production.

***Compile typst documents with a simple HTTP request.***

<!-- This sentence is from the typst repo -->
> [Typst](https://github.com/typst/typst) is a new markup-based typesetting system
> that is designed to be as powerful as LaTeX while being much easier to learn and use.
I recommend that you check it out if you don't know it yet.

This project is a web server that allows users to compile typst markup remotely by a simple API call.
This webserver is provided in the form of a docker container [`ghcr.io/slashformotion/typst-http-api` see available tags](https://github.com/slashformotion/typst-http-api/pkgs/container/typst-http-api).

I want to bring some elements to your attention:

- All contributions are welcome of course welcome.
- Currently, there is no way to compile a file that loads external resources (images or other `.typ` files for example).

## HTTP interface

This service expose two endpoints:

- `POST /` : send the typst content directly to the endpoint (no Content-Type header required) and a streaming reponse will be return with the raw pdf bytes. You can find the corresponding curl command in the section [How does it work ?](#how-does-it-work-).
  
  If your document is not valid and an error happen at the compilation step, you will get a code 422 and a json response with the raw error[^1].
  
- `GET /metrics` : a traditional prometheus metrics endpoint (includes python gc data, http requests info and others).

## How does it work ?

Run the container:

```shell
docker run -p 8000:8000 ghcr.io/slashformotion/typst-http-api
```

Send a valid Typst file (here `test.typ`) to  the api and output the file to `result.pdf`:

```shell
curl -H "Content-Type:text/plain" -X POST --data-binary @test.typ  http://localhost:8000 --output result.pdf
```

### With docker-compose

```yml
version: "3.8"

services:
  typst-builder:
    image: ghcr.io/slashformotion/typst-http-api:v0.3.0
    ports:
      - "8000:8000"
```

## Configuration

### Rate limiting

You can enable IP based rate limiting with the following environment variable : `TYPST_HTTP_API_REQUESTS_PER_MINUTES`. Must be an uint32 > 0, it will define the number of requests per minute.

If not defined, rate limiting is disabled.

## Build the docker image locally

Build the docker image

```shell
docker build . -t typst_image
# This command build an image using the Dockerfile at the root of the project,
# then tag it with "typst_image"
```

Create a container:

```shell
docker run -p 8000:8000  typst_image
# This command creates a docker container based on the image created at the last step
```

[^1]: error example: `{"reason":"compilation error", "content": "raw error log here"}`
