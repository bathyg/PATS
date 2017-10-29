import glob, os
import networkx as nx
import matplotlib.pyplot as plt
import cPickle as pickle
import parameters
import multiprocessing
import operator


def check_dir_exist(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return 0

def write_cytojs(G, file_output):
    description = pickle.load(open(parameters.description_file, 'rb'))
    uniprot_bait_count_dict = pickle.load(open(parameters.uniprot_bait_count_dict, "rb"))

    uniprot_name = file_output.split('_')[-1].split('.js')[0]
    size_normalizer = 0.07 / float(max(uniprot_bait_count_dict[uniprot_name].iteritems(), key=operator.itemgetter(1))[1])

    protein_list = G.node.keys()
    node_dict = {}
    edges_dict = {}

    for each in protein_list:
        try:
            node_size = uniprot_bait_count_dict[uniprot_name][each] * size_normalizer
        except:
            node_size = 0.01
            print uniprot_name, each
        node_dict[each] = (protein_list.index(each), each, node_size, G.node[each]['X'], G.node[each]['Y'])  # id,gene,score,x, y)
    edge_list = G.edge.keys()
    for each in edge_list:
        if len(G.edge[each].keys()) > 0:
            for each_key in G.edge[each].keys():
                target = each_key
                try:
                    edges_dict[each].append([node_dict[each][0], node_dict[node_dict[target][1]][0],
                                             G.edge[each][target]['weight']])
                except:
                    edges_dict[each] = []
                    edges_dict[each].append([node_dict[each][0], node_dict[node_dict[target][1]][0],
                                             G.edge[each][target]['weight']])  # source, target, weight
        else:
            edges_dict[each] = []
    file_output = os.path.join(parameters.network_dir, file_output)
    with open(file_output, 'wb') as file1:
        lines = []
        file1.write(
            'var cy;\n\n$(function(){ // on dom ready\n\n  cy = cytoscape({\n    container: document.getElementById(\'cy\'),\n\n    style: [{"selector":"core","style":{"selection-box-color":"#AAD8FF","selection-box-border-color":"#8BB0D0","selection-box-opacity":"0.5"}},{"selector":"node","style":{"width":"mapData(score, 0, 0.006769776522008331, 20, 60)","height":"mapData(score, 0, 0.006769776522008331, 20, 60)","content":"data(name)","font-size":"12px","text-valign":"center","text-halign":"center","background-color":"#555","text-outline-color":"#000","text-outline-width":"0.5px","color":"#fff","overlay-padding":"6px","z-index":"10"}},{"selector":"node[?attr]","style":{"shape":"rectangle","background-color":"#aaa","text-outline-color":"#aaa","width":"16px","height":"16px","font-size":"6px","z-index":"1"}},{"selector":"node[?query]","style":{"background-clip":"none","background-fit":"contain"}},{"selector":"node:selected","style":{"border-width":"6px","border-color":"#AAD8FF","border-opacity":"0.5","background-color":"#77828C","text-outline-color":"#77828C"}},{"selector":"edge","style":{"curve-style":"haystack","haystack-radius":"0.5","opacity":"0.4","line-color":"#bbb","width":"mapData(weight, 0, 1, 1, 8)","overlay-padding":"3px"}},{"selector":"node.unhighlighted","style":{"opacity":"0.2"}},{"selector":"edge.unhighlighted","style":{"opacity":"0.05"}},{"selector":".highlighted","style":{"z-index":"999999"}},{"selector":"node.highlighted","style":{"border-width":"6px","border-color":"#AAD8FF","border-opacity":"0.5","background-color":"#394855","text-outline-color":"#394855","shadow-blur":"12px","shadow-color":"#000","shadow-opacity":"0.8","shadow-offset-x":"0px","shadow-offset-y":"4px"}},{"selector":"edge.filtered","style":{"opacity":"0"}},{"selector":"edge[group=\\"coexp\\"]","style":{"line-color":"#d0b7d5"}},{"selector":"edge[group=\\"coloc\\"]","style":{"line-color":"#a0b3dc"}},{"selector":"edge[group=\\"gi\\"]","style":{"line-color":"#90e190"}},{"selector":"edge[group=\\"path\\"]","style":{"line-color":"#9bd8de"}},{"selector":"edge[group=\\"pi\\"]","style":{"line-color":"#eaa2a2"}},{"selector":"edge[group=\\"predict\\"]","style":{"line-color":"#f6c384"}},{"selector":"edge[group=\\"spd\\"]","style":{"line-color":"#dad4a2"}},{"selector":"edge[group=\\"spd_attr\\"]","style":{"line-color":"#D0D0D0"}},{"selector":"edge[group=\\"reg\\"]","style":{"line-color":"#D0D0D0"}},{"selector":"edge[group=\\"reg_attr\\"]","style":{"line-color":"#D0D0D0"}},{"selector":"edge[group=\\"user\\"]","style":{"line-color":"#f0ec86"}}],\n\n    elements: [\n')
        for key in node_dict:
            temp = node_dict[key]
            color = '008AFF'

            line = '{"data":{"id":"%d","idInt":%d,"name":"%s","score":%f,"query":true,"gene":true},' \
                   '"position":{"x":%s,"y":%s},"group":"nodes","removed":false,"selected":false,"selectable":true,"locked":false,"grabbed":false,"grabbable":true,"classes":"",' \
                   '"style": {"background-color": "#%s"}}' % (
                       temp[0], temp[0], temp[1], temp[2], temp[3], temp[4], color)
            lines.append(line)
        for key in edges_dict:
            if len(edges_dict[key]) > 0:
                temp = edges_dict[key][0]
                if temp[0] > temp[1]:
                    line = '{"data":{"source":"%d","target":"%d","weight":%s,"group":"spd","networkId":1,"networkGroupId":2,"intn":true},"position":{},"group":"edges","removed":false,"selected":false,"selectable":true,"locked":false,"grabbed":false,"grabbable":true,"classes":""}' % (
                        temp[0], temp[1], temp[2])
                    lines.append(line)
        file1.write(','.join(lines))
        file1.write(
            ']\n  });\n\n  var params = {\n    name: \'cola\',\n    nodeSpacing: 5,\n    edgeLengthVal: 45,\n    animate: true,\n    randomize: false,\n    maxSimulationTime: 1500\n  };\n  var layout = makeLayout();\n  var running = false;\n\n  cy.on(\'layoutstart\', function(){\n    running = true;\n  }).on(\'layoutstop\', function(){\n    running = false;\n  });\n\n  layout.run();\n\n  var $config = $(\'#config\');\n  var $btnParam = $(\'<div class="param"></div>\');\n  $config.append( $btnParam );\n\n  var sliders = [\n    {\n      label: \'Edge length\',\n      param: \'edgeLengthVal\',\n      min: 1,\n      max: 200\n    },\n\n    {\n      label: \'Node spacing\',\n      param: \'nodeSpacing\',\n      min: 1,\n      max: 50\n    }\n  ];\n\n  var buttons = [\n    {\n      label: \'<i class="fa fa-random"></i>\',\n      layoutOpts: {\n        randomize: true,\n        flow: null\n      }\n    },\n\n    {\n      label: \'<i class="fa fa-long-arrow-down"></i>\',\n      layoutOpts: {\n        flow: { axis: \'y\', minSeparation: 30 }\n      }\n    }\n  ];\n\n  sliders.forEach( makeSlider );\n\n  buttons.forEach( makeButton );\n\n  function makeLayout( opts ){\n    params.randomize = false;\n    params.edgeLength = function(e){ return params.edgeLengthVal / e.data(\'weight\'); };\n\n    for( var i in opts ){\n      params[i] = opts[i];\n    }\n\n    return cy.makeLayout( params );\n  }\n\n  function makeSlider( opts ){\n    var $input = $(\'<input></input>\');\n    var $param = $(\'<div class="param"></div>\');\n\n    $param.append(\'<span class="label label-default">\'+ opts.label +\'</span>\');\n    $param.append( $input );\n\n    $config.append( $param );\n\n    var p = $input.slider({\n      min: opts.min,\n      max: opts.max,\n      value: params[ opts.param ]\n    }).on(\'slide\', _.throttle( function(){\n      params[ opts.param ] = p.getValue();\n\n      layout.stop();\n      layout = makeLayout();\n      layout.run();\n    }, 16 ) ).data(\'slider\');\n  }\n\n  function makeButton( opts ){\n    var $button = $(\'<button class="btn btn-default">\'+ opts.label +\'</button>\');\n\n    $btnParam.append( $button );\n\n    $button.on(\'click\', function(){\n      layout.stop();\n\n      if( opts.fn ){ opts.fn(); }\n\n      layout = makeLayout( opts.layoutOpts );\n      layout.run();\n    });\n  }\n\n  cy.nodes().forEach(function(n){\n    var g = n.data(\'name\');\n\n    n.qtip({\n      content: [\n        {\n          name: \'GeneCard\',\n          url: \'http://www.genecards.org/cgi-bin/carddisp.pl?gene=\' + g\n        },\n        {\n          name: \'UniProt search\',\n          url: \'http://www.uniprot.org/uniprot/?query=\'+ g +\'&fil=organism%3A%22Homo+sapiens+%28Human%29+%5B9606%5D%22&sort=score\'\n        },\n        {\n          name: \'GeneMANIA\',\n          url: \'http://genemania.org/search/human/\' + g\n        }\n      ].map(function( link ){\n        return \'<a target="_blank" href="\' + link.url + \'">\' + link.name + \'</a>\';\n      }).join(\'<br />\\n\'),\n      position: {\n        my: \'top center\',\n        at: \'bottom center\'\n      },\n      style: {\n        classes: \'qtip-bootstrap\',\n        tip: {\n          width: 16,\n          height: 8\n        }\n      }\n    });\n  });\n\n  $(\'#config-toggle\').on(\'click\', function(){\n    $(\'body\').toggleClass(\'config-closed\');\n\n    cy.resize();\n  });\n\n}); // on dom ready\n\n$(function() {\n  FastClick.attach( document.body );\n});\n')
    file_output_html = file_output.replace('.js', '.html')
    with open(file_output_html, 'wb') as file2:
        if uniprot_name in description:
            description_text=description[uniprot_name]
        else:
            description_text='No description from fasta file'
        file2.write('<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset=utf-8 />\n    '
                    '<meta name="viewport" content="user-scalable=no, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, minimal-ui">\n'
                    '    \n    <title>%s</title>\n    \n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">\n    '
                    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">\n    '
                    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/4.10.3/css/bootstrap-slider.min.css">\n    '
                    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">\n    '
                    '<link href="http://cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.0/jquery.qtip.min.css" rel="stylesheet" type="text/css" />\n    '
                    '<link href="style.css" rel="stylesheet" />\n    \n    <script src="https://cdnjs.cloudflare.com/ajax/libs/fastclick/1.0.6/fastclick.min.js"></script>\n    '
                    '<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/3.10.0/lodash.min.js"></script>\n    '
                    '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>\n    '
                    '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>\n    '
                    '<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/4.10.3/bootstrap-slider.min.js"></script>\n    '
                    '<script src="https://cdn.rawgit.com/cytoscape/cytoscape.js-cola/1.6.0/cola.js"></script>\n    '
                    '<script src="http://js.cytoscape.org/js/cytoscape.min.js"></script>\n    '
                    '<script src="http://cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.0/jquery.qtip.min.js"></script>\n    '
                    '<script src="https://cdn.rawgit.com/cytoscape/cytoscape.js-qtip/2.7.0/cytoscape-qtip.js"></script>\n    '
                    '<script src="https://cdn.rawgit.com/cytoscape/cytoscape.js-cola/1.6.0/cytoscape-cola.js"></script>\n\n\n    \n    '
                    '<script src="%s"></script>\n  </head>\n  <body>\n    <div id="cy"></div>\n    \n    '
                    '<span class="fa fa-bars config-toggle" id="config-toggle"></span>\n    \n    <div id="config" class="config">\n      \n      '
                    '<div class="preamble">\n        <span class="label label-info">Target</span>\n\n        <p><a href="http://www.uniprot.org/uniprot/%s">%s</a>%s</p><p>The above protein has been detected from all the bait protein samples showing on the left.</p><p>This is a graph showing all the protein baits that contains the searched protein or peptide. Size of the circle is proportional to confidence and thickness of edges is proportional to STRING-DB score.  Use the controls below to alter the Cola.js layout parameters.</p>\n        <p>\n          Interaction by <a href="http://string-db.org">STRING-DB</a><br/>\n          Visualisation by <a href="http://js.cytoscape.org">Cytoscape.js</a><br/>\n          Layout by <a href="http://marvl.infotech.monash.edu/webcola/">Cola.js</a>\n        </p>\n      </div>\n      \n    </div>\n  </body>\n</html>\n' % (
                        uniprot_name, os.path.basename(file_output), uniprot_name, uniprot_name,
                        description_text))

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
    return corr_array[0][1:], corr_num_array


def gen_from_file_list(filename):
    for each in reversed(filename):
        protein_list, number_list = read_file_from(each)
        G = nx.Graph()
        num_ele = len(protein_list)
        for i in range(num_ele ** 2):
            y = i % num_ele
            x = (i - y) / num_ele
            if y > x and number_list[x][y] > 0.15:
                G.add_edge(protein_list[y], protein_list[x], weight=number_list[x][y] ** 0.5)

        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.6]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.6]

        pos = nx.fruchterman_reingold_layout(G)
        # pos = nx.spring_layout(G)
        # pos = nx.draw_circular(G)
        for each_position in pos.keys():
            G.node[each_position]['X'] = str(pos[each_position][0])
            G.node[each_position]['Y'] = str(pos[each_position][1])
        nx.draw_networkx_nodes(G, pos, node_size=700)
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
        nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')

        # labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

        # plt.axis('off')
        write_cytojs(G, each.replace('.csv', '.js'))
        # name = each + '.png'
        # name_gexf = each + '.gexf'
        # name_gml=each+'.gml'
        # plt.savefig(name)  # save as png
        # nx.write_gexf(G, name_gexf)
        # nx.write_gml(G, name_gml)
        # plt.close()


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def generate_description_from_fasta(fasta_file):
    des = {}
    with open(fasta_file, 'rb') as file_open:
        for line in file_open:
            if line.startswith('>'):
                split_line = line.rstrip().split('|')
                try:
                    uniprotname = split_line[1]
                    description = split_line[2]
                    des[uniprotname] = description
                except:
                    continue
    pickle.dump(des, open(parameters.description_file, 'wb'), protocol=2)
    return 0


