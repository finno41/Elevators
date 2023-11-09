# Elevator Control Panel

This project acts as an elevator control panel

## Getting started
Navigate to the main folder and run the following commands in your command line:
- source venv/bin/activate
- python3 manage.py runserver

### Edit settings
This API allows you to change the number of elevators and floors in the settings
- API URL: /elevator_panel/edit_settings
- Params:
  - number_of_elevators
  - number_of_floors
- Note: Editing settings will reset all lift positions to 0 and cancel any current journeys/ requests

### Request Elevator
This API will tell you which lift you need to take to get to your requested floor,
simply input the params below
- API URL: /elevator_panel/request_elevator
- Params:
  - floor_on
  - floor_to

### Elevator Statuses
This API allows you to see where the elevators currently are:
- API URL: /elevator_panel/elevator_statuses
