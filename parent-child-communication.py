import multiprocessing

# read the config file
filepath = 'config.txt'

# store the data points as a list entry
list_of_data_points = []

# loop through the list
with open(filepath) as fp:
   for cnt, line in enumerate(fp):

       # append list entry
       list_of_data_points.append(line)

# child function
def ack(data, q):

    # loop through the data sent by the parent
    # and send an ack if data is valid
    for i in data:

        # for this dummy application we loop through the queue and check if the point is valid
        if i == '1\n':

            # we send an ack
            q.put("Received data. Will move accordingly.")

if __name__ == "__main__":

    # create a multiprocessing queue
    q = multiprocessing.Queue()

    # start child process
    p = multiprocessing.Process(target=ack, args=(list_of_data_points, q))
    p.start()
    p.join

    # check child process
    while q:
        print(q.get())
