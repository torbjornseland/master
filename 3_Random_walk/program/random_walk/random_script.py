import os

os.system("python random_walk.py --ZN 50 --HN 10 --S 200 --g 40 --ZK 0.4 --HI 0.3  --makeplot --savefile movies_KA/RW_ZN_50_HN_10.gif")
os.system("python random_walk.py --ZN 10 --HN 50 --S 200 --g 40 --ZK 0.4 --HI 0.3  --makeplot --savefile movies_KA/RW_ZN_10_HN_50.gif")
os.system("python random_walk.py --ZN 50 --HN 50 --S 200 --g 40 --ZK 0.4 --HI 0.3  --makeplot --savefile movies_KA/RW_ZN_50_HN_50.gif")
