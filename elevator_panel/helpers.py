from elevator_panel.models import Elevator, ElevatorJourney
import numpy as np
import pandas as pd


def check_int(item, item_name):
    try:
        if float(item).is_integer():
            return True
        else:
            raise Exception(f"{item_name} must be an integetr")
    except:
        raise Exception(f"{item_name} must be an integetr")


def check_more_than_0(item, item_name):
    if item > 0:
        return True
    else:
        raise Exception(f"{item_name} must be greater than 0")


def check_more_than_eq_to_0(item, item_name):
    if item >= 0:
        return True
    else:
        raise Exception(f"{item_name} must be greater than 0")


def check_floor_below_max(floor, input_name, max_floor):
    if floor > max_floor:
        raise Exception(
            f"{input_name} cannot go above the max floor in the settings: '{max_floor}'")


def check_attr_set(attr, model):
    if getattr(model, attr) == None:
        raise Exception(
            f"{attr} is not currently set please retry and ensure this value is set"
        )


def find_closest_elevator(floor_from, floor_to, direction):
    all_elevators_df = get_elevators_df()
    # remove elevators going away from the users
    # if direction == "up":
    #     filt_elevators_df = all_elevators_df[(all_elevators_df["direction"].isna()) |
    #                                          ((all_elevators_df["direction"] == "up") & (
    #                                              all_elevators_df["current_floor"] < floor_from))]
    # else:
    #     filt_elevators_df = all_elevators_df[(all_elevators_df["direction"].isna()) |
    #                                          ((all_elevators_df["direction"] == "down") & (
    #                                              all_elevators_df["current_floor"] > floor_from))]
    # if filt_elevators_df.empty:
    #     raise Exception(
    #         "All elevators are currently moving away from you, please try again shortly")
    # find the closest eligible elevator
    closest_elevator = all_elevators_df.iloc[(
        all_elevators_df['current_floor']-floor_from).abs().argsort()[:1]]
    closest_elevator_id = closest_elevator["number"].to_list()[0]
    return Elevator.objects.get(number=closest_elevator_id)


def find_closest(arr, floor):
    low = 0
    high = arr[-1].current_floor
    while low < high:
        if abs(arr[low].current_floor - floor) <= abs(arr[high].current_floor - floor):
            high -= 1
        else:
            low += 1
    return arr[low]


def check_elevator_direction(elevator):
    journeys = ElevatorJourney.objects.filter(elevator=elevator)
    if not journeys:
        return None
    first_journey = journeys[0]
    if first_journey.floor_from < first_journey.floor_to:
        return "up"
    else:
        return "down"


def get_elevators_df():
    elevators = Elevator.objects.all()
    elevators_df = pd.DataFrame(elevators.values())
    # journeys = ElevatorJourney.objects.all()
    # if journeys:
    #     journeys_df = pd.DataFrame(journeys.values())
    #     journeys_df = journeys_df.drop_duplicates("elevator_id")
    #     journeys_df["direction"] = journeys_df.apply(give_df_direction, axis=1)
    #     elevators_df = elevators_df.merge(
    #         journeys_df, how="left", left_on="number", right_on="elevator_id")
    # else:
    #     elevators_df["direction"] = np.NaN
    return elevators_df


def give_df_direction(df):
    if (pd.isna(df["floor_from"]) or df["floor_from"] == df["floor_to"]):
        return np.NaN
    elif df["floor_from"] < df["floor_to"]:
        return "up"
    else:
        return "down"


def create_elevator_journey(elevator, floor_from, floor_to):
    journey = ElevatorJourney()
    journey.elevator = elevator
    journey.floor_from = floor_from
    journey.floor_to = floor_to
    journey.save()
    return journey


def get_elevator_journeys_df(elevator):
    journeys = ElevatorJourney.objects.filter(elevator=elevator)
    journeys_df = pd.DataFrame(journeys.values())
    journeys_df = journeys_df.sort_values(by="created_on", ascending=False)
    return journeys_df


def find_journeys_by_el_and_to_f(elevator, to_floor):
    journeys = ElevatorJourney.objects.filter(
        elevator=elevator, floor_to=to_floor)
    return journeys
