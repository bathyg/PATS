import glob, os
import matplotlib.pyplot as plot
from matplotlib.colors import ListedColormap
import types
import matplotlib
import parameters
import multiprocessing


def check_dir_exist(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return 0

def read_file_from(filename):
    corr_array = []
    corr_num_array = []
    with open(filename) as file1:
        for line in file1:
            corr_array.append(line.strip().split(','))
    for each_line in corr_array[1:]:
        temp_array = [float(i) for i in each_line[1:]]
        corr_num_array.append(temp_array)
    return [i for i in corr_array[0][1:]], corr_num_array


def plot_each_file(each_chunk):
    C = [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1], [4, 0, 1], [5, 0, 1], [6, 0, 1], [7, 0, 1], [8, 0, 1], [9, 0, 1], [9, 0, 1], [10, 0, 1], [11, 0, 1], [12, 0, 1],
         [13, 0, 1], [14, 0, 1], [15, 0, 1], [16, 0, 1], [17, 0, 1], [18, 0, 1], [19, 0, 1], [20, 0, 1], [21, 0, 1], [22, 0, 0], [23, 0, 0], [24, 0, 0], [25, 0, 0],
         [26, 0, 0], [26, 0, 0], [27, 0, 0], [28, 0, 0], [29, 0, 0], [30, 0, 0], [31, 0, 0], [32, 0, 0], [33, 0, 0], [34, 0, 0], [35, 0, 0], [36, 0, 0], [37, 0, 0],
         [38, 0, 0], [39, 0, 0], [40, 0, 0], [41, 0, 0], [42, 0, 0], [43, 0, 0], [43, 0, 0], [44, 0, 0], [45, 0, 0], [46, 0, 0], [47, 0, 0], [48, 0, 0], [49, 0, 0],
         [50, 0, 0], [51, 0, 0], [52, 0, 0], [53, 0, 0], [54, 0, 0], [55, 0, 0], [56, 0, 0], [57, 0, 0], [58, 0, 0], [59, 0, 0], [60, 0, 0], [61, 0, 0], [62, 0, 1],
         [63, 0, 2], [64, 0, 3], [65, 0, 4], [66, 0, 5], [67, 0, 6], [68, 0, 7], [69, 0, 7], [70, 0, 8], [71, 0, 9], [72, 0, 10], [73, 0, 11], [74, 0, 12], [75, 0, 13],
         [76, 0, 14], [77, 0, 15], [78, 0, 16], [79, 0, 17], [80, 0, 17], [81, 0, 18], [82, 0, 19], [83, 0, 20], [84, 0, 21], [85, 0, 22], [86, 0, 23], [87, 0, 24],
         [88, 0, 25], [89, 0, 26], [90, 0, 27], [91, 0, 28], [92, 0, 28], [94, 0, 29], [95, 0, 30], [96, 0, 31], [97, 0, 32], [98, 0, 33], [99, 0, 34], [100, 0, 35],
         [101, 0, 36], [102, 0, 37], [103, 0, 37], [104, 0, 38], [105, 0, 39], [106, 0, 40], [107, 0, 41], [108, 0, 42], [109, 0, 43], [110, 0, 44], [111, 0, 45],
         [112, 0, 46], [113, 0, 47], [114, 0, 48], [115, 0, 48], [116, 0, 49], [117, 0, 50], [118, 0, 51], [119, 0, 52], [120, 0, 53], [121, 0, 54], [122, 0, 55],
         [123, 0, 56], [124, 0, 57], [125, 0, 57], [126, 0, 58], [127, 0, 58], [128, 0, 58], [129, 0, 58], [130, 0, 58], [131, 0, 58], [132, 0, 58], [133, 0, 58],
         [135, 0, 58], [136, 0, 58], [137, 0, 58], [138, 0, 58], [139, 0, 58], [140, 0, 58], [141, 0, 58], [142, 0, 59], [143, 0, 59], [144, 0, 59], [145, 0, 59],
         [146, 0, 59], [147, 0, 59], [148, 0, 59], [149, 0, 59], [150, 0, 59], [151, 0, 59], [152, 0, 59], [153, 0, 59], [154, 0, 59], [155, 0, 59], [156, 0, 59],
         [157, 0, 59], [158, 0, 59], [159, 0, 59], [160, 0, 59], [161, 0, 59], [162, 0, 59], [163, 0, 59], [164, 0, 59], [165, 0, 59], [166, 0, 59], [167, 0, 59],
         [168, 0, 59], [169, 0, 59], [170, 0, 60], [171, 0, 60], [172, 0, 60], [173, 0, 60], [174, 0, 60], [175, 0, 60], [176, 0, 60], [177, 0, 60], [178, 0, 60],
         [179, 0, 60], [180, 0, 60], [181, 0, 60], [182, 0, 60], [183, 0, 60], [184, 0, 60], [185, 0, 60], [186, 0, 60], [187, 0, 60], [188, 0, 60], [189, 0, 60],
         [190, 0, 60], [191, 0, 60], [192, 0, 59], [193, 0, 58], [194, 0, 57], [195, 0, 56], [196, 0, 55], [197, 0, 54], [198, 0, 53], [199, 0, 52], [200, 0, 51],
         [201, 0, 50], [202, 0, 49], [203, 0, 48], [204, 0, 47], [205, 0, 46], [206, 0, 45], [207, 0, 44], [208, 0, 43], [209, 0, 43], [210, 0, 42], [211, 0, 41],
         [213, 0, 40], [214, 0, 39], [215, 0, 38], [216, 0, 37], [217, 0, 36], [218, 0, 35], [219, 0, 34], [220, 0, 33], [221, 0, 32], [222, 0, 31], [223, 0, 30],
         [224, 0, 29], [225, 0, 28], [226, 0, 27], [227, 0, 26], [228, 0, 26], [229, 0, 25], [230, 0, 24], [231, 0, 23], [232, 0, 22], [233, 0, 21], [234, 0, 20],
         [235, 0, 19], [236, 0, 18], [237, 0, 17], [238, 0, 16], [239, 0, 15], [240, 0, 14], [241, 0, 13], [242, 0, 12], [243, 0, 11], [244, 0, 10], [245, 0, 9],
         [247, 0, 9], [248, 0, 8], [249, 0, 7], [250, 0, 6], [251, 0, 5], [252, 0, 4], [253, 0, 3], [254, 0, 2], [255, 0, 1], [255, 0, 0]]
    C1 = [[i[0] / 255.0, i[1] / 255.0, i[2] / 255.0] for i in C]
    for each in each_chunk:
        setdpi = 150
        cmap_new = ListedColormap(C1)
        protein_list, number_list = read_file_from(each)
        fontsize = 12
        if len(protein_list) > 10:
            fontsize = 12 - (len(protein_list) + 20) / 10
            setdpi += len(protein_list) * 2
        if fontsize < 2:
            fontsize = 2
        protein_list_x = [i.ljust(8) for i in protein_list]
        # plot.text(0, 0, each, fontsize=12)
        norm1 = matplotlib.colors.Normalize(vmin=0., vmax=1.)
        fig, ax = plot.subplots()
        heatmap = ax.pcolor(number_list, norm=norm1, cmap=cmap_new)
        cbar = plot.colorbar(heatmap)
        cbar.ax.get_yaxis().set_ticks([])
        cbar.ax.get_yaxis().labelpad = 15
        cbar.ax.set_ylabel('STRING score', rotation=270)
        plot.locator_params(axis='y', nbins=len(protein_list))
        plot.locator_params(axis='x', nbins=len(protein_list))
        ax.set_xticklabels(protein_list_x, minor=False, rotation=45)
        ax.set_yticklabels(protein_list, minor=False)
        ax.xaxis.tick_top()
        plot.gca().invert_yaxis()
        SHIFT = -1.  # Data coordinates
        if len(protein_list) > 8:
            x_shift = -1
        elif len(protein_list) > 16:
            x_shift = -2
        else:
            x_shift = -0.5
        for label in ax.xaxis.get_majorticklabels():
            label.set_fontsize(fontsize)
            label.customShiftValue = x_shift
            label.set_x = types.MethodType(lambda self, x: matplotlib.text.Text.set_x(self, x - self.customShiftValue),
                                           label, matplotlib.text.Text)
        for label in ax.yaxis.get_majorticklabels():
            label.set_fontsize(fontsize)
            label.customShiftValue = -0.5
            label.set_y = types.MethodType(lambda self, y: matplotlib.text.Text.set_y(self, y - self.customShiftValue),
                                           label, matplotlib.text.Text)

        plot.tight_layout()
        name = each.replace('.csv', '') + '.png'
        out_name = os.path.join(parameters.plot_dir, os.path.basename(name))
        plot.savefig(out_name, dpi=setdpi)
        plot.close()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def step_5_csv_to_graph(sort_output_dir, plot_dir):
    filename = []
    os.chdir(sort_output_dir)
    for csv_file in glob.glob("*.csv"):
        if not csv_file.startswith('0.0_'):
            filename.append(csv_file)
    check_dir_exist(plot_dir)
    file_chunks = chunks(filename, 100)
    pool = multiprocessing.Pool(processes=parameters.maximum_thread_number)
    pool.map(plot_each_file, file_chunks)
    pool.close()
    pool.join()


if __name__ == "__main__":
    step_5_csv_to_graph(parameters.sorted_csv_dir, parameters.plot_dir)
