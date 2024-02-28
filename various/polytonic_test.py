from polytonic_shift import lower_polytonic, upper_polytonic

test = "ἀἁἐἑἰἱὀὁἠἡὐὑὠὡάὰέὲήὴόὸίὶὺύώὼἄἅἔἕὄὅὂὃἤἥἴἵὔὕὤὥἂἃἒἓἢἣἲἳὒὓὢὣᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧϋϊΐῒϋῢΰῗῧ"

upper = upper_polytonic(test)
print(upper)

lower = lower_polytonic(upper)
print(lower)

if test == lower:
    print("Success!")
else:
    print("Ay caramba.")