def step_6_generate_network_from_csv(fasta_file, output_dir):
    generate_description_from_fasta(fasta_file)
    css_content = '\nhtml {\n  width: 100%;\n  height: 100%;\n}\n\nbody { \n  font: 14px helvetica neue, helvetica, arial, sans-serif;\n  width: 100%;\n  height: 100%;\n  overflow: hidden;\n}\n\n#cy {\n  position: absolute;\n  left: 0;\n  top: 0;\n  bottom: 0;\n  right: 17em;\n}\n\n.config {\n  position: absolute;\n  right: 0;\n  top: 0;\n  bottom: 0;\n  width: 17em;\n  background: rgba(0, 0, 0, 0.75);\n  box-sizing: border-box;\n  padding: 1em;\n  color: #fff;\n  transition-property: opacity;\n  transition-duration: 250ms;\n  transition-timing-function: ease-out;\n  overflow: auto;\n  z-index: 1;\n}\n\n.param {\n  margin-bottom: 1em;\n}\n\n.preamble {\n  margin-bottom: 2em;\n}\n\np {\n  margin: 0.5em 0;\n  font-size: 1.0em;\n}\n\n.param button {\n  width: 3em;\n  margin-right: 0.25em;\n}\n\na,\na:hover {\n  color: #62daea;\n}\n\n.label {\n  display: inline-block;\n}\n\n.slider {\n  display: block;\n}\n\n.config-toggle {\n  position: absolute;\n  right: 0;\n  top: 0;\n  padding: 1em;\n  margin: 0.2em;\n  cursor: pointer;\n  color: #888;\n  z-index: 9999999;\n}\n\n.config-closed .config {\n  opacity: 0;\n  pointer-events: none;\n}\n\n.config-closed #cy {\n  right: 0;\n}\n\n@media (max-width: 600px){\n  #cy {\n    right: 0;\n  }\n}\n'
    check_dir_exist(output_dir)
    os.chdir(output_dir)
    with open('style.css', 'wb') as css:
        css.write(css_content)
    exist = glob.glob("*.html")
    exist = [i.replace('.html', '.csv') for i in exist]
    exist_set = set(exist)
    filename = []
    os.chdir(parameters.sorted_csv_dir)
    for csv_file in glob.glob("*.csv"):
        if not csv_file.startswith('0.0_'):
            if csv_file not in exist_set:
                filename.append(csv_file)
    # gen_from_file_list(filename)
    job_list = chunks(filename, 200)
    # map(gen_from_file_list,job_list)
    pool = multiprocessing.Pool(processes=parameters.maximum_thread_number)
    pool.map(gen_from_file_list, job_list)
    pool.close()
    pool.join()


if __name__ == '__main__':
    step_6_generate_network_from_csv(parameters.fasta_database_path, parameters.network_dir)
