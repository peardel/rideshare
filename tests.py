import student

def try_distance():
    pupil1 = student.Pupil("GU1 1SZ", False, False, 1)
    pupil2 = student.Pupil("RH10 7PC", False, False, 1)

    print(pupil1.get_distance(pupil2))

try_distance()