import numpy as np


class Restaurant:
    def __init__(self, tables, num_of_diners, restaurant_width, restaurant_length):
        self.tables = tables
        self.num_of_tables = len(tables)
        self.num_of_diners = num_of_diners
        self.restaurant_width = restaurant_width
        self.restaurant_length = restaurant_length
        self.area = np.zeros((restaurant_width, restaurant_length))

    def restaurant_size(self):
        return self.area.shape()

    def tables_arrangement(self, table_index):
        print("hello")
        print(self.area)

        if table_index == self.num_of_tables + 1:
            self.tables_arrangement(table_index - 1)
        elif table_index == 1:
            print("is 1")
            was_putted = self.embed_next_table(self.tables[table_index - 1])
            print(was_putted)
            if not was_putted:
                return
            if was_putted:
                print("was putted")
                print(self.area)
                self.tables_arrangement(table_index + 1)
        else:
            print("is not 1")
            was_putted = self.embed_next_table(self.tables[table_index - 1])
            if was_putted:
                self.tables_arrangement(table_index + 1)
            else:
                return
                # Self.tables_arrangement(table_index - 1)

        return 3

    def embed_next_table(self, table):
        self.remove_table(table)
        y_value, x_value = self.find_next_empty_cell(table)
        if y_value == -1 & x_value == -1:
            return False
        self.put_table(table, y_value, x_value)
        return True

    def find_next_empty_cell(self, table):
        table_width = table.width
        table_length = table.length
        for j in range(table.curr_x_position + 1, self.restaurant_width - 1):
            if (j + table_width <= self.restaurant_width) & (table.curr_y_position < table_length):
                if ((self.area[table.curr_y_position, j] == 0) & (self.area[table.curr_y_position + table_length - 1,
                                                                            j] == 0) & (self.area[table.curr_y_position,
                                                                                                  j + table_width - 1] == 0) &
                        (self.area[
                             table.curr_y_position + table_length - 1, j + table_width - 1] == 0)):
                    return table.curr_y_position, j

        for i in range(table.curr_y_position + 1, self.restaurant_length - 1):
            for j in range(self.restaurant_width - 1):
                if (j + table_width - 1 <= self.restaurant_width - 1) & (
                        i + table_length - 1 <= self.restaurant_length - 1):

                    if ((self.area[i, j] == 0) & (self.area[i + table_length - 1, j] == 0) & (self.area[i,
                                                                                                        j + table_width - 1] == 0) &
                            (self.area[
                                 i + table_length - 1, j + table_width - 1] == 0)):
                        return i, j

        return -1, -1

    # def put_table(self, table, y_value, x_value):
    #   for i in range(y_value, y_value + table.length):
    #      for j in range(x_value, x_value + table.width):
    #         self.area[i, j] = table.table_number
    # table.curr_y_position = y_value
    # table.curr_x_position = x_value

    def remove_table(self, table):
        for i in range(self.restaurant_length):
            for j in range(self.restaurant_width):
                if self.area[i, j] == table.table_number:
                    self.area[i, j] = 0

