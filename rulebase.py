def rule_algorithm(real_size, size, match_point, real_area, area) :

    siz_ = False
    mat_ = False
    arz_ = False

    # 물체 1%

    if abs(size - real_size) < real_size / 100 * 5: # +- 5%의 오차율을 만족할때 참 값
        siz_ = True


    if match_point < 0.005 : #유사도값 0.005이하일때 참 값
        mat_ = True

    if abs(real_area - area) < real_area / 100 * 5: # +- 5%의 오차율을 만족할 때 참 값
        arz_ = True


    if siz_ and mat_ and arz_ == True : # 3개의 값 모두 참 값일 경우 정상
        return "정상"

    else :
        return "불량"






def del_arr(error_range, sizelist, matchlist, arealist) : # 패턴에서 벗어난 값 제거

    i = 0
    while i < len(sizelist):



        if abs(sizelist[i] - error_range) > 10.5: # 10.5이상의 이상치를 제거함
            del sizelist[i]
            del matchlist[i]
            del arealist[i]


        else:
            i += i


    return sizelist, matchlist, arealist


def scale_chcek(size, sizescale, area, areascale) : # scale 측정할 때 조정하여 스케일 값 측정
    s_scale = size / sizescale
    a_scale = area/ areascale

    return s_scale, a_scale 