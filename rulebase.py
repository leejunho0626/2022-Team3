def rule_algorithm(real_size, size, match_point, real_area, area) :

    siz_ = False
    mat_ = False
    arz_ = False

    # 물체 1%

    if abs(size - real_size) < real_size / 100 * 5:
        siz_ = True


    if match_point < 0.005 :
        mat_ = True

    if abs(real_area - area) < real_area / 100 * 10 :
        arz_ = True


    if siz_ and mat_ and arz_ == True :
        return "정상"

    else :
        return "불량"






def del_arr(error_range, sizelist, matchlist, arealist) :

    i = 0
    while i < len(sizelist):



        if abs(sizelist[i] - error_range) > 10.5:
            del sizelist[i]
            del matchlist[i]
            del arealist[i]


        else:
            i += i


    return sizelist, matchlist, arealist


def scale_chcek(size, sizescale, area, areascale) :
    s_scale = size / sizescale
    a_scale = area/ areascale

    return s_scale, a_scale