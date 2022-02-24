This piece of code gets the endpoint load timings using selenium and python.

In order to run the code, you need to install dependencies from requirement.txt and run the main.py file.

Note: Chromedriver version in this codebase is 98, please update chromedriver if needed.

Caveats

1. The chrome logs will clear out every time you access the them [refer line no 10 of the gist]. Chrome accumulates the logs till you access them. Once accessed, they are deleted from the logs memory. This is why I have passed the endpoints as a list. So that I need to access the chrome logs once and I can get all the timings at once.

2. Above function cannot handle duplicate endpoint calling at once. I am filtering the logs with endpoint here, so its better to use unique endpoints. Even if we use duplicate endpoints, it capture the timings only for the first endpoint call.