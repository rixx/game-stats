import json

import matplotlib.pyplot as plt
import mpld3

from data import data


if __name__ == '__main__':
    names = ['Doc', 'Bashful', 'Grumpy', 'Dopey', 'Sneezy', 'Happy', 'Sleepy']
    absolute = [[] for _ in range(len(data[0]))]
    relative = [[] for _ in range(len(data[0]))]
    handicap = [[] for _ in range(len(data[0]))]
    stats = [{'name': name, 'times_won': 0} for name in names]
    relative_numstats = [[] for _ in range(len(['max', 'min', 'avg']))]
    absolute_numstats = [[] for _ in range(len(['max', 'min', 'avg']))]

    for line in data:
        baseline = min(line) // 10

        for index in range(len(line)):
            absolute[index].append(line[index])
            handicap[index].append(10 + (line[index] // 10) - baseline)
            if len(absolute[0]) > 1:
                relative[index].append(absolute[index][-1] - absolute[index][-2])

        if relative[0]:
            relative_numstats[0].append(max(line[-1] for line in relative))
            relative_numstats[1].append(min(line[-1] for line in relative))
            relative_numstats[2].append(sum(line[-1] for line in relative)/len(names))
            last_relative = [line[-1] for line in relative]
            stats[last_relative.index(relative_numstats[0][-1])]['times_won'] += 1
        else:
            stats[line.index(max(line))]['times_won'] += 1

        absolute_numstats[0].append(max(line))
        absolute_numstats[1].append(min(line))
        absolute_numstats[2].append(sum(line)/len(line))
    
    print(json.dumps(stats, indent=True))
    figure = plt.figure(1)
    axes = figure.add_subplot(211)
    plt.ylabel('total score')
    lines = [
        plt.plot(line, label=name)
        for line, name in zip(absolute, names)
    ]
    plt.legend(bbox_to_anchor=(0.905,1), loc='upper left', frameon=False)

    axes = figure.add_subplot(212)
    plt.xlabel('round')
    plt.ylabel('score in round')
    lines = [
        plt.plot(line, label=name)
        for line, name in zip(relative, names)
    ]
    # plt.legend()
    plt.legend(bbox_to_anchor=(0.905,1), loc='upper left')

    plt.figure(2)
    plt.title('Handicap over time')
    plt.xlabel('round')
    plt.ylabel('handicap')
    for line, name in zip(handicap, names):
        plt.plot(line, label=name)
    plt.legend(bbox_to_anchor=(0.905,1), loc='upper left')

    plt.figure(3)
    plt.subplot(211)
    plt.title('Max, min, avg score over time (total)')
    plt.xlabel('score')
    _1 = plt.plot(absolute_numstats[0], label='max')
    _3 = plt.plot(absolute_numstats[2], label='avg')
    _2 = plt.plot(absolute_numstats[1], label='min')
    # plt.legend()
    plt.legend(bbox_to_anchor=(0.905,1), loc='upper left')

    plt.subplot(212)
    plt.title('Max, min, avg score over time (relative)')
    plt.xlabel('score')
    plt.plot(relative_numstats[0], label='max')
    plt.plot(relative_numstats[2], label='avg')
    plt.plot(relative_numstats[1], label='min')
    # plt.legend()
    plt.legend(bbox_to_anchor=(0.905,1), loc='upper left')

    mpld3.save_html(
        plt.figure(1),
        'fig_scores.html',
        d3_url='/theme/js/vendor/d3.v3.min.js',
        mpld3_url='/theme/js/vendor/mpld3.v0.2.js',
        template_type='simple',
        figid='fig_scores'
    )
    mpld3.save_html(
        plt.figure(2),
        'handicap.html',
        d3_url='/theme/js/vendor/d3.v3.min.js',
        mpld3_url='/theme/js/vendor/mpld3.v0.2.js',
        template_type='simple',
        figid='fig_handicap'
    )
    mpld3.save_html(
        plt.figure(3),
        'avg_scores.html',
        d3_url='/theme/js/vendor/d3.v3.min.js',
        mpld3_url='/theme/js/vendor/mpld3.v0.2.js',
        template_type='simple',
        figid='fig_avg'
    )
    mpld3.show(local=True)
