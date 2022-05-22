def rule_algorithm(real_size, size, match_point, real_area, area) :

    siz_ = False
    mat_ = False
    arz_ = False
    if abs(size - real_size) < 50 :
        siz_ = True


    if match_point < 1 :
        mat_ = True

    if abs(real_area - area) < 50 :
        arz_ = False


    if siz_ and mat_ and arz_ == True :
        return True

    else :
        return False






def del_arr(error_range, sizelist, matchlist, arealist) :

    i = 0
    while i < len(sizelist):

        if abs(sizelist[i] - error_range) > 50:
            del sizelist[i]
            del matchlist[i]
            del arealist[i]


        else:
            i = i + 1


    return sizelist, matchlist, arealist


