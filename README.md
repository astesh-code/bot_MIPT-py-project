# Overview
**Edu_bot** is a telegram bot which can help you to track status on `russia-edu.minobrnauki.gov.ru` - service for foreign students enrolling to russia universities
#
# Features
 - Saving data for multiple checking
 - Interfaces completely based on keyboards, excluding form data input
 - Reading API-key from environment
 - Logging
 - Docker image
 #
# Requirements
 - Python 3.6 and above;
 #
# Docker image
`hub.docker.com/repository/docker/astesh/edu_bot`
#
# How to start
### Just from local machine
```
$ export API_KEY=<your_key>
$ python bot.py
```
### From docker image
```
$ docker run -e API_KEY=<your_key> edu_bot
```
#

