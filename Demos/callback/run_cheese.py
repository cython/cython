import cheese

def report_cheese(name):
    print("Found cheese: " + name.decode('utf-8'))

cheese.find(report_cheese)

