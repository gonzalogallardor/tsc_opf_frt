from .construction_module import get_index

class Bus:

    def __init__(self, bus_index,
                 bus_number,
                 bus_name,
                 nominal_voltage,
                 bus_type,
                 voltage_mag,
                 voltage_angle):

        self.index = int(bus_index)
        self.number = int(bus_number)
        self.name = bus_name
        self.nominal_voltage = float(nominal_voltage)
        self.type = int(bus_type)
        self.voltage_mag = float(voltage_mag)
        self.voltage_angle = float(voltage_angle)

class Load:
    
    def __init__(self,buses,
                 bus_number,
                 p,
                 q):

        self.bus_number = int(bus_number)
        [bus_index] = get_index(buses, [int(bus_number)])
        self.bus_index = int(bus_index)
        self.p = float(p)
        self.q = float(q)

class Generator:

    def __init__(self, buses,
                 bus_number,
                 gen_id,
                 p,
                 q,
                 mva_base,
                 r_tran,
                 x_tran,
                 p_max,
                 p_min,
                 q_max,
                 q_min,
                 internal_bus_index):

        self.bus_number = int(bus_number)
        self.id = gen_id
        self.p = float(p)
        self.q = float(q)
        self.mva_base = float(mva_base)
        self.r_tran = float(r_tran)
        self.x_tran = float(x_tran)
        self.p_max = float(p_max)
        self.p_min = float(p_min)
        self.q_max = float(q_max)
        self.q_min = float(q_min)
        [bus_index] = get_index(buses, [int(bus_number)])
        self.bus_index = int(bus_index)
        self.internal_bus_index = int(internal_bus_index)

class Branch:

    def __init__(self, buses,
                 bus_number_1,
                 bus_number_2,
                 branch_id,
                 r,
                 x,
                 g,
                 b,
                 mva_rate_1):

        self.bus_number_1 = int(bus_number_1)
        self.bus_number_2 = int(bus_number_2)
        [bus_index_1, bus_index_2] = get_index(buses,
                                               [int(bus_number_1),
                                                int(bus_number_2)])
        self.bus_index_1 = int(bus_index_1)
        self.bus_index_2 = int(bus_index_2)
        self.id = int(branch_id)
        self.r = float(r)
        self.x = float(x)
        self.g = float(g)
        self.b = float(b)
        self.mva_rate_1 = float(mva_rate_1)

class Transformer:

    def __init__(self, buses,
                 bus_number_1,
                 bus_number_2,
                 transf_id,
                 r12,
                 x12,
                 bus_number_3 = 0,
                 r13 = 0,
                 x13 = 0,
                 r23 = 0,
                 x23 = 0):

        self.bus_number_1 = int(bus_number_1)
        self.bus_number_2 = int(bus_number_2)
        self.bus_number_3 = int(bus_number_3)
        [bus_index_1, bus_index_2 , bus_index_3] = get_index(buses,
                                                             [int(bus_number_1),
                                                              int(bus_number_2),
                                                              int(bus_number_3)])
        self.bus_index_1 = int(bus_index_1)
        self.bus_index_2 = int(bus_index_2)
        self.bus_index_3 = int(bus_index_3)
        self.id = transf_id
        self.r12 = float(r12)
        self.x12 = float(x12)
        self.r13 = float(r13)
        self.x13 = float(x13)
        self.r23 = float(r23)
        self.x23 = float(x23)