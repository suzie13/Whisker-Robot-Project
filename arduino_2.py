import serial
# ser = serial.Serial('/dev/ttyACM0', BAUD_RATE)

port = '/dev/ttyACM0'
baud = 9600

serial_port = serial.Serial(port, baud, timeout=1)

# while True:

#    serial_port.write(b'1') 

#    reading = serial_port.readline().decode()

#    if reading != '':
#          print(reading)
while True:
    serial_port.write(b'1') 

    reading = serial_port.readline().decode()

    if reading != '':
            print(reading)

    serial_port.write(b'2 200 200') 

    reading = serial_port.readline().decode()

    if reading != '':
            print(reading)

# int i = 0

serial_port.write(b'1') 

reading = serial_port.readline().decode()

if reading != '':
        print(reading)

serial_port.write(b'2 200 200') 

reading = serial_port.readline().decode()

if reading != '':
        print(reading)




while True:
    # if 
    serial_port.write(b'1') 

    reading = serial_port.readline().decode()

    if reading != '':
            print(reading)
    break

    # if True:

serial_port.flush()
while True:
    serial_port.write(b'2 200 200') 

    reading = serial_port.readline().decode()

    if reading != '':
            print(reading)
    serial_port.flush()

    break

##################################################

# while True:
#     serial_port.write(b'2 200 200') 

#     reading = serial_port.readline().decode()

#     if reading != '':
#             print(reading)
#     break
# if True:
#     serial_port.write(b'2 200 200') 

#     reading = serial_port.readline().decode()

#     if reading != '':
            # print(reading)
    # break
#######################
# ser.flush()
# ser.flushInput()
# ser.flushOutput()