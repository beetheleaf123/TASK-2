import random


def generate_matrix(rows, columns):

    return ''.join(random.choice('01') for _ in range(rows * columns))


def create_mat_in_file(filename):

    num_matrices = random.randint(100000, 100005)

    with open(filename, 'w') as file:
        for _ in range(num_matrices):
            rows = random.randint(5, 10)
            columns = random.randint(5D, 10)
            matrix_data = generate_matrix(rows, columns)
            file.write(f'{rows}x{columns}:{matrix_data}\n')


def read_matrices_from_file(filename):
    matrices = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            dim_part, matrix_data = line.split(':')
            rows, columns = map(int, dim_part.split('x'))
            matrix = []
            for i in range(rows):
                row = list(matrix_data[i * columns:(i + 1) * columns])
                matrix.append(row)
            matrices.append(matrix)
    return matrices


def is_isolated_cluster(matrix, cluster):
    rows = len(matrix)
    columns = len(matrix[0])
    for r, c in cluster:
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < columns and (nr, nc) not in cluster:
                if matrix[nr][nc] == '1':
                    return False
    return True


def find_clusters(matrix, size):
    rows = len(matrix)
    columns = len(matrix[0])
    visited = [[False] * columns for _ in range(rows)]
    clusters = []

    def dfs(r, c, cluster):
        if r < 0 or r >= rows or c < 0 or c >= columns or visited[r][c] or matrix[r][c] == '0':
            return
        visited[r][c] = True
        cluster.append((r, c))
        if len(cluster) == size:
            return
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in cluster:
                dfs(nr, nc, cluster)

    for r in range(rows):
        for c in range(columns):
            if matrix[r][c] == '1' and not visited[r][c]:
                cluster = []
                dfs(r, c, cluster)
                if len(cluster) == size and is_isolated_cluster(matrix, cluster):
                    clusters.append(cluster)
                # Reset visited for the current cluster if it is not the correct size
                for cr, cc in cluster:
                    visited[cr][cc] = False

    return len(clusters)


def count_isolated_ones(matrix):
    isolated_count = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == '1' and is_isolated(matrix, row, col):
                isolated_count += 1
    return isolated_count


def is_isolated(matrix, row, col):
    rows = len(matrix)
    columns = len(matrix[0])
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < columns:
            if matrix[r][c] == '1':
                return False
    return True


def main():
    filename = 'mat.in'
    create_mat_in_file(filename)
    print(f'Random matrices written to {filename}')

    matrices = read_matrices_from_file(filename)
    results = []

    for matrix in matrices:
        isolated_ones = count_isolated_ones(matrix)
        clusters_of_two = find_clusters(matrix, 2)
        clusters_of_three = find_clusters(matrix, 3)
        results.append((isolated_ones, clusters_of_two, clusters_of_three))
        print(f'Isolated 1s count: {isolated_ones}')
        print(f'Clusters of two: {clusters_of_two}')
        print(f'Clusters of three: {clusters_of_three}')
        for row in matrix:
            print(''.join(row))
        print()

    with open('mat.out', 'w') as file:
        for isolated_ones, clusters_of_two, clusters_of_three in results:
            file.write(f'{isolated_ones} {clusters_of_two} {clusters_of_three}\n')


if __name__ == "__main__":
    main()
