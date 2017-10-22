
def read_filename2bait_csv(filename):
    temp_dict = {}
    with open(filename, 'rb') as file_open:
        for line in file_open:
            split_line = line.rstrip().split(',')
            temp_dict[split_line[0]] = split_line[1]
    return temp_dict

if __name__ == '__main__':
    filename_to_bait = read_filename2bait_csv('filename_to_baitname.csv')
    print filename_to_bait

