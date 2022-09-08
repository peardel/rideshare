import pupil

def try_distance():
    pupil1 = pupil.Pupil("GU1 1SZ", False, False, 1)
    pupil2 = pupil.Pupil("KT11 2AF", False, False, 1)

    print(pupil1.get_distance(pupil2))

try_distance()