import numpy as np


def is_righter(x1, y1, x2, y2):
    # if x1 == y1 == 0.0: return False
    # if x2 == y2 == 0.0: return False

    vec_prod =  x1 * y2 - x2 * y1
    # if np.allclose(vec_prod, 0):
    #     if not np.allclose(x2, 0.0):
    #         return x2 / x1 > 1
    #     elif not np.allclose(y2, 0.0):
    #         return y2 / y1 > 1
    # else:
    return vec_prod > 0


def convex_hull(points):
    # sorts points in right way
    available_idx = set(range(len(points)))
    p_id_min = 0
    for p_id in available_idx:
        if tuple(points[p_id]) < tuple(points[p_id_min]):
            p_id_min = p_id

    result_idx = [p_id_min]
    available_idx.remove(p_id_min)
    while True:
        chosen_nxt = None
        for p_id in range(len(points)):
            if result_idx[-1] == p_id:
                continue

            if chosen_nxt is None:
                chosen_nxt = p_id
                continue

            x0, y0 = points[result_idx[-1]]
            x1, y1 = points[p_id]
            x2, y2 = points[chosen_nxt]
            if is_righter(x1 - x0, y1 - y0, x2 - x0, y2 - y0):
                chosen_nxt = p_id
        if chosen_nxt not in available_idx:
            break
        result_idx.append(chosen_nxt)
        available_idx.remove(chosen_nxt)

    return [points[p_id] for p_id in result_idx]


def intersect_lines(line1, line2, diagram_size=1000):
    A1, B1, C1 = line1
    A2, B2, C2 = line2
    if np.allclose(A1 * B2, A2 * B1):
        return None

    M = np.array([[A1, B1], [A2, B2]])
    v = -np.array([[C1], [C2]])
    sol = np.linalg.inv(M).dot(v).reshape((-1,))#.astype('int32')

    def outside_borders(x):
        if np.isclose(x, 0) or np.isclose(x, diagram_size):
            return False
        return (x < 0) or (x > diagram_size)

    if any(outside_borders(x) for x in sol):
        return None

    return tuple(sol)


def ordered(i, j):
    if i < j:
        return i, j
    return j, i


def get_bisections_and_candidates(points, diagram_size=1000):
    bisection_eqs = {}
    border_lines = ((0, 1, 0), (1, 0, 0), (1, 0, - diagram_size), (0, 1, - diagram_size))
    basic_candidates = set([(0, 0), (0, diagram_size), (diagram_size, 0), (diagram_size, diagram_size)])
    for i, (x1, y1) in enumerate(points):
        for j, (x2, y2) in enumerate(points):
            if i < j:
                A = x2 - x1
                B = y2 - y1
                x0 = (x1 + x2) * 0.5
                y0 = (y1 + y2) * 0.5
                C = -(A * x0 + B * y0)
                bisection_eqs[(i, j)] = (A, B, C)
                for bl in border_lines:
                    intersection = intersect_lines((A, B, C), bl)
                    if intersection is not None:
                        basic_candidates.add(intersection)

    return bisection_eqs, basic_candidates

# пересечь серединные перпендикуляры: n - 1 перпендикуляр, (n - 1)(n - 2) / 2 точка пересечения сп
# n - 1 правильная полуплоскость (которая содержит сайт) - нужно проверить, принадлежит ли каждая точка всем
# остальным полуплоскостям.
def voronoi_diagram(points, diagram_size=1000):
    bisection_eqs, basic_candidates = get_bisections_and_candidates(points, diagram_size=diagram_size)
    cells = {}
    for i, (site_x, site_y) in enumerate(points):
        candidate_points = [candidate for candidate in basic_candidates]
        for j in range(len(points)):
            if j == i:
                continue
            for k in range(j + 1, len(points)):
                if k == i:
                    continue
                line1 = bisection_eqs[ordered(i, j)]
                line2 = bisection_eqs[ordered(i, k)]
                intersection = intersect_lines(line1, line2)
                if intersection is not None:
                    candidate_points.append(intersection)
        cell_vertices = set()
        for candidate in candidate_points:
            for j in range(len(points)):
                if j == i:
                    continue
                A, B, C = bisection_eqs[ordered(i, j)]
                candidate_value = A * candidate[0] + B * candidate[1] + C
                origin_value = A * site_x + B * site_y + C
                if (not np.isclose(candidate_value, 0)) and candidate_value * origin_value < 0:
                    break
            else:
                cell_vertices.add(candidate)
        cells[i] = convex_hull(list(cell_vertices))

    return cells
