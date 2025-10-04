p=lambda j:[r[(m:=[*map(any,zip(*j))]).index(1):-m[::-1].index(1)]*2for r in j if any(r)]
