# Technologies

* Python 3.7.10 +
* Docker

# Dependencies

* Scrapy

# How to Run?

* Python
  - Install requeriments and then run:
  ```
  cat sample_docker.txt | python3 cialdnb/runner.py
  ```
  
* Docker
  - Build Image:
  ```
  docker build -t basic_info:latest .
  ```
  - Run:
  ```
  cat sample_docker.txt | sudo docker run -i basic_info
  ```
  
# About

* Develop usin Pycharm IDE
