import RPi.GPIO as io
import time
io.setmode(io.BOARD)
io.setwarnings(False)

x_axis=19
y_axis=21
z_axis=29

io.setup(x_axis,io.IN)
io.setup(y_axis,io.IN)
io.setup(z_axis,io.IN)


try:
     while True:
        x=io.input(x_axis)
        print("x:axis "+str(x))
        time.sleep(1)
        y=io.input(y_axis)
        print("y:axis "+str(y))
        time.sleep(1)
        z=io.input(z_axis)
        print("z:axis "+str(z))
        time.sleep(1)                    
except KeyboardInterrupt:
    print("Received Interupt")
