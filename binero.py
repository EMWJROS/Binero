#! /bin/python

"""
BINERO
The squares are to be filled with zeros and ones. Each row and column shall
contain the same number of ones and zeros. There must not be more than two
zeros or ones in line, regardless of direction. Each column must be unique.
The same holds for the rows.
"""

# CONSTANTS #############################################################
NUM_ROWS_COLS = 12;
ALL_ONES = 2**NUM_ROWS_COLS-1;
UNDETERMINED = 3;
ASCII_FOR_ZERO = 47;
BIG_NUMBER = 1000;

# UTILITIES ###############################################################

# Turns 0 or 1 into the proper ASCII char
def char_value(i) :
    return chr(i+ASCII_FOR_ZERO);

# Turns '0' or '1' into numerical value
def num_value(c):
    return ord(c)-ASCII_FOR_ZERO;

# Adjusts a binary string to proper width by prepending zeros
def adjusted(s):
    l = len(s);
    if l < NUM_ROWS_COLS:
        new_s = "0"*(NUM_ROWS_COLS-l) + s;
    else:
        new_s = s;
    return new_s;

# MAIN ALGORITHM PARTS ####################################################

# Adjusts the zones so that they only contain values consistent with the boxes
def prune():
    for r in range(NUM_ROWS_COLS):
        for c in range(NUM_ROWS_COLS):
            if box[r][c] != UNDETERMINED:
                # Prune rows
                adjusted = [];
                for p in rows[r]:
                    if zone_value[p][c] == char_value(box[r][c]):
                        adjusted.append(p);
                rows[r] = adjusted;
                # Prune cols
                adjusted = [];
                for p in cols[c]:
                    if zone_value[p][r] == char_value(box[r][c]):
                        adjusted.append(p);
                cols[c] = adjusted;

# Find zones or boxes that can only hold one value
def find_solitaries():
    # Find solitary rows
    for r in range(NUM_ROWS_COLS):
        if len(rows[r]) == 1:
            for c in range(NUM_ROWS_COLS):
                box[r][c] = num_value(zone_value[rows[r][0]][c]);
            # Remove duplicates
            for r2 in range(NUM_ROWS_COLS):
                if r != r2:
                    rows[r2] = list(filter(lambda c : c != rows[r][0], rows[r2]));          

    # Find solitary columns
    for c in range(NUM_ROWS_COLS):
        if len(cols[c]) == 1:
            for r in range(NUM_ROWS_COLS):
                box[r][c] = num_value(zone_value[cols[c][0]][r]);
            # Remove duplicates
            for c2 in range(NUM_ROWS_COLS):
                if c != c2:
                    cols[c2] = list(filter(lambda r : r != cols[c][0], cols[c2]));

    # Solitary zeros in rows
    for r in range(NUM_ROWS_COLS):
        aggregate = ALL_ONES;
        for p in rows[r]:
            aggregate = aggregate & (ALL_ONES-int(zone_value[p],2));
        row = adjusted(format(ALL_ONES-aggregate,'b'));
        for c in range(NUM_ROWS_COLS):
            if row[c] == '0':
                box[r][c] = 1;

    # Solitary ones in rows
    for r in range(NUM_ROWS_COLS):
        aggregate = ALL_ONES;
    	for p in rows[r]:
            aggregate = aggregate & int(zone_value[p],2);
        row = adjusted(format(aggregate,'b'));
        for c in range(NUM_ROWS_COLS):
            if row[c] == '1':
                box[r][c] = 2;

    # Solitary zeros in columns
    for c in range(NUM_ROWS_COLS):
        aggregate = ALL_ONES;
        for p in cols[c]:
            aggregate = aggregate & (ALL_ONES-int(zone_value[p],2));
        col = adjusted(format(ALL_ONES-aggregate,'b'));
        for r in range(NUM_ROWS_COLS):
            if col[r] == '0':
                box[r][c] = 1;

    # Solitary ones in columns
    for c in range(NUM_ROWS_COLS):
        aggregate = ALL_ONES;
        for p in cols[c]:
            aggregate = aggregate & int(zone_value[p],2);
        col = adjusted(format(aggregate,'b'));
        for r in range(NUM_ROWS_COLS):
            if col[r] == '1':
                box[r][c] = 2;

# HELPER FUNCTIONS ######################################################

# Returns the number of undetermined boxes in a zone
def num_undeter(z):
   return len(list(filter(lambda b : b == UNDETERMINED, z)));

# Returns total number of undetermined boxes
def num_of_unknowns():
   return sum(map(num_undeter, box));

# PREPARATORY FUNCTIONS #################################################

# Construct a list of possible values for a zone
def generate_possible_values():
    result = [];
    c = 0;
    for i in range(ALL_ONES+1):
        binary = adjusted(format(i, 'b'));
        # There must be 4 of each and can't be more than two in line
        if binary.count('0') == (NUM_ROWS_COLS/2) and binary.count('1') == (NUM_ROWS_COLS/2) and \
            binary.count('000') == 0 and binary.count('111') == 0:
            c = c+1;
            result.append(binary);
    return result;

# Convert puzzle to internal format
def generate_boxes(p):
    result = [];
    for i in range(NUM_ROWS_COLS):
        row = [];
        for j in range(NUM_ROWS_COLS):
	    if p[i][j] == '0':
                row.append(1);
            elif p[i][j] == '1':
                row.append(2);
            elif p[i][j] == '.':
                row.append(UNDETERMINED);
        result.append(row);
    return result;

########################################################################################

# The problem at hand
"""
puzzle = [".......1", \
          ".11...0.", \
          "0.......", \
          ".1.....1", \
          "1.11....", \
          ".1......", \
          "..0..1..", \
          ".1......"];
"""
puzzle=[".00...0.1...", \
        ".....00..0..", \
        "00.0.1......", \
        ".0..0.......", \
        "0...........", \
        "..........1.", \
        "..0......0..", \
        "........1..1", \
        ".1.........1", \
        "..0.......0.", \
        "....0..0....", \
        ".00.0...1..."];

# Board matrix, two bits for each box indicating a value of 0 (1) or 1 (2) or undetermined (3)
box = generate_boxes(puzzle);

# Binary strings representing the possible rows or columns
zone_value = generate_possible_values();

# Contains indices of zone values that are currently possible for each row or column
rows = [range(len(zone_value))]*NUM_ROWS_COLS;
cols = [range(len(zone_value))]*NUM_ROWS_COLS;

# Let's start solving!

previously_unknown = BIG_NUMBER;
currently_unknown = num_of_unknowns();
print("Number of unknowns: " + str(currently_unknown));
while currently_unknown < previously_unknown:
    prune();
    find_solitaries();
    previously_unknown = currently_unknown;
    currently_unknown = num_of_unknowns();
    print("Number of unknowns: " + str(currently_unknown));

if currently_unknown == 0:
    print("Hooooray! We solved it!");
    for r in box:
        for c in r:
            print(str(c-1) + " "),
        print;
