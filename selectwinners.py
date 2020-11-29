from giveaway import Giveaway
from secrets import LOGIN, PASSWORD
import time
import sys
import getopt
from multiprocessing import Process, Pipe


def main(argv):

    allow_duplicates = False
    tag_ammount = 0
    require_likes = False
    require_comments = False
    excluded_accounts = []
    post_link = ""
    winners_ammount = 1

    try:
        opts, args = getopt.getopt(argv, "hdt:lce:p:w:", ["tags=", "excluded=", "help", "post=", "winners="])
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
            excluded_accounts = arg.split(',')
            print(excluded_accounts)
        elif opt in ("-p", "--post"):
            post_link = arg
        elif opt in ("-w", "--winners"):
            winners_ammount = arg

    likes_parent, likes_child = Pipe()
    comms_parent, comms_child = Pipe()

    likes = []
    comms = []

    if (require_comments and require_likes):

        proc_like = Process(target=get_likes, args=(likes_child,))
        proc_like.start()

        proc_comm = Process(target=get_comments, args=(comms_child, tag_ammount))
        proc_comm.start()

        likes = likes_parent.recv()
        comms = comms_parent.recv()

        proc_like.join()
        proc_comm.join()

    elif(require_comments):
        ig = Giveaway(LOGIN, PASSWORD, excluded_accounts)
        ig.login()
        comms = ig.get_comments()
        likes = comms
    elif(require_likes):
        ig = Giveaway(LOGIN, PASSWORD, excluded_accounts)
        ig.login()
        likes = ig.get_people_who_liked()
        comms = likes

    if (allow_duplicates):
        people_to_chose = [x for x in comms if x in likes]
    else:
        people_to_chose = list(set(comms) & set(likes))
    
    people_to_chose = [x for x in people_to_chose if x not in excluded_accounts]

    print(people_to_chose)

    print(f"There is {len(people_to_chose)} people...")

    print(f"Picking winners...")

    print('Congratulations!')
    ig.close_browser()


def get_likes(pipe):
    ig = Giveaway(LOGIN, PASSWORD, [])
    ig.login()
    print("Logged in... (Likes Thread)")
    print('Getting people who liked post...')
    people_who_liked = ig.get_people_who_liked()
    time.sleep(1)
    pipe.send(people_who_liked)
    pipe.close()
    ig.close_browser()


def get_comments(pipe, tags):
    ig = Giveaway(LOGIN, PASSWORD, [])
    ig.login()
    print("Logged in... (Comments Thread)")
    print('Getting people who commented and tagged {} friends in the post'.format(tags))
    people_who_commented = ig.get_comments()
    time.sleep(1)
    pipe.send(people_who_commented)
    pipe.close()
    ig.close_browser()


if __name__ == '__main__':
    main(sys.argv[1:])
