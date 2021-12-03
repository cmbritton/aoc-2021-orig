def main(diagnostics):
    with open('diagnostics.data', 'r') as data_file:
        line = data_file.readline()
        while line:
            value = line.strip()
            diagnostics.accumulate(value=value)
            line = data_file.readline()
    print("gamma: {}".format(diagnostics.power.power()))
