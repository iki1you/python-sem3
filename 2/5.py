def find_optimal_division(N, K, M, pairs):
    graph = {i: set() for i in range(1, N+1)}
    for pair in pairs:
        graph[pair[0]].add(pair[1])
        graph[pair[1]].add(pair[0])

    def dfs(node, visited):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, visited)

    max_coherence = 0
    team1 = set()
    team2 = set()
    for i in range(1, N+1):
        visited = set()
        dfs(i, visited)
        coherence = sum(1 for v in visited if v <= K)
        if coherence > max_coherence:
            max_coherence = coherence
            team1 = visited
            team2 = {i for i in range(1, N+1)} - visited

    return team1, team2

# Чтение входных данных из файла
N, K, M = map(int, input().split())
pairs = [tuple(map(int, input().split())) for _ in range(M)]

team1, team2 = find_optimal_division(N, K, M, pairs)

# Запись участников первой и второй команд в файл

print(' '.join(map(str, team1)), '\n')
print(' '.join(map(str, team2)))
