colors = {
    'white': '00',
    'black': '01',
    'blue': '02',
    'green': '03',
    'red': '04',
    'brown': '05',
    'magenta': '06',
    'orange': '07',
    'yellow': '08',
    'lightgreen': '09',
    'cyan': '10',
    'lightcyan': '11',
    'lightblue': '12',
    'pink': '13',
    'grey': '14',
    'lightgrey': '15',
}

def color(text, color, background=None):
    ret = ''
    if (background == None):
        ret = '\003{c}{t}\003{c}'.format(t=text, c=colors[color])
    else:
        ret = '\003{c},{b}{t}\003{c},{b}'.format(t=text, c=colors[color], b=colors[background])
    return ret