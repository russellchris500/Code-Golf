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

    # Initialize output grid with zeros
    o = [[0] * w for _ in range(h)]

    # Extract the 3x3 object
    tile = []
    for dr in range(-1, 2):
        row = []
        for dc in range(-1, 2):
            r = center_r + dr
            c = center_c + dc
            if 0 <= r < h and 0 <= c < w:
                row.append(g[r][c])
            else:
                row.append(0)
        tile.append(row)

    # Check for surrounding objects in 8 directions and get their colors
    directions = []

    # Check 8 directions around the original 3x3 object (4x4 spacing)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the center (original object)

            # Check the 4x4 tile in this direction
            check_r = center_r - 1 + dr * 4
            check_c = center_c - 1 + dc * 4

            # Look for non-zero values in this 4x4 area
            found_color = 0
            for tr in range(4):
                for tc in range(4):
                    r = check_r + tr
                    c = check_c + tc
                    if 0 <= r < h and 0 <= c < w and g[r][c] != 0:
                        found_color = g[r][c]
                        break
                if found_color != 0:
                    break

            if found_color != 0:
                directions.append((dr, dc, found_color))

    # First place the original 3x3 object
    for dr in range(3):
        for dc in range(3):
            out_r = center_r - 1 + dr
            out_c = center_c - 1 + dc
            if 0 <= out_r < h and 0 <= out_c < w:
                o[out_r][out_c] = tile[dr][dc]

    # Extend tiles in directions where surrounding objects were found
    for dir_r, dir_c, color in directions:
        # Extend in this direction to the edge of the grid
        k = 1
        while True:
            # Calculate position for next tile in this direction
            tile_r = center_r - 1 + dir_r * 4 * k
            tile_c = center_c - 1 + dir_c * 4 * k

            # Check if tile would be completely outside grid bounds
            if (tile_r + 2 < 0 or tile_r >= h or
                tile_c + 2 < 0 or tile_c >= w):
                break

            # Place tile with the surrounding object's color
            for dr in range(3):
                for dc in range(3):
                    if tile[dr][dc] != 0:  # Only color non-zero parts of original tile
                        out_r = tile_r + dr
                        out_c = tile_c + dc
                        if 0 <= out_r < h and 0 <= out_c < w:
                            o[out_r][out_c] = color
            k += 1

    return o