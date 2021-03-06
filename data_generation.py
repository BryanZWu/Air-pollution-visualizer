import numpy as np
import matplotlib.pyplot as plt
import random
from csv import writer
from time import sleep

"""
New York City
Bottom Left Corner: (40.706, -74.011491)
Top Right Corner (40.777, -73.946)
Top Right of Lower Manhattan(40.75,-73.971)
"""
decay = 10 ** -100
class Node:
    ID = 100
    names = ["Stanley", "Birmingham", "Manning", "Canal", "Madison", "Bowery", "America", "Houston", "Lexington",
             "Maiden", "Christopher", "Steinway","Utopia","Love","Brooklyn","Victory"]
    suffix = ["Circle", "Boulevard", "Street", "Drive", "Way", "Avenue", "Lane", "Parkway", "Heights"]
    location = set()
    while len(location)< 116:
        location.add(random.choice(names) + " " + random.choice(suffix))
    loc_gen = location.__iter__()

    def __init__(self, cords, val=[0, 0, 0], traffic=[0, 0, 0]):
        self.id = Node.ID
        Node.ID += 1
        self.pos = cords
        self.val = val
        self.traffic = traffic
        #print(Node.loc_gen)
        self.street = Node.loc_gen.__next__()


    def dist_to(self, other):
        assert len(other.pos) == len(self.pos), "Unmatched Dimensions"
        sm = 0
        for a, b in zip(self.pos, other.pos):
            sm += (a - b) ** 2
        return sm ** 0.5

    def pol_received(self, other):
        self.val = [v + v2 * (decay ** self.dist_to(other)) for v, v2 in zip(self.val, other.val)]

    def __repr__(self):
        return [self.id, self.street] + self.pos


lat_bot, lat_top = 40.706, 40.75
lon_bot, lon_top = -74.011, -73.971
n_sources = 16
random.seed(1)
sources = []
for i in range(n_sources):
    sources.append(Node([random.uniform(lat_bot, lat_top), random.uniform(lon_bot, lon_top)],
                        [random.randint(1000, 10000) for i in range(3)]))

sensors = []
for lat in np.linspace(40.706, 40.75, 10):
    for lon in np.linspace(-74.011, -73.971, 10):
        sensors.append(Node([lat, lon], traffic=[random.randint(500, 10000) for i in range(3)]));
for src in sources:
    for sens in sensors:
        sens.pol_received(src)


def plot(sources, sensors, trafficM):
    lon = []
    lat = []
    c = []
    for p in sources:
        lat.append(p.pos[0])
        lon.append(p.pos[1])
        print(p.val)
        c.append(p.val)
    for s in sensors:
        lat.append(s.pos[0])
        lon.append(s.pos[1])
        c.append(s.val + trafficM * s.traffic)
    c = 1 - c / max(c)
    plt.style.use('grayscale')
    plt.scatter(lon, lat, c=c)
    plt.show()
    plt.close()


dM = [0.5] + [1] * 5 + [0.5]
hM = list(np.linspace(0.5, 2.5, 8)) + list(np.linspace(2.5, 1.5, 4)) + list(np.linspace(1.5, 2.5, 4)) + list(
    np.linspace(2.5, 0.5, 8))

# with open('sample_data_sources.csv', 'w', newline='') as csvfile:
#     write = writer(csvfile, delimiter=",")
#     for src in sources:
#         build = src.__repr__()
#         nxt = [str(src.val[i]) for i in range(3)]
#         build += nxt
#         write.writerow(build)


with open('sample_data_traffic.csv', 'w', newline='') as csvfile:
    write = writer(csvfile, delimiter=",")
    for s in sensors:
        build = s.__repr__()
        nxt = [str(s.traffic[i] * hM[0]) for i in range(3)]
        for h in range(1, 24):
            nxt = [nxt[i] + "$" + str(s.traffic[i] * hM[h]) for i in range(3)]
        build += nxt
        write.writerow(build)
# with open('sample_data.csv', 'w', newline='') as csvfile:
#     write = writer(csvfile, delimiter=",")
#     for s in sensors:
#         build = s.__repr__()
#         nxt = [str(s.val[i] + s.traffic[i] * hM[0]) for i in range(3)]
#         for h in range(1, 24):
#             nxt = [nxt[i] + "$" + str(s.val[i] + s.traffic[i] * hM[h]) for i in range(3)]
#         build += nxt
#         write.writerow(build)
