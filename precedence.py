p1 = [
    ["A", [], 11],
    ["B", [], 18],
    ["C", ["A"], 14],
    ["D", ["A"], 8],
    ["E", ["B"], 2],
    ["F", ["C", "E"], 7],
    ["G", ["D", "F"], 3]
]

long_no_dum = [
    ["A", [], 1],
    ["B", [], 1],
    ["C", ["A"], 1],
    ["D", ["A"], 1],
    ["E", ["B"], 1],
    ["F", ["B"], 1],
    ["G", ["D"], 1],
    ["H", ["D"], 1],
    ["I", ["C", "E"], 1],
    ["J", ["F"], 1],
    ["K", ["G", "I", "J"], 1],
    ["L", ["H", "K"], 1]
]


p2 = [
    ["A", [], 3],
    ["B", [], 5],
    ["C", ["A", "B"], 2],
    ["D", ["A"], 5]
]  # a table that requires 1 dummy

fiveBQ5 = [
    ["P", [], 4],
    ["Q", [], 6],
    ["R", ["P"], 4],
    ["S", ["P"], 7],
    ["T", ["P", "Q"], 2],
]

umergeable = [
    ["A", [], 1],
    ["B", [], 2],
    ["C", [], 3],
    ["D", ["A", "B"], 6],
    ["E", ["A", "C"], 5],
    ["F", ["B", "C"], 3]
]

p_long = [  # a long and complex table, that nevertheless doesn't need dummies
    # 2 critial paths with length 54.
    ["A", [], 10],
    ["B", [], 14],
    ["C", ["A"], 11],
    ["D", ["B"], 5],
    ["E", ["B"], 15],
    ["F", ["B"], 20],
    ["G", ["C", "D"], 8],
    ["H", ["C", "D"], 12],
    ["I", ["G"], 16],
    ["J", ["E", "H"], 10],
    ["K", ["E", "H"], 21],
    ["L", ["E", "H"], 6],
    ["M", ["I", "J"], 9],
    ["N", ["F", "L"], 12],
]

line = [
    ["A", [], 2], #research
    ["B", ["A"], 4],
    ["C", ["B"], 2],
    ["D", ["C"], 3],
    ["E", ["C"], 1],
    ["F", ["D"], 3],
    ["G", ["F"], 1]
]

impossible = [  # nothing checks for this kind of situation. It will cause the
    # algorithm to hang
    ["A", [], 1],
    ["B", ["C"], 1],
    ["C", ["D"], 1],
    ["D", ["B", "A"], 1]
]

p_short = [
    ["A", [], 2],
    ["B", [], 7],
    ["C", ["A"], 4],
    ["D", ["A"], 3],
    ["E", ["C"], 2],
    ["F", ["B", "D"], 4],
    ["G", ["B"], 1]
]


mix1 = [
    ["A", [], 10],
    ["B", [], 15],
    ["C", ["B"], 11],
    ["D", ["A","C"], 5],
    ["E", ["A"], 15],
    ["F", ["E"], 20],
    ["G", ["E"], 8],
    ["H", ["G"], 12],
    ["I", ["D","F"], 16],
    ["J", ["G","I"], 10],
    ["K", ["G","I"], 21],
    ["L", ["H","K"], 6]
]

tp = [
    ["i", [], 4],
    ["ii",["i","v"],2],
    ["iii",["ii"],2],
    ["iv",["viii"],5],
    ["v",[], 6],
    ["vi",["ix","ii"],4],
    ["vii",["vi","ii","viii"],6],
    ["viii",["ii"],5],
    ["ix",[],5],
    ["x",["ii"],8]
]
# http://slideplayer.com/slide/3870208/ slide 6
new_prog = [
    ["A" ,[],1], #hire programmer
    ["B" ,[],6], #program phase 1
    ["C",[] ,2], #Obtain marketing backup
    ["D",["C"] ,1], #consolidate training plans
    ["E", [],1], #Deliver marketing for training
    ["F",["D"] ,2], #design training course
    ["G",["A"],4] ,# renumbering routine
    ["H",["C"],2], #consolidate advertising
    ["I",["B"],2], #prepare operating inststuctions
    ["J",["B","G"],6], #program phase 2
    ["K",["B","G"],2], #prepare op inst for renumbering
    ["L",["H"],5], #draft brochure
    ["M",["H"],4], #submit paper
    ["N",["H"],4], #national advertising
    ["O",["E","F"],5], #train marketing
    ["P",["J","K","I"],2], #pre op inst for phase2
    ["Q",["I"],2], # Prep phase 1 package
    ["R",["L"],3], #prep indu app copy
    ["S",["R"],1], #make ind app copy layout
    ["T",["S"],1], #print ind app brochure
    ["U",["L"],2], #make gen bro layout
    ["V",["U"],1], #print gen brochure
    ["W",["N"],2], # distribute advertising
    ["X",["Q","P"],2], #prep complete package
    ["Y",["Q"],2], #limited dist of phase 1
    ["Z",["X","Y"],1], #deliver program to marketing
    ["AA",["T","R"],1], #deliver brochure to marketing
    ["AB",["O","W","M"],3] #review national ads
]
