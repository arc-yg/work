
def retroactive_resolution(coefficients: list, vector: list, dem: int) -> list:

    x = [0.0] * dem
    for i in reversed(range(dem)):
        sum = 0
        for j in range(i + 1, dem):
            sum += coefficients[i*dem + j] * x[j]
        x[i] = (vector[i] - sum) / coefficients[i*dem + i]

    return x


def gaussian_elimination(coefficients: list, vector: list, dem: int) -> list:
    # coefficients must to be a square matrix so we need to check first
    if len(coefficients) != dem*dem or len(vector) != dem:
        return []
    
    # augmented matrix

    # scale the matrix leaving it triangular
    for i in range(dem - 1):
        pivot = coefficients[i*dem + i]
        for j in range(i + 1, dem):
            factor = coefficients[j*dem + i] / pivot
            for k in range(dem):
                coefficients[j*dem + k] -= factor * coefficients[i*dem + k]
            vector[j] -= factor * vector[i]

    x = retroactive_resolution(coefficients, vector, dem)

    return x


if __name__ == "__main__":
    x = gaussian_elimination([3, 2, 5, 2], [5, 5], 7)
    print(x)
    x = gaussian_elimination([2, 2, -1, 0, -2, -1, 0, 0, 5], [5, -7, 15], 3)
    print(x)
    x = gaussian_elimination([2, 2, -1, 0, -2, -1, 0, 0], [5, -7, 15], 3)
    print(x)