def hex_to_fixed_point(hex_value):
    decimal_value = int(hex_value, 16)
    if decimal_value & 0x8000:
        decimal_value = decimal_value - 65536
    integer_part = decimal_value >> 8  # Shift right by 8 bits
    fractional_part = decimal_value & 0xFF  # Mask the lower 8 bits
    fixed_point_value = float(integer_part) + float(fractional_part) / 256.0
    return fixed_point_value


def get_adv_type(adv, adv_len):  # finding type of adv packet
    # print(adv[10:14])
    if ((adv_len / 2) == 26) and adv[10:14] == "E1FF":
        return 1  # indicates the Accelerometer adv packets
    elif ((adv_len / 2) == 30) and adv[10:14] == "4C00":
        return 2  # indicates the ibeacon packet
    else:
        return 0  # indicates the neither the above packet


def get_mac_address(adv_data):  # extracting the mac_address from adv packet
    # print(adv_data)
    adv_data = adv_data[2:]
    adv_data_len = len(adv_data)
    # print(adv_data_len)
    ret_adv_type = get_adv_type(adv_data, adv_data_len)
    if ret_adv_type == 1:
        data = adv_data[40:]
        # print(data)
        mac_address = ":".join([data[i:i + 2] for i in range(0, len(data), 2)][::-1])
        return mac_address
    elif ret_adv_type == 2:
        return 2
    elif ret_adv_type == 0:
        return 0


def print_mac_address(adv_data):  # printing mac_address
    ret_code_macaddress = get_mac_address(x)
    if ret_code_macaddress == 0:
        print("parsed neither ibeacon packet or accelerometer packet")
    elif ret_code_macaddress == 2:
        print("no mac_address found because parsed adv packet belong to ibeacon")
    else:
        print(ret_code_macaddress)


def get_accelerometer_coordinates(raw_adv_data):  # getting x,y,z coordinates
    raw_adv_data = raw_adv_data[2:]
    raw_adv_data_len = len(raw_adv_data)
    ret_raw_adv_type = get_adv_type(raw_adv_data, raw_adv_data_len)
    if ret_raw_adv_type == 1:
        raw_data_x = raw_adv_data[28:32]
        raw_data_x = hex_to_fixed_point(raw_data_x)
        raw_data_y = raw_adv_data[32:36]
        raw_data_y = hex_to_fixed_point(raw_data_y)
        raw_data_z = raw_adv_data[36:40]
        raw_data_z = hex_to_fixed_point(raw_data_z)
        return [raw_data_x, raw_data_y, raw_data_z]
    else:
        print("invalid adv packet")


def get_accelerometer_status(adver_data):  # status of object
    l = get_accelerometer_coordinates(adver_data)
    if (abs(l[0]) == 0) and (abs(l[1]) == 0) and (abs[l[2]] == -1.0):
        return 0
    else:
        return 1


x = input("please enter the adv data")
print_mac_address(x)
status = get_accelerometer_status(x)
if status == 1:
    print("object is moving")
else:
    print("object is not moving ...")
