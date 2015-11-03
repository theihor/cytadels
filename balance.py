from globalvars import *
from game import *

RUN_COUNT = 2000

collosus_count = 0
result = {}
for i in range(1, RUN_COUNT):
    (gs, winner) = run_game()
    if winner in result:
        result[winner] += 1
    else: result[winner] = 1
    if i % 100 == 99:
        lst = [(p, result[p]) for p in result]
        lst.sort()
        s = ""
        for p in lst: s += str(round(100.0 * p[1] / i, 1)) + '% '
        print('\r' + s + " i = " + str(i), end="")
        
     
    for p in gs.players:
        for card in p.slots:
            if card['name'] == 'Collosus':
                collosus_count += 1

print('\nCollosus was built ' + str(collosus_count) + ' times.')
#for p in result:
#    print(p + " won " + str(100.0 * result[p] / RUN_COUNT) + '%')