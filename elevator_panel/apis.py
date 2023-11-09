from django.http import JsonResponse, HttpResponse
import time
from elevator_panel.models import Settings, Elevator, ElevatorJourney
from elevator_panel.helpers import (
    check_int,
    check_more_than_0,
    check_more_than_eq_to_0,
    check_floor_below_max,
    check_attr_set,
    find_closest_elevator,
    create_elevator_journey,
    get_elevator_journeys_df,
    find_journeys_by_el_and_to_f
)
from elevator_panel.globals import ELEVATOR_EXIT_ENTRY_TIME, TIME_BETWEEN_FLOORS


def request_elevator(request):
    try:
        settings = Settings.objects.all()[0]
    except:
        raise Exception(
            "you need to specify the settings first at 'elevator_panel/edit_settings?number_of_floors'"
        )
    fields = ["floor_on", "floor_to"]
    max_floor = settings.number_of_floors
    params = request.GET.dict()
    for field in fields:
        if field not in params:
            raise Exception(f"{field} is required")
        check_int(params[field], field)
        check_more_than_eq_to_0(int(params[field]), field)
        check_floor_below_max(int(params[field]), field, max_floor)
    floor_on = int(params["floor_on"])
    floor_to = int(params["floor_to"])
    if floor_on == floor_to:
        raise Exception(
            "You cannot request the lift to the floor you are already on")
    direction = "up" if floor_to > floor_on else "down"
    elevator = find_closest_elevator(floor_on, floor_to, direction)
    elevator.current_floor = floor_to
    elevator.save()
    # floor_change = 1 if direction == "up" else -1
    # add journey
    # current_journey = create_elevator_journey(elevator, floor_on, floor_to)
    # get the journey plan
    # journeys_df = get_elevator_journeys_df(elevator)
    # # create a loop that:
    # from_floors = list(journeys_df["floor_from"])
    # to_floors = list(journeys_df["floor_to"])
    # floor_lists = [from_floors, to_floors]
    # for floor_list in floor_lists:
    #     if direction == "up":
    #         floor_list.sort()
    #     else:
    #         floor_list.sort(reverse=True)
    # current_floor = elevator.current_floor
    # end_floor = to_floors[-1]
    # for i in floor_range:
    # checks that the journey is still the operating (most recent) journey and breaks the loop if not
    # journeys_df = get_elevator_journeys_df(elevator)
    # check DB to see if this is still the most recent and up to date journey
    # if journeys_df.iloc[0]["id"] != current_journey.pk:
    #     break
    # at each interval pauses if there are any stops
    # if i in from_floors or i in to_floors:
    # time.sleep(ELEVATOR_EXIT_ENTRY_TIME)
    # at each interval deletes completed journeys
    # if i in to_floors:
    #     find_journeys_by_el_and_to_f(elevator, i).delete()
    # time.sleep(TIME_BETWEEN_FLOORS)
    # at each interval updates the lift position

    return JsonResponse({"elevator_number": elevator.number, "direction": direction})


def elevator_statuses(request):
    elevators = Elevator.objects.all()
    elevator_info = list(elevators.values())
    return JsonResponse({"elevators": elevator_info})


def edit_settings(request):
    params = request.GET.dict()
    greater_than_0 = ["number_of_elevators",
                      "number_of_floors"]
    must_be_int = ["number_of_elevators",
                   "number_of_floors"]
    must_be_set = ["number_of_elevators",
                   "number_of_floors"]
    number_of_floors = int(
        params["number_of_floors"]) if "number_of_floors" in params else None
    number_of_elevators = int(
        params["number_of_elevators"]) if "number_of_elevators" in params else None
    try:
        settings = Settings.objects.all()[0]
    except:
        settings = Settings()
    [check_more_than_0(getattr(settings, setting), setting)
     for setting in greater_than_0]
    [check_int(getattr(settings, setting), setting) for setting in must_be_int]
    reset_response = False
    if ((number_of_floors != None and settings.number_of_floors != number_of_floors)
            or (number_of_elevators != None and number_of_elevators !=
                settings.number_of_elevators)
            ):
        Elevator.objects.all().delete()
        for i in range(number_of_elevators):
            elevator = Elevator()
            elevator.number = i+1
            elevator.save()
        reset_response = True
    if number_of_floors != None:
        settings.number_of_floors = number_of_floors
    if number_of_elevators != None:
        settings.number_of_elevators = number_of_elevators
    [check_attr_set(attr, settings) for attr in must_be_set]
    response = {"number_of_floors": settings.number_of_floors,
                "number_of_elevators": settings.number_of_elevators}
    if reset_response:
        response |= {
            "note": "You have reset the elevator locations and queued journeys, people are stranded and furious"
        }
    settings.save()

    return JsonResponse(response)
