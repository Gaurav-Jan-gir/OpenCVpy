import cv2 as cv

def check_attr(prop_id, cap, value):
    default_value = cap.get(prop_id)
    cap.set(prop_id, value)
    current_value = cap.get(prop_id)
    cap.set(prop_id, default_value)
    return abs(current_value - value) < 1e-3

def get_min_val(prop_id, upper_bound, cap):
    if not check_attr(prop_id, cap, upper_bound):
        return None
    step = 1
    while check_attr(prop_id, cap, upper_bound - step):
        upper_bound -= step
        step *= 2
    step //= 2
    while step >= 1:
        if check_attr(prop_id, cap, upper_bound - step):
            upper_bound -= step
        step //= 2
    return upper_bound

def get_max_val(prop_id, lower_bound, cap):
    if not check_attr(prop_id, cap, lower_bound):
        return None
    step = 1
    while check_attr(prop_id, cap, lower_bound + step):
        lower_bound += step
        step *= 2
    step //= 2
    while step >= 1:
        if check_attr(prop_id, cap, lower_bound + step):
            lower_bound += step
        step //= 2
    return lower_bound

def get_range(prop_id, cap):
    default = cap.get(prop_id)
    if not cap.isOpened():
        return (default, default)

    min_val = max_val = None

    if default <= -1:
        min_val = get_min_val(prop_id, default, cap)
        max_val = get_max_val(prop_id, 1, cap)
        if max_val is None:
            max_val = 0 if check_attr(prop_id, cap, 0) else -1

    elif default <= 0:
        min_val = get_min_val(prop_id, -1, cap)
        max_val = get_max_val(prop_id, 1, cap)
        if min_val is None and check_attr(prop_id, cap, 0):
            min_val = 0
        if max_val is None and check_attr(prop_id, cap, 0):
            max_val = 0

    elif default <= 1:
        min_val = get_min_val(prop_id, -1, cap)
        if min_val is None:
            min_val = 0 if check_attr(prop_id, cap, 0) else 1
        max_val = get_max_val(prop_id, 1, cap)

    else:
        min_val = get_min_val(prop_id, -1, cap)
        if min_val is None:
            min_val = 0 if check_attr(prop_id, cap, 0) else 1
        max_val = get_max_val(prop_id, 1, cap)

    return (min_val or default, max_val or default)


