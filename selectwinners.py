from giveaway import Giveaway
from secrets import LOGIN, PASSWORD
import time, sys, getopt

def main(argv):

    allow_duplicates = False
    tag_ammount = 0
    require_likes = False
    require_comments = False
    excluded_accounts = []

    try:
        opts, args = getopt.getopt(argv, "hdt:lce:", ["tags=", "excluded=", "help"])
    except getopt.GetoptError:
      print 'selectwinners.py -t <Ammount of tag per comment> -e <Usernames excluded>'
      sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'selectwinners.py -t <Ammount of tag per comment> -e <Usernames excluded>'
            sys.exit()
        elif opt == "-d":
            allow_duplicates = True
        elif opt in ("-t", "--tags"):
            tag_ammount = arg
        elif opt  == "-l":
            require_likes = True
        elif opt == "-c":
            require_comments = True
        elif opt in ("-e", "--excluded"):
            excluded_accounts = arg

    ig = Giveaway(LOGIN, PASSWORD, excluded_accounts)
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