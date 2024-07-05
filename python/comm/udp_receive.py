import socket
import struct
import csv

UDP_IP = "127.0.0.1"
UDP_PORT = 20001
BATCH_SIZE = 10

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

# Define the format string
# 'I' = unsigned int (4 bytes)
# 'd' = double (8 bytes)
format_string = '<IdddddIddd'

columns = [
        "rownum",
        "robotDevID",
        "AlphaDegrees",
        "BetaDegrees",
        "Time",
        "zHeight",
        "AbsoluteAngleL1",
        "AbsoluteAngleL2",
        "AbsoluteAngleL3",
        "AbsoluteAngleL4",
        "Arm1.waferStatus",
    ]

i = 0
j = 0
while j < 10:
    # open a data file
    filename = 'train_data_1M.' + str(j) + '.csv'
    file = open(filename, 'w', newline='')

    writer = csv.writer(file)
    writer.writerow(columns)

    while i < 100000:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

        # First byte indicates the type of the message. 0x01 is robot angle data 
        if data[0] != 0x01: continue

        # Unpack the binary message
        # struct.unpack returns a tuple of the unpacked values
        unpacked_data = struct.unpack(format_string, data[1:])

        # Extract the individual variables
        devId, zHeight, angle1, angle2, angle3, angle4, waf_status, alpha, beta, rdtsc = unpacked_data

        if devId == 100:

            data_row = [i, devId, alpha, beta, rdtsc, zHeight, angle1, angle2, angle3, angle4, waf_status]
            writer.writerow(data_row)

            # labels = [1, 0]
            # LABEL = (
            #     1
            #     if labels[0] == 1
            #     else (0 if labels[0] == -1 else -1)
            # )

            # LABEL = (
            #     "INLIER"
            #     if labels[0] == 1
            #     else ("OUTLIER" if labels[0] == -1 else "Unknown_type")
            # )

            # Print the unpacked variables
            # MESSAGE = "devId:%d" % devId + ",zHeight:%.2f" % zHeight + ",angle1:%.2f" % angle1 + ",angle2:%.2f" % angle2 + \
                    #   ",angle3:%.2f" % angle3 + ",angle4:%.2f" % angle4 + ",alpha:%.2f" % alpha + ",beta:%.2f" % beta + \
                    #   ",wafStatus:%d" % waf_status + ",rdtsc:%.0f" % rdtsc   

            # print(MESSAGE)
            # Print the unpacked variables
            # print('devId:', devId, ' zHeight:%.2f' % zHeight, ' angle1:%.2f' % angle1, ' angle2:%.2f' %angle2, ' angle3:%.2f' % angle3, ' angle4:%.2f' % angle4, ' wafStatus:',  waf_status, ' alpha:%.2f' % alpha, ' beta:%.2f' % beta, ' rdtsc:%.2f' % rdtsc)


            # data_for_predict = [devId, zHeight, angle1, angle2, angle3, angle4, waf_status]
            # print(data_for_predict)

            i = i + 1

    file.close()
    j = j + 1
    i = 0