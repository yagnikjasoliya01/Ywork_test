def child_candies(ratings):
    if not ratings:
        return 0

    n = len(ratings)
    candies = [1] * n #[1,1,1]

    # Left to right
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Right to left
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)

print(child_candies([3,2,2]))
