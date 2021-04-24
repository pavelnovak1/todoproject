# To Do list project
This project is a simple To Do list, that provides methods for adding, editing, managing and removing jobs that must be done in the future. This app has two interfaces. 
First one is an interactive mode from the command line. The second is web interface using Flask framework. 

This project is only partialy done and some functionality is not implemented yet. 

# Prerequisites:
python > 3.7

Flask framework

# How to use:
```python main.py -w``` for web mode. To do list is available, by default, on localhost - port 5000.

```python main.py -c <username> <password>``` for interactive mode.

For both modes: If no user with the given name exists, the new one is created.
