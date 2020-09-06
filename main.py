from pylab import *

from Table import Table

print("his")


def find_top_left_corner(board, table_number):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == table_number:
                return (i, j)


def clean_rims_right(board, j, k, table_number, num_of_tables, Tables):
    for i in range(3):
        t = 0
        while (k + t < len(board[0])) and (board[j + i][k + t] == table_number):
            if (t < 3) or (t >= Tables[table_number - 1].width-3):
                board[j + i][k + t] = 0
            else:
                board[j + i][k + t] = num_of_tables + 1

            t = t + 1


def clean_rims_down(board, j, k, table_number, num_of_tables, Tables):
    for i in range(3):
        t = 0
        while (j + t < len(board)) and (board[j + t][k + i] == table_number):
            board[j + t][k + i] = num_of_tables + 1
            t = t + 1


def locate_people(board, Tables):
    for i in range(len(Tables)):
        top_left_corner = find_top_left_corner(board, i + 1)
        clean_rims_right(board, top_left_corner[0], top_left_corner[1], i + 1, len(Tables), Tables)
        clean_rims_right(board, top_left_corner[0] + Tables[i].length - 3, top_left_corner[1], i + 1, len(Tables),
                         Tables)
        clean_rims_down(board, top_left_corner[0] + 3, top_left_corner[1], i + 1, len(Tables), Tables)
        clean_rims_down(board, top_left_corner[0] + 3, top_left_corner[1] + Tables[i].width - 3, i + 1, len(Tables),
                        Tables)


def arrange_tables(tables_list, restaurant_matrix):
    remaining_points = create_all_points(restaurant_matrix)
    best_distance = -1
    table_arrangement = []
    for _ in range(100):
        curr_remaining_points = remaining_points.copy()
        global_min_distance, current_table_arrangement = incremental_farthest_search(tables_list, curr_remaining_points)
        global_min_distance = global_min_distance / 5
        print(global_min_distance)
        if global_min_distance > best_distance:
            best_distance = global_min_distance
            table_arrangement = current_table_arrangement

    if best_distance > 0:
        board = np.zeros((len(restaurant_matrix), len(restaurant_matrix[1])))

        for j in range(len(table_arrangement)):
            board[table_arrangement[j][0], table_arrangement[j][1]] = table_arrangement[j][2]
        for k in range(len(remaining_points)):
            if remaining_points[k][2] == -1:
                board[remaining_points[k][0], remaining_points[k][1]] = -1
        print(best_distance)

        locate_people(board, Tables)

        plt.figure(1)
        plt.imshow(board, interpolation='nearest')
        plt.grid(True)
        plt.show()
    else:
        print("impossible arrangement")


def incremental_farthest_search(tables, remaining_points):
    selectedPoints = []
    global_min_distance = np.inf
    for i in range(len(tables)):
        possibleSpots = find_possible_spots(tables[i], remaining_points)
        if len(possibleSpots) == 0:
            print("failed")
            return -1, []
        min_distance, minimum_distance_coordinate = calculate_distances(possibleSpots, selectedPoints, tables[i])
        global_min_distance = min(global_min_distance, min_distance)
        put_table(tables[i], remaining_points, selectedPoints, minimum_distance_coordinate[0],
                  minimum_distance_coordinate[1])
    return global_min_distance, selectedPoints


def put_table(table, remaining_points, selected_points, x, y):
    for i in range(x, x + table.length):
        for j in range(y, y + table.width):
            next_point = remaining_points.pop(remaining_points.index((i, j, 0)))
            selected_points.append((next_point[0], next_point[1], table.table_number))


def find_possible_spots(table, remaining_points):
    possibleSpots = []

    for i in range(len(remaining_points)):
        is_possible = True
        for j in range(0, table.length):
            for k in range(0, table.width):
                if (remaining_points[i][0] + j, remaining_points[i][1] + k, 0) not in remaining_points:
                    is_possible = False
        if is_possible:
            possibleSpots.append(remaining_points[i])
    return possibleSpots


def calculate_distances(possible_spots, selected_points, table):
    global_min_distance = 0
    global_min_distance_coordinate = (-1, -1)

    if table.table_number == 1:
        n = np.random.randint(0, len(possible_spots) - 1)

        return np.inf, (possible_spots[n][0],possible_spots[n][1])

    for (i, j, k) in possible_spots:
        min_distance = np.inf
        for r in range(0, table.length):
            for m in range(0, table.width):
                for (o, p, q) in selected_points:
                    if distance(i + r, j + m, o, p) < min_distance:
                        min_distance = distance(i + r, j + m, o, p)
        if min_distance > global_min_distance:
            global_min_distance = min_distance
            global_min_distance_coordinate = (i, j)

    return global_min_distance, global_min_distance_coordinate


def distance(i, j, k, r):
    return np.math.sqrt(((i - k) ** 2) + ((j - r) ** 2))


def create_all_points(restaurant):
    res = []
    for i in range(len(restaurant)):
        for j in range(len(restaurant[0])):
            if restaurant[i][j] == 0:
                res.append((i, j, 0))
            if restaurant[i][j] == 1:
                res.append((i, j, -1))

    return res


Tables = []
nom_of_tables = int(input("Enter number of tables in your restaurant: "))
for a in range(1, nom_of_tables + 1):
    length = float(input("{}{}{}".format("Enter  the ", a, "th table length")))
    width = float(input("{}{}{}".format("Enter  the ", a, "th table width")))
    Tables.append(Table(width, length, a))

length = int((float(input("Enter max restaurant length in meters: "))) / 0.2)
width = int((float(input("Enter max restaurant width in meters: "))) / 0.2)
is_rectangle = str(input("is your restaurant has rectangle shape? "))
if is_rectangle == 'yes':
    restaurant_matrix = np.zeros((length, width))
    arrange_tables(Tables, restaurant_matrix)
else:
    matrix = []
    print("Enter the %s x %s matrix: " % (length, width))
    for a in range(length):
        matrix.append(list(map(int, input().rstrip().split())))
    arrange_tables(Tables, matrix)

# table1 = Table(2, 4, 1)
# table2 = Table(1, 6, 2)
# table3 = Table(2, 2, 3)
# table4 = Table(1, 1, 4)
# table5 = Table(3, 3, 5)
# table6 = Table(5, 5, 6)

# tables = [table1, table2, table3, table4, table5, table6]


# arrange_tables(tables, 5, (20, 20), True)
