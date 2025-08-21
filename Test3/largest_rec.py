def maximumrectangle(matrix):
    if not matrix:
        return 0
    
    rows = len(matrix)
    cols = len(matrix[0])
    max_area = 0
  
    for top in range(rows):
        for left in range(cols):
            if matrix[top][left] == 0:
                continue
  
            for bottom in range(top, rows):
                for right in range(left, cols):
                    all_once = True

                    for r in range(top, bottom+1):
                        for c in range(left, right+1):
                            if matrix[r][c] == "0":
                                all_once = False
                                break

                        if not all_once:
                            break
                    
                    if all_once:
                        area = (bottom - top + 1) * (right - left + 1)
                        max_area = max(max_area, area)

    return max_area

matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]

print(maximumrectangle(matrix))
