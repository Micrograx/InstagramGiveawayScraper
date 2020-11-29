from giveaway import Giveaway
from secrets import LOGIN, PASSWORD
import time
import sys
import getopt
from multiprocessing import Process, Queue


def main(argv):

    allow_duplicates = False
    tag_ammount = 0
    require_likes = False
    require_comments = False
    excluded_accounts = []
    post_link = ""

    try:
        opts, args = getopt.getopt(argv, "hdt:lce:p:", ["tags=", "excluded=", "help", "post="])
    except getopt.GetoptError:
        print('selectwinners.py -t <Ammount of tag per comment> -e <Usernames excluded>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('selectwinners.py -p <Link to post> -c -l')
            sys.exit()
        elif opt == "-d":
            allow_duplicates = True
        elif opt in ("-t", "--tags"):
            tag_ammount = arg
        elif opt == "-l":
            require_likes = True
        elif opt == "-c":
            require_comments = True
        elif opt in ("-e", "--excluded"):
            excluded_accounts = arg
        elif opt in ("-p", "--post"):
            post_link = arg

    ig = Giveaway(LOGIN, PASSWORD, excluded_accounts)
    ig.login()
    n_likes = int(ig.get_number_likes(post_link))
    n_comments = n_likes * 2

    print("Logged in...")

    print("Likes amm: {}".format(n_likes))
    print("Comms amm: {}".format(n_comments))

    if (require_comments and require_likes):
        process_l = []

        likes = Queue()
        p_likes = Process(target=get_likes, args=(likes,))
        if (require_likes):
            p_likes.start()
            process_l.append(p_likes)

        comments = Queue()
        p_comms = Process(target=get_comments, args=(comments, tag_ammount))
        if (require_comments):
            p_comms.start()
            process_l.append(p_comms)

        for p in process_l:
            p.join()
    elif(require_comments):
        comments = ig.get_comments()
    elif(require_likes):
        likes = ig.get_people_who_liked()


    # people_to_chose = ig.check_if_liked(people_who_commented, people_who_liked)
    # print(f"There is {len(people_to_chose)} people...")
    # time.sleep(1)
    # print(f"Picking winners...")
    # ig.pick_winners(people_to_chose, 4)
    # print('Congratulations!')
    # ig.close_browser()


def get_likes(q):
    ig = Giveaway(LOGIN, PASSWORD, [])
    ig.login()
    print("Logged in... (Likes Thread)")
    print('Getting people who liked post...')
    people_who_liked = ig.get_people_who_liked()
    time.sleep(1)
    q.put(people_who_liked)


def get_comments(q, tags):
    ig = Giveaway(LOGIN, PASSWORD, [])
    ig.login()
    print("Logged in... (Comments Thread)")
    print('Getting people who commented and tagged {} friends in the post'.format(tags))
    people_who_commented = ig.get_comments()
    time.sleep(1)
    q.put(people_who_commented)


if __name__ == '__main__':
    main(sys.argv[1:])
