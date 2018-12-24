import numpy as np

def Ybus_construction(buses, branches, transformers):

    Y = np.zeros((len(buses),len(buses)),complex)

    ### Adding branches to Y_bus Matrix
    for branch in branches:
     
        y_series = 1 / complex(branch.r, branch.x)
        y_shunt = 1 / 2 * complex(branch.g, branch.b)

        Y = Ybus_add_series_element(Y, y_series, 
                                    branch.bus_index_1, 
                                    branch.bus_index_2)

        Y = Ybus_add_shunt_element(Y, y_shunt, 
                                   branch.bus_index_1)

        Y = Ybus_add_shunt_element(Y, y_shunt, 
                                   branch.bus_index_2)
            
    ### Adding transformers to Y_bus matrix
    for transformer in transformers:

        y12 = 1 / complex(transformer.r12,transformer.x12)
        
        Y = Ybus_add_series_element(Y, y12, 
                                    transformer.bus_index_1, 
                                    transformer.bus_index_2)

    return Y

def Ybus_add_series_element(Y, y_series, bus_index_1, bus_index_2):

    Y[bus_index_1, bus_index_1] += y_series
    Y[bus_index_2, bus_index_2] += y_series
    Y[bus_index_1, bus_index_2] += - y_series
    Y[bus_index_2, bus_index_1] += - y_series

    return Y

def Ybus_add_shunt_element(Y, y_shunt, bus_index):

    Y[bus_index, bus_index] += y_shunt

    return Y

def rows_to_up(array, rows_to_be_moved):

    up_indexes = rows_to_be_moved
    total_indexes = list(np.arange(0, array.shape[0] - 1))

    down_indexes = []

    for index in total_indexes:
        if index not in up_indexes:
            down_indexes.append(index)

    final_order = []

    for index in up_indexes:
        final_order.append(index)

    for index in down_indexes:
        final_order.append(index)

    array = array[final_order, :]

    return array

def columns_to_the_left(array, columns_to_be_moved):

    left_indexes = columns_to_be_moved
    total_indexes = list(np.arange(0, array.shape[0] - 1))

    right_indexes = []

    for index in total_indexes:
        if index not in left_indexes:
            right_indexes.append(index)

    final_order = []

    for index in left_indexes:
        final_order.append(index)

    for index in right_indexes:
        final_order.append(index)

    array = array[:, final_order]

    return array

def kron_reduction(Y, retained_indexes):

    Y = rows_to_up(Y, retained_indexes)
    Y = columns_to_the_left(Y, retained_indexes)

    stop_position = len(retained_indexes)

    Y_11 = Y[:stop_position, :stop_position]
    Y_12 = Y[:stop_position, stop_position:]
    Y_21 = Y[stop_position:, :stop_position]
    Y_22 = Y[stop_position:, stop_position:]

    Y_reduced = Y_11 - np.dot(np.dot(Y_12, np.linalg.inv(Y_22)), Y_21)

    return Y_reduced

def get_index(buses, bus_number_list):
    
    bus_index_list = [] 
    for bus_number in bus_number_list:
        if bus_number == 0:
            bus_index_list.append(-1)
            break
        for bus in buses:
            if bus_number == bus.number:
                bus_index_list.append(int(bus.index))
                break

    return bus_index_list

def get_branch_index(branches, bus_number_1, bus_number_2):
    
    founded_branch = False
    for branch in branches:
        if branch.bus_number_1 == bus_number_1 or \
            branch.bus_number_1 == bus_number_2:
            if branch.bus_number_2 == bus_number_1 or \
                branch.bus_number_2 == bus_number_2:
                    founded_branch = branch
                    break

    return founded_branch
