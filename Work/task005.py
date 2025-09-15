def p(g):
    h = len(g)
    w = len(g[0])

    # Find the center of the 3x3 object
    # Look for a non-zero square with non-zero neighbors in all 4 directions
    center_r, center_c = 0, 0
    for r in range(1, h-1):
        for c in range(1, w-1):
            q=[*zip(*g)]
            # Check if it has non-zero neighbors in all 4 directions
            if max(g[r-1][c-1:c+2])==max(g[r+1][c-1:c+2])==max(q[c-1][r-1:r+2])==max(q[c+1][r-1:r+2])!=0:
                center_r, center_c = r, c
                break
        if center_r != 0:
            break