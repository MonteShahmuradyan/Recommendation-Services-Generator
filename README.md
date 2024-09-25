# Krisp-Recommendation-Services
Krisp-Recommendation-Services. 



This Project has 2 main services ` Generator and Invoker. 
Project is tested with different tools, including terminals, POST and GET methods,in browser and Postman. The app handles local and Redis caches, TTL of 10 seconds and 3 key, as project requires. 

1. Generator. Generator Service generates recommendations based on the viewer ID and the model name provided in the request. It produce an output in JSON format.
   

It performs the following tasks:
      1. Accept input parameters of viewer ID & model_name.
      2. The Generator service generates a recommendation result.
      3. The Generator returns the recommendation in a JSON format.
          
          {
            "reason": "<MODELNAME>",
            "result": <RANDOMNUMBER>
          }


2. Invoker Service. Invoker Service is the service between client and Generator, here Invoker manages data caching, both locally and with Redis.
Invoker Service performs the following tasks.
  1. It can receive requests for recommendation through a POST endpoint.
  2. Invoker Uses an local cache to store recent recommendations. This cache has a TTL (time-to-live) of 10 seconds and is limited to 3 keys as project requirements.
 the Invoker also uses Redis to store and retrieve recommendations.
  3. Invoker Service is also able for Cache Check and Generate Recommendations. Cache check first checks if the recommendation for the given viewerid is available in the local cache. If not, it queries Redis.
If recommendation is not available in local cache or Redis, Invoker service calls to Generator Service via runcascade function, Collects and combines the responses from the Generator.
  4. Serves a specific HTML page (post_request.html) based on the recommendations. This is a file which you can run on your local browser by using the file path in Your directory. It takes input of only Viewer ID, and return Recommendations, the JSON files formatted as HTML text. 
  5. POST /recommend: Endpoint that processes requests, check the caches, generates recommendations, and responds with HTML.
     GET /post_request.html: Serves an HTML file from the static directory, as browser can not directly handle POST method requests. GET allow use to interact with it via browser.



DOCKER AND DOCKER IMAGES, CONTAINERS

The project has dockerfile for each service` Generator and Invoker, and the services are orchestrated by "docker-compose.yml".
The docker-compose.yml file defines the services, networks, and volumes needed for the project.

To Deploy the project Docker, please follow the steps below

1. Do a git clone of the project -> https://github.com/MonteShahmuradyan/Krisp-Recommendation-Services.git
   and move forward to the path of the file on terminal.
2. Pull all images described in the project`s docker-compose file from  previous step in docker desktop into one container under 1 network using -> docker-compose up -d
3. Third step, run -> docker-compose up --build  , first step` docker-compose --build, second step docker-compose up... But "docker-compose up --build" is running together.
4. Verify that all images are running -> docker-compose ps
5. Can test the application and check for the desired updated.
6. Make sure to use -> docker-compose down after completing the usage of the application.
7. Optional: docker system prune: To clean all the memory that dockerized application used.
