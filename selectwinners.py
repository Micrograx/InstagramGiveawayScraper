from giveaway import Giveaway
from secrets import LOGIN, PASSWORD
import time
import sys
import getopt
from multiprocessing import Process, Pipe
import random


def main(argv):

    post_link = ""

    allow_duplicates = False
    require_likes = False
    require_comments = False
    excluded_accounts = set()
    tag_ammount = 0
    winners_ammount = 1

    try:
        opts, args = getopt.getopt(argv, "hdt:lce:p:w:", ["tags=", "excluded=", "help", "post=", "winners="])
    except getopt.GetoptError:
        print('selectwinners.py -p <Post link> -e <Usernames excluded>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('selectwinners.py -p <Link to post> -c -l')
            sys.exit()
        elif opt == "-d":
            allow_duplicates = True
        elif opt in ("-t", "--tags"):
            tag_ammount = int(arg)
        elif opt == "-l":
            require_likes = True
        elif opt == "-c":
            require_comments = True
        elif opt in ("-e", "--excluded"):
            for x in arg.split(','):
                excluded_accounts.add(x)
            print(excluded_accounts)
        elif opt in ("-p", "--post"):
            post_link = arg
        elif opt in ("-w", "--winners"):
            winners_ammount = int(arg)

    if (post_link == ""):
        print("Usage: selectwinners.py -p <Post Link>")
        sys.exit(2)
    if (not require_likes and not require_comments):
        print("You need to set -c or -l or both")
        sys.exit(2)

    likes_parent, likes_child = Pipe()
    comms_parent, comms_child = Pipe()

    likes = []
    comms = []

    if (require_comments and require_likes):

        proc_like = Process(target=get_likes, args=(likes_child,post_link))
        proc_like.start()

        proc_comm = Process(target=get_comments, args=(comms_child, tag_ammount, post_link))
        proc_comm.start()

        likes = likes_parent.recv()
        comms = comms_parent.recv()

        proc_like.join()
        proc_comm.join()

        comments_with_both = [x for x in comms if x[0] in likes]
        people_to_chose = []
        
        if (not allow_duplicates):
            for comment in comments_with_both:
                if comment[0] in people_to_chose:
                    excluded_accounts.add(comment[0])
                else:
                    people_to_chose.append(comment[0])

        comments_to_chose = [x for x in comments_with_both if x[0] not in excluded_accounts]

        print(comments_to_chose)

        print(f"There is {len(comments_to_chose)} people...")


    else:
        ig = Giveaway(LOGIN, PASSWORD, tag_ammount, post_link)
        ig.login()
        print("Logged in...")

        if(require_comments):
            print('Getting people who commented and tagged {} friends'.format(tag_ammount))
            comms = ig.get_comments()
        elif(require_likes):
            print('Getting people who liked post...')
            likes = ig.get_people_who_liked()

        ig.close_browser()

    print(f"Picking winners...")
    if (winners_ammount < len(people_to_chose)):
        winners = random.sample(people_to_chose, winners_ammount)
    else:
        winners = people_to_chose

    for w in winners:
        print("Congratulations: @{}".format(w))
    


def get_likes(pipe, post_link):
    ig = Giveaway(LOGIN, PASSWORD, 0, post_link)
    ig.login()
    print("Logged in... (Likes Thread)")
    print('Getting people who liked post...')
    people_who_liked = ig.get_people_who_liked()
    time.sleep(1)
    pipe.send(people_who_liked)
    pipe.close()
    ig.close_browser()
    print("There are {} likes in the post".format(len(people_who_liked)))


def get_comments(pipe, tags, post_link):
    ig = Giveaway(LOGIN, PASSWORD, tags, post_link)
    ig.login()
    print("Logged in... (Comments Thread)")
    print('Getting people who commented and tagged {} friends in the post'.format(tags))
    people_who_commented = ig.get_comments()
    time.sleep(1)
    pipe.send(people_who_commented)
    pipe.close()
    ig.close_browser()
    print("There are {} comments in the post".format(len(people_who_commented)))


if __name__ == '__main__':
    main(sys.argv[1:])
