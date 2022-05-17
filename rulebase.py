def rule_algorithm(real_size, size, real_match_point, match_point) :

    siz_ = false
    mat_ = false
    if abs(size - real_size) < 50 :
        siz_ = true


    if abs(real_match_point - match_point) < 50 :
        mat_ = true



    if siz_ and mat_ == true :
        return true

    else :
        return false





