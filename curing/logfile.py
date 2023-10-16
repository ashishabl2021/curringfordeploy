def logdata(data):
    f = open('log.txt','+a')
    f.write(str(data)+"\n")
    f.close()
    return 