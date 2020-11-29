from giveaway import Giveaway
from secrets import LOGIN, PASSWORD
import time, sys, getopt

def main(argv):
    giveaway_people = ['@jakobowsky', '@someone']
    ig = Giveaway(LOGIN, PASSWORD, giveaway_people)
    ig.login()
    print("Logged in...")
    print("Getting people who commented and tagged 2 friends...")
    people_who_commented = ig.get_comments()
    time.sleep(1)
    print('Getting people who liked post...')
    people_who_liked = ig.get_people_who_liked()
    time.sleep(1)
    people_to_chose = ig.check_if_liked(people_who_commented, people_who_liked)
    print(f"There is {len(people_to_chose)} people...")
    time.sleep(1)
    print(f"Picking winners...")
    ig.pick_winners(people_to_chose, 4)
    print('Congratulations!')
    ig.close_browser()



if __name__ == '__main__':
    main(sys.argv[1:])