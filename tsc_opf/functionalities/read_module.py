import numpy as np
import csv
from functionalities.system_classes import *
from functionalities.construction_module import *

def read_raw_data(data_path):
    rawfile = open(data_path,'r')

    ### Comments
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    s_base = float(words[1])
    comments = [rawfile.readline(),rawfile.readline()]

    ### Bus data
    buses = []
    node_counter = 0
    while 1:
        line = rawfile.readline()
        if '/' in line: line = line[:line.find('/')]
        words = line.split(',')
        if len(words) == 1 and int(words[0]) == 0: break

        bus_instance = Bus(node_counter,
                           words[0],
                           words[1][1:-1],
                           words[2],
                           words[3],
                           words[7],
                           words[8])

        buses.append(bus_instance)
        node_counter += 1

    ### Load data
    loads = []
    while 1:
        line = rawfile.readline()
        if '/' in line: line = line[:line.find('/')]
        words = line.split(',')
        if len(words) == 1 and int(words[0]) == 0: break

        load_instance = Load(buses,
                             words[0],
                             words[5],
                             words[6])

        loads.append(load_instance)

    ### Not usefull data
    while 1:
        line = rawfile.readline()
        if '/' in line: line = line[:line.find('/')]
        words = line.split(',')
        if len(words) == 1 and int(words[0]) == 0: break

    ### Generators
    generators = []
    while 1:
        line = rawfile.readline()
        if '/' in line: line = line[:line.find('/')]
        words = line.split(',')
        if len(words) == 1 and int(words[0]) == 0: break

        generator_instance = Generator(buses,
                                       words[0],
                                       words[1][1:-1],
                                       words[2],
                                       words[3],
                                       words[8],
                                       words[9],
                                       words[10],
                                       words[16],
                                       words[17],
                                       words[4],
                                       words[5],
                                       node_counter)

        node_counter += 1  # Assign new bus_index to internal generator bus (fictious)

        generators.append(generator_instance)

    ### Branches
    branches = []
    while 1:
        line = rawfile.readline()
        if '/' in line: line = line[:line.find('/')]
        words = line.split(',')
        if len(words) == 1 and int(words[0]) == 0: break

        branch_instance = Branch(buses,           # buses
                                 words[0],        # bus_number_1
                                 words[1],        # bus_number_2
                                 words[2][1:-1],  # branch_id
                                 words[3],        # r (series)
                                 words[4],        # x (series)
                                 0,               # g (shunt)
                                 words[5],        # b (shunt)
                                 words[6])         # mva_rate_1 (MVA)

        branches.append(branch_instance)

    ### Transformers
    transformers = []
    while 1:
        line = rawfile.readline()
        if '/' in line: line = line[:line.find('/')]
        words = line.split(',')

        if len(words) == 1 and int(words[0]) == 0: break

        while len(words) < 36:
            line=rawfile.readline()
            words.extend(line.split(','))

        transformer_instance = Transformer(buses,
                                           words[0],
                                           words[1],
                                           words[3][1:-1],
                                           words[14],
                                           words[15],
                                           words[2],
                                           0,0,0,0)

        transformers.append(transformer_instance)
    rawfile.close()

    return s_base, buses, loads, generators, branches, transformers

def read_hvdc_param(data_path):
    csv_file = open(data_path,'r')
    csv_file = csv.reader(csv_file)
    csv_list = list(csv_file)

    headers = [('bus_number', 'i'),
               ('P_l', 'f8'),
               ('P_lo', 'f8'),
               ('P_up', 'f8'),
               ('Q_l', 'f8'),
               ('Q_lo', 'f8'),
               ('Q_up', 'f8'),
               ('a_1', 'f8'),
               ('hvdc_pf_interval_1', 'f8'),
               ('hvdc_pf_interval_2', 'f8'),
               ('hvdc_pf_interval_3', 'f8')]
    
    new_csv_list = []
    for row in csv_list[1:]:
        new_row = []
        for column in range(0, len(row)): 
            new_row.append(float(row[column]))
        new_csv_list.append(tuple(new_row))

    csv_array = np.array(new_csv_list, dtype = headers)
    
    return csv_array

def read_opf_param(data_path):
    csv_file = open(data_path,'r')
    csv_file = csv.reader(csv_file)
    csv_list = list(csv_file)

    headers = [('slack_bus', 'i'),
               ('v_ini', 'f8'),
               ('v_min', 'f8'),
               ('v_max', 'f8')]

    new_csv_column = []
    for row in csv_list:
        new_csv_column.append(float(row[1]))

    csv_array = np.array(tuple(new_csv_column), dtype = headers)
    
    return csv_array

def read_tsc_param(data_path):
    csv_file = open(data_path,'r')
    csv_file = csv.reader(csv_file)
    csv_list = list(csv_file)

    headers = [('total_time', 'f8'),
               ('delta_t', 'f8'),
               ('clearing_time', 'f8'),
               ('faulted_bus', 'i'),
               ('isolated_branch_bus1', 'i'),
               ('isolated_branch_bus2', 'i'),
               ('Sm/Pmax', 'f8')]
    
    new_csv_column = []
    for row in csv_list: 
        new_csv_column.append(float(row[1]))

    csv_array = np.array(tuple(new_csv_column), dtype = headers)
    
    return csv_array

def read_dfig_param(data_path):
    csv_file = open(data_path,'r')
    csv_file = csv.reader(csv_file)
    csv_list = list(csv_file)

    headers = [('N_gen','i'),
               ('bus_number','i'),
               ('Sb','f8'),
               ('a_1','f8'),
               ('Pg','f8'),
               ('Qg','f8'),
               ('Dt','f8'),
               ('Kq','f8')]
    
    new_csv_column = []
    for row in csv_list: 
        new_csv_column.append(float(row[1]))

    csv_array = np.array(tuple(new_csv_column), dtype = headers)
    
    return csv_array

def add_gen_parameters(data_path, generators):
    csv_file = open(data_path,'r')
    csv_file = csv.reader(csv_file)
    csv_list = list(csv_file)

    new_attributes = ['bus_number', # int
                      'a_1',        # $/MW
                      'P_max',      # MW
                      'P_min',      # MW
                      'Q_min',      # Mvar
                      'Q_max',      # Mvar
                      'Sm',         # -
                      'e_fd_max',   # Field voltage max limit, pu
                      'e_fd_min',   # Field voltage max limit, pu
                      'ra',         # Armature resistance, pu
                      'xd',         # Steady-state direct-axis reactance, pu
                      'xd_p',       # Transient state quadrature-axis reactanse, pu
                      'xq',         # Steady-state direct-axis reactance, pu
                      'xq_p',       # Transient state quadrature-axis reactanse, pu
                      'H',          # Inertia [s]
                      'D',          # Damping factor
                      'Td_p',       # Direct-axis transient state time constant[s]
                      'Tq_p',       # Quadrature-axis transient state time constant[s]
                      'P_ini',      # Initial value of real input power [MW] (gams)
                      'Q_ini']      # Initial value of imaginary input VA [Mvar] (gams)

    for row in range(1, len(csv_list)):
        row_values = csv_list[row]
        for generator in generators:
            if int(row_values[0]) == generator.bus_number:
                column = 1
                for new_attribute in new_attributes[1:]:
                    setattr(generator, new_attribute, float(row_values[column]))
                    column += 1
                break