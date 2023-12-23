# Typst HTTP API

<!-- This sentence is from the typst repo -->
> [Typst](https://github.com/typst/typst) is a new markup-based typesetting system
> that is designed to be as powerful as LaTeX while being much easier to learn and use.
I recommend that you check it out if you don't know it yet.

This project is a web server that allows users to compile typst markup remotely by a simple API call.
This webserver is provided in the form of a docker container.
*For now there is no official image on any registry.*

I want to bring some elements to your attention:

- Please be aware that while the container runs,
  I do not consider this project production-ready, more work is needed.
- All contributions are welcome of course welcome.
- Currently, there is no way to compile a file that loads external resources (images or other `.typ` files for example).

Current version: v0.1.0

## Build and run

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

Send `test.typ` to the api and output the file to `result.pdf`:

```shell
curl -H "Content-Type:text/plain" --data-binary @test.typ  http://localhost:8000 --output result.pdf
```

Or more simply use [httpie](https://httpie.io/cli):

```shell
cat test.typ | http POST http://localhost:8000 > result.pdf
```

- If the compilation succeeds, you will get a response with an HTTP code `200`.
The body of the response will contain the pdf document.
- On an invalid input you will get a JSON containing the error returned by the compiler with an HTTP code `422 Unprocessable Content`.

    ```json
    {
    "error": "compile error: 16:21 expected length, found string"
    }
    ```
