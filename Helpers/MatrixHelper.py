
class MatrixHelper:
    @staticmethod
    def get_matrix_index_of_element(matrix, element):
        x = 0
        for x_axis_element in matrix:
            y = 0
            for y_axis_element in x_axis_element:
                if element is y_axis_element:
                    return x, y
                y += 1
            x += 1
