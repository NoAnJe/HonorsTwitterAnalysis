import os
import query_full
import update_convs_ids

if __name__ == '__main__':
    # service.py executed as script
    # do something
    curr_dir = os.getcwd()
    error = False
    while not error:
        update_convs_ids.update_ids()
        os.chdir(curr_dir)
        res = query_full.get_next_page_conv()
        if res == -1:
            error = True
        os.chdir(curr_dir)
        
        