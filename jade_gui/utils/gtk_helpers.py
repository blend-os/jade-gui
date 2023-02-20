def set_list_text(list, string):
    n = list.get_n_items()
    if n > 0:
        list.splice(0, n, [string])
    else:
        list.append(string)
