def append_helper(initial_list, append_this):
    if type(initial_list) is not list:
        raise TypeError("initial_list must be a list")
    if type(append_this) == list:
        return initial_list + append_this
    else:
        initial_list.append(append_this)
        return initial_list
